from .models import Comment, Contact, Subscription
from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django import forms
from tuedo import config
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment_body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input is-standardform', 'id':'id_name'}),
            'email': forms.TextInput(attrs={'class': 'input is-standardform', 'id':'id_email'}),
            'comment_body': forms.Textarea(attrs={'rows': 6, 'class': 'textarea is-standardform', 'id':'id_comment_body'}),
        }
        labels = {
            'name': _('Name'),
            'email': _('E-Mail'),
            'comment_body': _('Kommentar'),
        }

        error_messages={
            'name': config.ERROR_MSG_REQUIRED,
            'email': {**config.ERROR_MSG_REQUIRED, **config.ERROR_MSG_EMAIL_INVALID},
            'comment_body': config.ERROR_MSG_REQUIRED,
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.dataset_error_msg = config.DATASET_ERROR_MSG


class CaptchaForm(forms.Form):

    captcha_code = None
    captcha_input = forms.CharField(max_length=10, error_messages= {**config.ERROR_MSG_REQUIRED, **config.ERROR_MSG_CAPTCHA_INVALID})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset_error_msg = config.DATASET_ERROR_MSG

    def clean_captcha_input(self):
        captcha_passed = self.cleaned_data.get('captcha_input')
        if self.captcha_code != captcha_passed:
            field = self.fields.get('captcha_input')
            raise forms.ValidationError(field.error_messages.get('invalid'))
        return captcha_passed


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset_error_msg = config.DATASET_ERROR_MSG

    class Meta:
        model = Contact
        fields = ('name', 'email', 'content', 'confirmed')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input is-standardform', 'id':'id_name'}),
            'email': forms.TextInput(attrs={'class': 'input is-standardform', 'id':'id_email'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'textarea is-standardform', 'id':'id_content'}),
            'confirmed': forms.CheckboxInput(attrs={'class': '',  'id':'id_confirmed', 'checked': 'unchecked'}),
        }
        labels = {
            'name': _('Name'),
            'email': _('E-Mail'),
            'content': _('Ihre Nachricht'),
            'confirmed': format_lazy(_("Ich habe die <a href=\"{link}\">Datenschutzbestimmungen</a> gelesen und bestätige hiermit meine Zustimmung."), link=reverse_lazy('datenschutz')),
        }
    
        error_messages={
            'name': config.ERROR_MSG_REQUIRED,
            'email': {**config.ERROR_MSG_REQUIRED, **config.ERROR_MSG_EMAIL_INVALID},
            'content': {**config.ERROR_MSG_REQUIRED},
            'confirmed': config.ERROR_MSG_REQUIRED,
        }
    

        
        
    def clean_confirmed(self):
        confirmed_passed = self.cleaned_data.get('confirmed')
        if confirmed_passed is False:
            field = self.fields.get('confirmed')
            raise forms.ValidationError(field.error_messages.get('required'))
        return True
    


class SubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset_error_msg = config.DATASET_ERROR_MSG

    class Meta:
        model = Subscription
        fields = ('subscription_email',)
        widgets = {
            'subscription_email': forms.TextInput(attrs={'class': 'input is-standardform'}),
        }
        labels = {
            'subscription_email': _('Newsletter abonnieren'),
        }
        error_messages={
            'subscription_email': {**config.ERROR_MSG_REQUIRED, **config.ERROR_MSG_EMAIL_UNIQUE, **config.ERROR_MSG_EMAIL_INVALID},
        }
