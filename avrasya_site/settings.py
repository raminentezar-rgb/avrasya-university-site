from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY, DEBUG, and ALLOWED_HOSTS are defined at the bottom of this file using environment variables.

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

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
    'core.middleware.ForceTurkishMiddleware',  # اضافه کردن این خط
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'core.context_processors.languages',
            ],
        },
    },
]

WSGI_APPLICATION = 'avrasya_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# استفاده از متغیر محیطی برای امنیت
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev')

# --- تنظیمات استاتیک ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # این پوشه برای دپلوی حیاتی است

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
EMAIL_HOST_USER = 'ramin.entezar@avrasya.edu.tr'
# پسورد ایمیل را در سرور به صورت متغیر محیطی تعریف می‌کنیم
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '1136130@NaNa') 
DEFAULT_FROM_EMAIL = 'ramin.entezar@avrasya.edu.tr'
SERVER_EMAIL = 'noreply@avrasya.edu.tr'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
PASSWORD_RESET_TIMEOUT = 3600






