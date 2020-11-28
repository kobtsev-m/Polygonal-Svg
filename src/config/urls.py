from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic.base import RedirectView


favicon_view = RedirectView.as_view(
    url='/static/svg/favicon.svg',
    permanent=True
)

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', favicon_view)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.extend([
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ])