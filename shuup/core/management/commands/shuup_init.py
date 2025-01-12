# This file is part of Shuup.
#
# Copyright (c) 2012-2021, Shuup Commerce Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db.transaction import atomic
from six import print_

from shuup import configuration
from shuup.core.defaults.order_statuses import create_default_order_statuses
from shuup.core.models import Currency, CustomerTaxGroup, ProductType, SalesUnit, Shop, ShopStatus, Supplier
from shuup.core.models._taxes import ZERO_TAX_CLASS_ID
from shuup.core.payments.providers.pesapalprod.constants import PESAPAL_PAYMENT_METHOD_ID
from shuup.core.telemetry import get_installation_key, is_telemetry_enabled
from shuup.xtheme import set_current_theme


def schema(model, identifier, **info):
    return locals()


class Initializer(object):
    schemata = [
        schema(ProductType, "default", name="Standard Product"),
        schema(ProductType, "digital", name="Digital Product"),
        schema(Supplier, "default", name="Default Supplier"),
        schema(CustomerTaxGroup, "default_person_customers", name="Retail Customers"),
        schema(CustomerTaxGroup, "default_company_customers", name="Company Customers"),
    ]

    def __init__(self):
        self.objects = {}

    def create_default_shop(self):
        print_("Creating shop ...", end=" ")
        kwargs = dict(identifier="default")
        shop, _ = Shop.objects.get_or_create(**kwargs)
        shop.domain = "127.0.0.1:8001"
        shop.status = ShopStatus.ENABLED
        shop.maintenance_mode = False
        shop.currency = "KES"
        shop.name = "Dawa Sasa Test Shop"
        shop.public_name = "Dawa Sasa Test Shop"
        shop.save()
        print(f"ID {shop.id} Done.")
        return shop

    def process_schema(self, schema):
        model = schema["model"]
        assert issubclass(model, Model)
        identifier_attr = getattr(model, "identifier_attr", "identifier")
        obj = model.objects.filter(**{identifier_attr: schema["identifier"]}).first()
        if obj:
            return obj
        print_("Creating %s..." % model._meta.verbose_name, end=" ")
        obj = model()
        setattr(obj, identifier_attr, schema["identifier"])
        for key, value in schema["info"].items():
            if value in self.objects:
                value = self.objects[value]
            setattr(obj, key, value)
        obj.full_clean()
        obj.save()
        print_(obj)
        if isinstance(obj, Supplier):
            print_("Adding shop for supplier...")
            obj.shops.add(Shop.objects.first())

        return obj

    def create_sales_units(self):
        print_("Creating sales units ...", end=" ")
        sales_units = [
            dict(identifier="pcs", name="Pieces", symbol="pcs"),
            dict(identifier="mls", name="Mili litres", symbol="mls"),
            dict(identifier="tabs", name="Tablet", symbol="tab"),
        ]
        for unit in sales_units:
            name = unit.pop('name')
            symbol = unit.pop('symbol')
            unit, _ = SalesUnit.objects.get_or_create(**unit)
            unit.name = name
            unit.symbol = symbol
            unit.save()
        print_("Done.")

    def create_currency(self):
        print_("Creating currencies ...", end=" ")
        currency_codes = ["KES", "USD", "EUR"]
        Currency.objects.all().delete()
        for code in currency_codes:
            Currency.objects.get_or_create(code=code, decimal_places=2)
        print_("done.")

    def create_payment_method(self, shop):
        print_("Creating payment method...", end=" ")
        kwargs = dict(identifier=PESAPAL_PAYMENT_METHOD_ID)
        from shuup.core.models import PaymentProcessor
        processor, _ = PaymentProcessor.objects.get_or_create(**kwargs)
        processor.name = "Pesapal"
        processor.enabled = True
        processor.save()
        from shuup.core.models import TaxClass
        zero_tax, _ = TaxClass.objects.get_or_create(identifier=ZERO_TAX_CLASS_ID)
        method_args = dict(identifier=PESAPAL_PAYMENT_METHOD_ID, shop=shop, tax_class=zero_tax)
        from shuup.core.models import PaymentMethod
        method, _ = PaymentMethod.objects.get_or_create(**method_args)
        method.name = 'Pesapal'
        method.payment_processor = processor
        method.description = 'Pay via Card, banks and Mpesa'
        method.enabled = True
        method.save()
        print_("done.")
        return method

    def run(self):
        shop = self.create_default_shop()
        self.create_currency()
        for schema in self.schemata:
            self.objects[schema["model"]] = self.process_schema(schema)
        self.create_sales_units()
        self.create_payment_method(shop)
        # Ensure default statuses are available
        print_("Creating order statuses...", end=" ")
        create_default_order_statuses()
        print_("done.")
        if not settings.DEBUG and is_telemetry_enabled():
            try:
                data = json.dumps({"key": get_installation_key()})
                resp = requests.get(url=settings.SHUUP_SUPPORT_ID_URL, data=data, timeout=5)
                if resp.json().get("support_id"):
                    configuration.set(None, "shuup_support_id", resp.json().get("support_id"))
            except Exception:
                print_("Failed to get support id.")

        set_current_theme("shuup.themes.classic_gray", Shop.objects.first())

        print_("Initialization done.")


class Command(BaseCommand):
    leave_locale_alone = True

    def handle(self, *args, **options):
        with atomic():
            Initializer().run()
