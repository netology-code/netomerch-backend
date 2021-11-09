#!/bin/sh

cd /netomerch-backend

bash ./wait.sh $DB_HOST:$DB_PORT -- python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 config.wsgi
