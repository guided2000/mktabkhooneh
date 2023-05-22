from my_site.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s7-4_((!^+gd_91l-k6-kyatsmx!bq4e+n&w(5c201^y8h!*0s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# site framework
SITE_ID=1



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


MEDIA_ROOT =BASE_DIR/'media'
STATIC_ROOT =BASE_DIR/'static'
STATICFILES_DIRS = [
    BASE_DIR / "assets",
    
]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mahdi.yazdanpanah000@gmail.com'
EMAIL_HOST_PASSWORD = 'stifmtfuaxafiqgh'
EMAIL_PORT = 587


ESSION_COOKIE_SECURE=True