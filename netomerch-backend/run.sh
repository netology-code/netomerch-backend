#!/bin/sh

cd /netomerch-backend
bash ./wait.sh db-postgres:5432 -- python manage.py migrate --no-input

gunicorn --bind 0.0.0.0:8000 config.wsgi
