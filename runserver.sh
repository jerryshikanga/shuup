#!/bin/bash

# python3 setup.py build_resources RUN thus manually to save on boot time
python3 -m shuup_workbench migrate
python3 -m shuup_workbench shuup_init

echo '
from django.contrib.auth import get_user_model
from django.db import IntegrityError
try:
    get_user_model().objects.create_superuser("admin", "admin@admin.com", "admin")
except IntegrityError:
    pass'\
| python3 -m shuup_workbench shell

python3 -m shuup_workbench runserver 0.0.0.0:8001