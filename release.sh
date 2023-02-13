#!/bin/sh

python manage.py migrate_schemas election
python manage.py migrate election

python manage.py init_public_client
python manage.py init_admin
