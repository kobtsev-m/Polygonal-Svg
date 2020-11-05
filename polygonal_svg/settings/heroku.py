from settings.base import *

import dj_database_url
import django_heroku
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['pure-oasis-09000.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

django_heroku.settings(locals())