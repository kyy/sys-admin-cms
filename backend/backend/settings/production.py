import re

from .base import *

DEBUG = False
SECRET_KEY = "django-insecure-w6l!_e)mfbl-z$$8!8&ga+(#uqn@nz$u6!e5gc8%n81b=3ifbq"
# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage


MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
CSRF_ALLOWED_ORIGINS = [
    'http://127.0.0.1/',
    'http://localhost/',
]
DJANGO_VITE = {
    'default': {
        'dev_mode': DEBUG,  # True в разработке, False в production
        'manifest_path': os.path.join(BASE_DIR, 'static/manifest.json'),
        'static_url_prefix': '',
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
SERVE_MEDIA = True
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]
try:
    from .local import *
except ImportError:
    pass