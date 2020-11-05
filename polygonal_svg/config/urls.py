from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from django.views.generic.base import RedirectView
from django.urls import path, re_path, include


favicon_view = RedirectView.as_view(url='/static/img/favicon.svg', permanent=True)

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', favicon_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)