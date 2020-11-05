from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic.base import RedirectView


favicon_view = RedirectView.as_view(url='/static/img/favicon.svg', permanent=True)

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', favicon_view)
]