release: python manage.py migrate
web: gunicorn techhub.wsgi:application --bind 0.0.0.0:$PORT 