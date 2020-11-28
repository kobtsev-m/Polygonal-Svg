from django.urls import path
from main.views import HomePage

app_name = 'main'
urlpatterns = [
    path('', HomePage.as_view(), name='home')
]