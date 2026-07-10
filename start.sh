#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate --noinput

exec gunicorn techhub.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
