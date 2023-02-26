#!/usr/bin/env bash

set -e

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py makemigrations

python manage.py makemigrations app

python manage.py migrate --noinput

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini
