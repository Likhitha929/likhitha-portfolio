#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
python manage.py loaddata fixtures/content.json
python manage.py createsuperuser --noinput || true

exec gunicorn config.wsgi:application