from django.shortcuts import render, redirect
from django.utils.html import escape
from django.apps import apps
from django.http import Http404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from tuedo import config

def mail(request):
    if request.method == 'GET':
        if request.GET:
            method = request.GET.get('action')
            if method == 'confirm-subscription':
                Subscription = apps.get_model(app_label='werkstatt', model_name='Subscription')
                user_id = escape(request.GET.get('user-id'))
                hashcode = escape(request.GET.get('hash'))
                queryset = Subscription.objects.filter(pk=user_id).filter(subscribe_hash=hashcode)
                if queryset.exists():
                    user = queryset.first()
                    if user.active is True:
                        messages.warning(request, config.MESSAGE['subscribe_newsletter_warning'])
                    else:
                        user.active = True
                        user.save(update_fields=['active',])
                        messages.success(request, config.MESSAGE['subscribe_newsletter_success'])
                else:
                    raise Http404
            elif method == 'unsubscribe':
                Subscription = apps.get_model(app_label='werkstatt', model_name='Subscription')
                user_id = escape(request.GET.get('user-id'))
                hashcode = escape(request.GET.get('hash'))
                queryset = Subscription.objects.filter(pk=user_id).filter(unsubscribe_hash=hashcode)
                if queryset.exists():
                    user = queryset.first()
                    user.delete()
                    messages.warning(request, config.MESSAGE['unsubscribe_newsletter'])
                else:
                    raise Http404
            elif method == 'confirm-comment' or method == 'delete-comment':
                if request.user.is_staff is False:
                    raise PermissionDenied
                Comment = apps.get_model(app_label='werkstatt', model_name='Comment')
                comment_id = escape(request.GET.get('comment-id'))
                hashcode = escape(request.GET.get('hash'))
                queryset = Comment.objects.filter(pk=comment_id).filter(confirm_hash=hashcode)
                if queryset.exists():
                    comment = queryset.first()
                    if comment.active is True:
                        messages.warning(request, config.MESSAGE['confirm_comment_warning'])
                    else:
                        if method == 'delete-comment':
                            comment.delete()
                            messages.warning(request, config.MESSAGE['delete_comment'])
                        else:
                            comment.active = True
                            comment.confirm_hash = 'confirmed'
                            comment.save(update_fields=['active', 'confirm_hash',])
                            messages.success(request, config.MESSAGE['confirm_comment_success'])
                else:
                    raise Http404

        return redirect('index')
    
    else:
        raise Http404
