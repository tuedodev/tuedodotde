from .forms import SubscriptionForm
from django.middleware.csrf import get_token
from django.utils.functional import SimpleLazyObject
from django.urls import reverse
from meta.views import Meta
from tuedo import config, settings

from django.utils import translation

def get_subscription_form(request):
    subscription_form = SubscriptionForm()
    path = request.get_full_path()
    def _get_value():
        token = get_token(request)
        if token is None:
            return 'NOTPROVIDED'
        else:
            return token
    return { 'subscription_form': subscription_form, 'csrf_token': SimpleLazyObject(_get_value), 'subscribe_button': config.BUTTON['subscribe'], 'site_path': path }

def getConfigData(request):
    language_short = settings.LANGUAGE_CODE
    if request.method == 'GET':
        try:
            language_short = request.language_short
        except:
            pass
    context = {
        'search_path': reverse('search'),
        'social_links': config.SOCIAL_LINKS,
        'navbar_items': config.NAVBAR_ITEMS,
        'website_title': config.WEBSITE_TITLE,
        'website_owner': config.WEBSITE_OWNER,
        'footer_year': f"{config.WEBSITE_STARTING_YEAR}" if config.CURRENT_YEAR==config.WEBSITE_STARTING_YEAR else f"{config.WEBSITE_STARTING_YEAR}-{config.CURRENT_YEAR}",
        'language_short': language_short,
        'google_site_verification': config.GOOGLE_SITE_VERIFICATION if not config.DEBUG else '',
    }
    return context

def getDefaultMetaTags(request):
    meta = Meta(
        **config.METATAGS.get('default')
    )
    return {'meta':meta}
