from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fp(3w=ugr60jtkhc)6yo+=nx5naev%&grc&1s!r=1+^3gqax8g'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
