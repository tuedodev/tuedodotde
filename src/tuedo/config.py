import environ
import datetime
from django.utils.translation import gettext_lazy as _

env = environ.Env()
env.read_env(env.str('./', '.env'))

DEBUG = env.bool('DEBUG')
WEBSITE_OWNER = env('WEBSITE_OWNER')
WEBSITE_URL = env('WEBSITE_URL')
WEBSITE_ADMINISTRATION_EMAIL = env('WEBSITE_ADMINISTRATION_EMAIL')
WEBSITE_SENDER = env('WEBSITE_SENDER')
WEBSITE_STARTING_YEAR =env.int('WEBSITE_STARTING_YEAR')
WEBSITE_TITLE = ('Tuedo', 'The Vibrant World of the Web.')
 
now = datetime.datetime.now()
CURRENT_YEAR = now.year

if DEBUG is True:
    WEBSITE_URL = 'http://127.0.0.1:8000'
    
# Available Languages
LANGUAGES = (
    (1, 'de'),
    (2, 'en'),
)
# Sites for Sitecontent model
SITES = (
    (0, 'about'),
    (1, 'datenschutz'),
    (2, 'references'),
    (3, 'imprint'),
)

# Extra Meta Tags Values
METATAGS = {
    'default': {
        'title': _('Tuedo: The Vibrant World of the Web'),
        'description': _('Tuedo: Webblog über Web-Development, Python, Django, Web-Design, CSS, React, Javascript, Gatsby'),
        'keywords' : [_('Web Development'), _('Blog'), _('Python'), _('Javascript'), _('Portfolio Website')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'imprint' : {
        'title': _('Tuedo | Impressum'),
        'description': _('Impressum Rechtliche Hinweise von Tuedo Web-Development'),
        'keywords' : [_('Impressum'), _('Imprint'), _('Rechtliche Hinweise'), _('Adresse')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'contact' : {
        'title': _('Tuedo | Kontakt Feedback Seite'),
        'description': _('Kontakt und Feedback Seite von Tuedo Web-Development'),
        'keywords' : [_('Kontakt'), _('Feedback'), _('Anfrage'), _('Bewertung')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'references' : {
        'title': _('Tuedo | Markus Felder Web-Developer Referenzen'),
        'description': _('Markus Felder Web-Developer Referenzen Portfolio'),
        'keywords' : [_('Web-Development'), _('Full-Stack Web-Developer'), _('Web-Entwickler'), _('Frontside Web-Developer')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'about' : {
        'title': _('Tuedo | Markus Felder Web-Developer About'),
        'description': _('Markus Felder Web-Developer About-Site'),
        'keywords' : [_('Web-Development'), _('About'), _('Bio'), _('Biografie'), _('Portfolio')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'werkstatt' : {
        'title': _('Tuedo | Software Werkstatt'),
        'description': _('Werkstatt für Web-Development Django React Gatsby Javascript PHP'),
        'keywords' : [_('Web-Development'), _('Django'), _('Gatsby'), _('React'), _('PHP'), _('Wordpress'), _('Javascript'), _('Rust')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
    'privacy' : {
        'title': _('Tuedo | Datenschutzerklärung'),
        'description': _('Datenschutzerklärung von Tuedo c/o MemoTrek Technologies Vertrieb e. K.'),
        'keywords' : [_('Datenschutz'), _('privacy'), _('Datenschutzerklärung')],
        'extra_props': {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
            'robots': 'noindex',
            'googlebot': 'noindex',
        },
        'extra_custom_props':[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    },
}

BLOGS_PER_PAGE = 7

#True: Prefix in URL for default language (settings.LANGUAGE_CODE)
LANGUAGE_DEFAULT_PREFIX = False

COMMENT_FIELDS = ['name', 'email', 'comment_body']
CONTACT_FIELDS = ['name', 'email', 'content', 'confirmed']
CAPTCHA_FIELDS = ['captcha_input']

CATEGORY_PREFIX = "#"

NAVBAR_ITEMS = [
    ('navbar-item', [_('Werkstatt'), 'werkstatt', 'navbar-link is-size-3 is-arrowless'], []),
    ('navbar-item has-dropdown is-hoverable', [_('About'), 'about', 'navbar-link is-size-3 is-arrowless'], [
        ('navbar-dropdown is-boxed', [_('Referenzen'), 'referenzen', 'navbar-item is-size-3 is-arrowless'], []),
    ]),
    ('navbar-item has-dropdown is-hoverable', [_('Kontakt'), 'kontakt', 'navbar-link is-size-3 is-arrowless'], [
        ('navbar-dropdown is-boxed', [_('Impressum'), 'impressum', 'navbar-item is-size-3 is-arrowless'], []),
        ('navbar-dropdown is-boxed', [_('Datenschutz'), 'datenschutz', 'navbar-item is-size-3 is-arrowless'], []),
    ]),
]

BUTTON = {
    'okay': _('Okay'),
    'send': _('Senden'),
    'home': _('Startseite'),
    'subscribe': _('Abonnieren'),
    'going_home': _('Zur Startseite'),
}

MESSAGE = {
    'comment_success': [_('Vielen Dank für Ihren Kommentar.'), _('Nach einer Prüfung wird er freigeschaltet.')],
    'error_transfer_data':  [_('Bei der Übermittlung der Daten ist ein Fehler aufgetreten.')],
    'error_unknown_homepage': [_('Ein unbekannter Fehler ist aufgetreten.'), _('Sie werden zur Startseite geleitet.')],
    'contact_success': [_('Vielen Dank für Ihre Kontaktanfrage.'), _('Wir setzen uns in Kürze mit Ihnen in Verbindung.'), _('Sie werden zur Startseite geleitet.')],
    'subscription_success': [_('Vielen Dank! Sie haben unseren Newsletter abonniert.'), _('Sie können sich jederzeit wieder abmelden.'), _('Beachten Sie die Unsubscribe-Hinweise im Newsletter.')],
    'subscribe_newsletter_warning': _('Ihr Newsletter-Abo wurde bereits freigeschaltet.'),
    'subscribe_newsletter_success': _('Vielen Dank! Ihr Newsletter-Abo wurde erfolgreich freigeschaltet.'),
    'unsubscribe_newsletter': _('Schade, dass Sie sich abgemeldet haben. Ihr Newsletter-Abonnement wurde gekündigt. Sie erhalten keine weiteren Newsletter.'),
    'confirm_comment_warning': _('Der Kommentar wurde bereits freigeschaltet.'),
    'confirm_comment_success': _('Der Kommentar wurde freigeschaltet.'),
    'delete_comment': _('Der Kommentar wurde gelöscht.'),
    'captcha_modal_header': _('Gleich haben Sie es geschafft.'),
    'captcha_modal_message': [_('Bitte geben Sie folgenden Sicherheitscode (Captcha) zum Schutz vor Spam-Bots ein.'), _('Zum Aktualisieren des Codes klicken Sie bitte auf das Reload-Icon.')],
    'modal_message_header': _('Danke!'),
}

HINT = {
    'previous-blog': _('Vorheriger Artikel'),
    'next-blog': _('Nächster Artikel'),
    'comments_empty_message': _('Dieser Beitrag wurde bisher nicht kommentiert.'),
    'comments_add_comment': _('Kommentar hinzufügen'),
}

TEXT = {
    'comments_number_string': (_('Keine Kommentare'), _('{} Kommentar'), _('{} Kommentare')),
    'comment': _('Kommentar'),
    'comment_reply': _('Antwort'),
    'comment_by': _('von'),
    'comment_on': _('am'), 
    'comment_at': _('um'),
    'comment_notification': _('Ihr Kommentar wird geprüft und freigeschaltet.'),
    'error_page_header': _('Ooops! Fehlercode {{ status }}'),
    'read_on': _('Weiterlesen'),
    'searching': _('Suche'),    
    'searching_for': _('nach'),
    'searching_hits': _('Treffer'),
    'searching_no_hits': _('Keine Suchergebnisse'),
    'searching_category': _('Kategorie'),
    'captcha_code': _('Captcha-Code')
}

TEMPLATE_HEADERS = {
    'about': (_('About'), 'Markus Felder', _('Web Developer')),
    'imprint': _('Impressum'),
    'contact': (_('Kontakt'),_('Fragen? Anregungen? Interesse an Webdev?'), _('Kontaktieren Sie mich noch heute.')),
    'references': _('Referenzen'),
    'privacy': (_('Datenschutz'), _('Datenschutzerklärung'), _('Unsere Datenschutzerklärung')),
}

EMAIL_TEMPLATES = {
    'subscription': {
        'subject': _('Herzlich Willkommen bei Tuedo - The Vibrant Web Developer Site'),
    },
    'new-comment-alert': {
        'subject': _('Tuedo-Administrator: Ein neuer Kommentar muss freigeschaltet werden'),
    },
    'new-contact-alert': {
        'subject': _('Tuedo-Administrator: Eine neue Kontaktanfrage ist eingetroffen'),
    },
}

ERROR_PAGES_MSG = {
    '404': _('Die angeforderte Seite wurde nicht gefunden.'),
    '500': _('Beim Server ist ein Problem aufgetreten.'),
    '403': _('Unberechtigter Zugriff auf Ressource.'),
    '400': _('Ein allgemeiner Fehler ist aufgetreten.'),
}

ERROR_MSG_REQUIRED = {'required': _('Bitte Pflichtfeld ausfüllen.'),}
ERROR_MSG_EMAIL_UNIQUE = {'unique': _('Diese E-Mail-Adresse ist bereits registriert.'),}
ERROR_MSG_EMAIL_INVALID = {'invalid': _('Diese E-Mail-Adresse ist nicht gültig.'),}
ERROR_MSG_INVALID = {'invalid': _('Ungültige Eingabe.'),}
ERROR_MSG_CAPTCHA_INVALID = {'invalid': _('Der eingegebene Code ist nicht korrekt.'),}

DATASET_ERROR_MSG = {
    'data-error_msg_required': ERROR_MSG_REQUIRED.get('required'),
    'data-error_msg_email_unique': ERROR_MSG_EMAIL_UNIQUE.get('unique'),
    'data-error_msg_email_invalid': ERROR_MSG_EMAIL_INVALID.get('invalid'),
    'data-error_msg_invalid': ERROR_MSG_INVALID.get('invalid'),
    'data-error_msg_captcha_invalid': ERROR_MSG_CAPTCHA_INVALID.get('invalid'),
}

SOCIAL_LINKS = {
    'github': ('https://github.com/tuedodev', 'fab fa-github fa-3x'),
    'twitter': ('https://twitter.com/tuedodev', 'fab fa-twitter fa-3x'),
    'codepen': ('https://codepen.io/tuedodev', 'fab fa-codepen fa-3x'),
}

GOOGLE_SITE_VERIFICATION = env('GOOGLE_SITE_VERIFICATION')

# Functions
def getLanguageCode(code):
    for tup in LANGUAGES:
        (lang_code, lang_short) = tup
        if lang_short == code:
            return lang_code

def getLanguageShort(code):
    for tup in LANGUAGES:
        (lang_code, lang_short) = tup
        if lang_code == code:
            return lang_short