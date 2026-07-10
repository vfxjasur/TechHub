"""
WSGI config for techhub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techhub.settings')

if os.environ.get('RENDER'):
    import django
    django.setup()
    from django.core.management import call_command

    call_command('migrate', '--noinput', verbosity=0)
    try:
        call_command('collectstatic', '--noinput', verbosity=0)
    except Exception:
        pass

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
