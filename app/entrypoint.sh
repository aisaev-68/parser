#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_superuser
python manage.py run_parser
#python manage.py dumpdata rate > tests/fixtures/rate-fixtures.json
python manage.py runserver 0.0.0.0:8000