from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-dev-key')

DEBUG = os.getenv('DEBUG') == 'True'



ALLOWED_HOSTS = ['*']

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












STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# فرمت‌های مجاز ویدیو (اختیاری)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

# فقط زمانی که DEBUG=False است از STATIC_ROOT استفاده کنید
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ایمیل SMTP اختصاصی
# settings.py

SITE_URL = "https://www.avrasya.edu.tr"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # یا smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'ramin.entezar@avrasya.edu.tr'
SERVER_EMAIL = 'noreply@avrasya.edu.tr'  # ایمیل برای خطاهای سیستم

LOGIN_REDIRECT_URL = '/'  # یا هر URL که بعد از لاگین میخوای

LOGOUT_REDIRECT_URL = '/'  

PASSWORD_RESET_TIMEOUT = 3600






