#!/bin/bash
# Create a new user
export DJANGO_SUPERUSER_PASSWORD='admin'
python manage.py createsuperuser --username admin --email admin@x.com --no-input --database "{'ENGINE': 'django.db.backends.postgresql','NAME': 'postgres',  'USER': 'postgres',        'PASSWORD': 'postgres',        'HOST': 'db',        'PORT': '5432',}"
