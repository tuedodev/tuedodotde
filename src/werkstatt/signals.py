from django.db.models.signals import post_save
from django.dispatch import receiver
from werkstatt.models import Subscription, Comment, Contact
from mail.utils import send_email_out
from tuedo import config
from django.template.loader import render_to_string
from django.template import Context, Template


@receiver(post_save, sender=Subscription)
def save_subscription(sender, instance, **kwargs):
    receiver = []
    receiver.append(instance.subscription_email)
    method = 'confirm-subscription'
    subscribe_link = f"{config.WEBSITE_URL}/mail?action={method}&user-id={instance.pk}&hash={instance.subscribe_hash}"
    unsubscribe_link = f"{config.WEBSITE_URL}/mail?action=unsubscribe&user-id={instance.pk}&hash={instance.unsubscribe_hash}"
    body = render_to_string('email/subscription.txt', {
                            'subscribe_link': subscribe_link,
                            'unsubscribe_link': unsubscribe_link,
                        })
    email_dict = {
        'receiver': receiver,
        'fail_silently': False,
        'subject': config.EMAIL_TEMPLATES['subscription']['subject'],
        'body': body,
    }
    if instance.active is not True:
        send_email_out(email_dict)

@receiver(post_save, sender=Comment)
def save_comment(sender, instance, **kwargs):
    receiver = []
    receiver.append(config.WEBSITE_ADMINISTRATION_EMAIL)
    confirm_link = f"{config.WEBSITE_URL}/mail?action=confirm-comment&comment-id={instance.pk}&hash={instance.confirm_hash}"
    delete_link = f"{config.WEBSITE_URL}/mail?action=delete-comment&comment-id={instance.pk}&hash={instance.confirm_hash}"
    body = render_to_string('email/new-comment-alert.txt', {
                            'confirm_link': confirm_link,
                            'delete_link': delete_link,
                            'blogpost': instance.blogpost_short,
                            'comment_short': instance.comment_body_short,
                        })
    email_dict = {
        'receiver': receiver,
        'fail_silently': False,
        'subject': config.EMAIL_TEMPLATES['new-comment-alert']['subject'],
        'body': body,
    }
    if instance.confirm_hash != 'confirmed' and not instance.reply:
        send_email_out(email_dict)

@receiver(post_save, sender=Contact)
def save_comment(sender, instance, **kwargs):
    receiver = []
    receiver.append(config.WEBSITE_ADMINISTRATION_EMAIL)
    body = render_to_string('email/new-contact-alert.txt', {
                            'name': instance.name,
                            'email': instance.email,
                            'content': instance.content,
                            'date_posted': instance.date_posted,
                        })
    email_dict = {
        'receiver': receiver,
        'fail_silently': False,
        'subject': config.EMAIL_TEMPLATES['new-contact-alert']['subject'],
        'body': body,
    }
    send_email_out(email_dict)