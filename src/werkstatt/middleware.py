from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
from django.utils import translation
from tuedo import settings, config
from .utils import getCurrentLanguage

# Custom Middleware enforcing CSRF Cookie in every request
class ForceCsrfCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_token(request)

# Custom Middleware Enforcing Standard Language (can be overwritten in blogpost view)
class SetLanguageForView(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.language_short = settings.LANGUAGE_CODE
        if request.method == 'GET':
            current_language = getCurrentLanguage(view_kwargs)
            request.language_short = current_language
            translation.activate(current_language)