from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'avrasya_universitesi_hakkinda'

urlpatterns = [
    
    
    # URLهای صفحات استاتیک مدیریت کسب و کار انگلیسی
    path('', cache_page(60 * 60)(views.anasayfa), name='anasayfa'),
    path('felsefemiz', cache_page(60 * 60)(views.felsefemiz), name='felsefemiz'),
    path('misyon_vizyon/', cache_page(60 * 60)(views.misyon_vizyon), name='misyon_vizyon'),
    path('kurucu_vakif/', cache_page(60 * 60)(views.kurucu_vakif), name='kurucu_vakif'),
    path('akreditasyon/', cache_page(60 * 60)(views.akreditasyon), name='akreditasyon'),
    path('kalite_politikasi/', cache_page(60 * 60)(views.kalite_politikasi), name='kalite_politikasi'),
    path('tarihce/', cache_page(60 * 60)(views.tarihce), name='tarihce'),
    path('organizasyon_semasi/', cache_page(60 * 60)(views.organizasyon_semasi), name='organizasyon_semasi'),
    path('stratejik_plan/', cache_page(60 * 60)(views.stratejik_plan), name='stratejik_plan'),
   
]