from os import environ, path
from .common import *

SECRET_KEY = environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []
