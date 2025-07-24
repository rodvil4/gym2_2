#!/usr/bin/env bash

set -o errexit

#Build the project

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '@gmail.com', 'RoDa2025$.');
    print('Superusuario creado exitosamente.');
else:
    print('El superusuario ya existe.');
"


