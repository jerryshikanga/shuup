# Generated by Django 2.2.24 on 2021-09-16 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shuup', '0100_pesapalpayment_amount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PesapalPayment',
        ),
    ]
