from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin

# Custom Middleware enforcing CSRF Cookie in every request
class ForceCsrfCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_token(request)