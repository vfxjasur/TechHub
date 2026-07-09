release: python manage.py migrate
web: gunicorn --pythonpath . techhub.wsgi:application