from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('', include('werkstatt.urls')),
]

handler404 = 'werkstatt.views.custom_page_not_found_view'
handler403 = 'werkstatt.views.custom_permission_denied_view'
handler400 = 'werkstatt.views.custom_bad_request_view'
handler500 = 'werkstatt.views.custom_error_view'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
