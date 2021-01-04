from django.conf import settings
from django.urls import path, re_path

from . import views
from .sitemaps import BlogPostSitemap, StaticViewSitemap
from mail import views as mailviews
from django.contrib.sitemaps.views import sitemap

sitemaps = {
        'static': StaticViewSitemap,
        'blogposts': BlogPostSitemap,
}

urlpatterns = [path('', views.index, name='index'),
        re_path(r'^robots.txt$', views.robots_txt),
        re_path(r'^sitemap.xml$', sitemap, { 'sitemaps': sitemaps }),
        re_path(r'validate_form/$', views.validate_form,
                name='check_form'),
        re_path(r'process_form/$', views.process_form,
                name='check_form'),
        path('mail/', mailviews.mail, name='mail'),
        path('datenschutz/', views.DatenschutzView.as_view(), name='datenschutz'),
        path('referenzen/', views.ReferencesView.as_view(), name='referenzen'),
        path('about/', views.AboutView.as_view(), name='about'),
        path('impressum/', views.ImpressumView.as_view(), name='impressum'),
        path('kontakt/', views.KontaktView.as_view(), name='kontakt'),
        path('werkstatt/', views.WerkstattView.as_view(), name='werkstatt'),
        path('search/', views.SearchView.as_view(), name='search'),
        path('get_captcha_image/', views.get_captcha_image, name='get_captcha_image'),
        path('check_captcha/', views.check_captcha, name='check_captcha'),
        path('<slug:blog_slug>/', views.blogpost, name='blogpost'),
        path('<slug:language_slug>/<slug:blog_slug>/',
                views.blogpost, name='blogpost'),
]
