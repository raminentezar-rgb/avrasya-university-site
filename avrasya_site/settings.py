from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY, DEBUG, and ALLOWED_HOSTS are defined at the bottom of this file using environment variables.

INSTALLED_APPS = [
    'daphne',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',

    # local apps
    'core',
    'news',
    'contact',
    'duyurular',
    'etkinlikler',
    'aday_ogrenci',
    'akademik',
    'fakulteler',
    'enstituler',
    'yuksekokullari',
    'meslekyuksekokullari',
    'fen_edebiyat',
    'iktisadi_idari',
    'muhendislik_mimarlik',
    'saglik_bilimleri',
    'spor_bilimleri',
    'iletisim',
    'uygulamali_bilimler',
    'meslek_yuksekokulu',
    'saglik_hizmetleri_myo',
    'psikoloji',
    'ingiliz_dili_edebiyati',
    'turk_dili_edebiyati',
    'molekuler_biyoloji_genetik',
    'mutercim_tercumanlik',
    'bilgisayar_muhendisligi',
    'elektrik_elektronik_muhendisligi',
    'gida_muhendisligi',
    'harita_muhendisligi',
    'ic_mimarlik',
    'insaat_muhendisligi',
    'makine_muhendisligi',
    'mimarlik',
    'isletme',
    'isletme_ingilizce',
    'avrasya_universitesi_hakkinda',
    'siyaset_bilimi',
    'maliye',
    'uluslararasi_iliskiler',
    'avrasya_universitesi_yonetim',
    'beslenme_diyetetik',
    'cocuk_gelisimi',
    'ebelik',
    'ergoterapi',
    'fizyoterapi_rehabilitasyon',
    'hemsirelik',
    'kutuphane',
    'odyoloji',
    'saglik_yonetimi',
    'antrenorluk_egitimi',
    'egzersiz',
    'ogrenci_isleri',
    'spor_yoneticiligi',
    'rekreasyon',
    'yatay_gecis',
    'gallery',
    'yeni_medya_iletisim',
    'arastirma',
    'international',
    'erasmus',
    'lee',
    'support',
    'accounts',
    'gorsel_iletisim_tasarimi',
    'idari_birimler',
    'sks',
    'channels',
    'chat',
    'tuition',
    
    #MYO
    'adalet',
    'ascilik',
    'bilgisayar_programciligi',
    'bilisim_guvenligi',
    'dis_ticaret',
    'e_ticaret',
    'grafik_tasarimi',
    'halkla_iliskiler',
    'harita_kadastro',
    'ic_mekan',
    'insaat_teknolojisi',
    'lojistik_programi',
    'mimari_restorasyon',
    'mahkeme_buro',
    'moda_tasarimi',
    'otomotiv',
    'sivil_havacilik',
    'sosyal_guvenlik',
    'sosyal_hizmetler',
    'spor_yonetimi',
    'web_tasarimi',
    'sosyal_hizmet',
    
    # SHMYO
    'acil_durum',
    'agiz_dis',
    'ameliyathane',
    'anestezi',
    'diyaliz',
    'dis_protezi',
    'elektronorofizyoloji',
    'eczane',
    'fizyoterapi',
    'cocuk_gelisimi_programi',
    'ilk_acil_yardim',
    'is_sagligi_guvenligi',
    'is_ugrasi_terapisi',
    'odyometri',
    'optisyenlik',
    'ortopedik_protez',
    'patoloji_laboratuar',
    'radyoterapi',
    'saglik_kurumlari',
    'tibbi_goruntuleme',
    'tibbi_laboratuvar',

    #UBYO
    'yonetim_bilisim_sistemleri',
    'gastronomi_mutfak_sanatlari',
    
    

    
    
    
    

    
    # third-party
    'crispy_forms',
    'crispy_bootstrap5',
]









# تنظیمات crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'core.middleware.ForceTurkishMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'avrasya_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.languages',
            ],
        },
    },
]

WSGI_APPLICATION = 'avrasya_site.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'postgresql://postgres:{os.environ.get("DB_PASSWORD", "1136130@NaNa")}@127.0.0.1:5432/avrasya_db',
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# زبان‌های پشتیبانی شده
LANGUAGES = [
    ('tr', ('Turkish')),
    ('en', ('English')),
    ('fa', ('Persian')),
    ('ar', ('Arabic')),   # عربی
    ('ru', ('Russian')),  # روسی
    ('de', ('German')),   # آلمانی
]

# مسیر فایل‌های ترجمه
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# زبان‌های RTL (راست به چپ)
LANGUAGES_BIDI = ["ar", "fa", "he", "ur"]
# --- پایان بخش زبان‌ها ---












# --- تنظیمات دپلوی ---
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'avrasya.edu.tr,www.avrasya.edu.tr,localhost,127.0.0.1').split(',')
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOST_RENDER = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if ALLOWED_HOST_RENDER not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(ALLOWED_HOST_RENDER)

# --- Security Hardening ---
if not DEBUG:
    # SSL/HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Browser security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
# --- End Security Hardening ---

# استفاده از متغیر محیطی برای امنیت
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev')

# --- تنظیمات استاتیک ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# تنظیمات آپلود فایل
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ایمیل SMTP اختصاصی
SITE_URL = "https://www.avrasya.edu.tr"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'avu.web@avrasya.edu.tr'
# پسورد ایمیل را در سرور به صورت متغیر محیطی تعریف می‌کنیم
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Avu202561.*') 
DEFAULT_FROM_EMAIL = 'avu.web@avrasya.edu.tr'
SERVER_EMAIL = 'noreply@avrasya.edu.tr'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
PASSWORD_RESET_TIMEOUT = 3600

# Axes Configuration
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 hour
AXES_LOCKOUT_TEMPLATE = None # Can be a custom template
AXES_RESET_ON_SUCCESS = True
AXES_IP_GETTER = 'axes.helpers.get_ip'
AXES_PROXY_COUNT = 1



# CKEditor configuration
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join([
            'codesnippet',
            'youtube',
            'image2',
        ]),
    },
}


# Channels configuration
ASGI_APPLICATION = 'avrasya_site.asgi.application'

# Redis configuration for channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],
        },
    },
}



