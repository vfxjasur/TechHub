from django.utils.translation import activate, get_language
from django.conf import settings


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.session.get('language', settings.LANGUAGE_CODE)
        activate(lang)
        request.LANGUAGE_CODE = lang
        return self.get_response(request)
