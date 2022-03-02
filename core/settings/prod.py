from os import environ, path
from .common import *
import dj_database_url as db_url

SECRET_KEY = environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ["pritdjango-blogapi.herokuapp.com"]

DATABASES = {
    'default': db_url.config()
}

# prod git: https://git.heroku.com/pritdjango-blogapi.git