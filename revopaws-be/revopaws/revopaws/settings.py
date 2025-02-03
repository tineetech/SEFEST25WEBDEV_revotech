from pathlib import Path
import os
from decouple import config
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    
    'django_cleanup.apps.CleanupConfig',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.revoshop',
    'apps.artikel',
    'apps.payments',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'revopaws.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'revopaws.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='property_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': '',
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

AUTH_USER_MODEL = 'users.CustomUser'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'   
MEDIA_ROOT = BASE_DIR / 'media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def is_group_member(request, group_name):
    """ Helper untuk mengecek apakah user adalah anggota dari group tertentu """
    return request.user.groups.filter(name=group_name).exists()


UNFOLD = {
    "SITE_TITLE": "Revopaws",
    "SITE_HEADER": "Revopaws Admin",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigasi Utama"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        # "permission": lambda request: request.user.is_superuser,  # Hanya superuser yang bisa akses
                    },
                ],
            },
            {
                "title": _("RevoShop"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Data Barang"),
                        "icon": "shopping_basket",
                        "link": reverse_lazy("admin:revoshop_product_changelist"),
                        # "permission": lambda request: is_group_member(request, 'seller'),
                    },
                    {
                        "title": _("Kategori Barang"),
                        "icon": "category",
                        "link": reverse_lazy("admin:revoshop_productcategory_changelist"),
                        # "permission": lambda request: is_group_member(request, 'seller'),
                    },
                    {
                        "title": _("Pesanan"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:revoshop_productcategory_changelist"),
                        # "permission": lambda request: is_group_member(request, 'seller'),
                    },
                ],
            },
            {
                "title": _("Artikel"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Data Artikel"),
                        "icon": "shopping_basket",
                        "link": reverse_lazy("admin:artikel_artikel_changelist"),
                        # "permission": lambda request: is_group_member(request, 'seller'),
                    },
                    {
                        "title": _("Kategori Artikel"),
                        "icon": "category",
                        "link": reverse_lazy("admin:artikel_artikelcategory_changelist"),
                        # "permission": lambda request: is_group_member(request, 'seller'),
                    },
                ],
            },
            {
                "title": _("Pembayaran"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Opsi Pembayaran"),
                        "icon": "credit_card",
                        "link": reverse_lazy("admin:payments_paymentoption_changelist"),
                        # "permission": lambda request: is_group_member(request, 'admin') or is_group_member(request, 'petugas'),
                    },
                ],
            },
            {
                "title": _("Manajemen Pengguna"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Pengguna"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_customuser_changelist"),
                        # "permission": lambda request: is_group_member(request, 'admin') or is_group_member(request, 'petugas'),
                    },
                    {
                        "title": _("Role"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    }
}

