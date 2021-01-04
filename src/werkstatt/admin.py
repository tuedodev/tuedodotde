from django.contrib import admin
from . import models
from werkstatt.models import Comment

class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('tuedo_number', 'language', 'title', 'featured', 'featured_position', 'date_posted', 'draft')
    list_display_links = ('tuedo_number', 'title', 'date_posted')

admin.site.register(models.BlogPost, BlogPostAdmin)
admin.site.register(models.Contact)
admin.site.register(models.Author)
admin.site.register(models.Category)

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment_body_short', 'blogpost_short', 'date_posted', 'active')
    list_filter = ('active', 'date_posted')
    search_fields = ('name', 'email', 'comment_body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reply":
            try:
                comment_id = request.META['PATH_INFO'].rstrip('/').split('/')[-2]
                kwargs["queryset"] = Comment.objects.get(pk=comment_id).blogpost.comments.filter(active=True).filter(reply__isnull=True)
            except:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_email', 'date_joined')

@admin.register(models.Sitecontent)
class SitecontentAdmin(admin.ModelAdmin):
    list_display = ('site', 'header', 'position', 'content')