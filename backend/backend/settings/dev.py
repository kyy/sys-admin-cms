from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w6l!_e)mfbl-z$$8!8&ga+(#uqn@nz$u6!e5gc8%n81b=3ifbq"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

DJANGO_VITE = {
    'default': {
        'dev_mode': DEBUG,  # True в разработке, False в production
        'dev_server_protocol': 'http',
        'dev_server_host': 'localhost',
        'dev_server_port': 3000,  # Порт Vite dev server
    }
}