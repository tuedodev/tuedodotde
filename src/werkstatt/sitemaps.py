from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from werkstatt.models import BlogPost
from .utils import filterBlogs
from tuedo import settings

class BlogPostSitemap(Sitemap):

    protocol = settings.META_SITE_PROTOCOL
    changefreq = 'daily'

    def items(self):
        queryset = BlogPost.objects.exclude(draft=True)
        return queryset
    
    def lastmod(self, obj):
        return obj.date_posted

    def priority(self, obj):
        return 1.0 if obj.featured else 0.5 

class StaticViewSitemap(Sitemap):
    
    protocol = settings.META_SITE_PROTOCOL
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index', 'datenschutz', 'referenzen', 'about', 'impressum', 'kontakt', 'werkstatt']

    def location(self, item):
        return reverse(item)