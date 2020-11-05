from settings.base import *

import dj_database_url
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['']

DATABASES = {
    'default': dj_database_url(default=os.environ.get('DATABASE_URL'))
}