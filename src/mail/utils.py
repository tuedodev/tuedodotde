from django.core.mail import send_mail
from tuedo import config

def send_email_out(email_dict):
    sender = config.WEBSITE_SENDER
    receiver = email_dict.get('receiver')
    fail_silently = email_dict.get('fail_silently')
    subject = email_dict.get('subject')
    body = email_dict.get('body')
    if fail_silently is None:
        fail_silently = True
    if subject:
        send_mail(subject, body, sender, receiver, fail_silently)