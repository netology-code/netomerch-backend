#!/usr/bin/env bash

set -euxo pipefail

bash ./wait.sh "$POSTGRES_HOST:$POSTGRES_PORT" -- python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4 --timeout 60
