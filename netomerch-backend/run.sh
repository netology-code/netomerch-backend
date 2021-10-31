#!/bin/sh

cd /netomerch-backend
python manage.py migrate --no-input
gunicorn --bind 0.0.0.0:8000 config.wsgi
