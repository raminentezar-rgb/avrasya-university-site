from django.urls import path
from . import views

app_name = 'avrasya_universitesi_hakkinda'

urlpatterns = [
    
    
    # URLهای صفحات استاتیک مدیریت کسب و کار انگلیسی
    path('', views.anasayfa, name='anasayfa'),
    path('felsefemiz', views.felsefemiz, name='felsefemiz'),
    path('misyon_vizyon/', views.misyon_vizyon, name='misyon_vizyon'),
    path('kurucu_vakif/', views.kurucu_vakif, name='kurucu_vakif'),
    path('akreditasyon/', views.akreditasyon, name='akreditasyon'),
    path('kalite_politikasi/', views.kalite_politikasi, name='kalite_politikasi'),
    path('tarihce/', views.tarihce, name='tarihce'),
    path('organizasyon_semasi/', views.organizasyon_semasi, name='organizasyon_semasi'),
    path('stratejik_plan/', views.stratejik_plan, name='stratejik_plan'),
   
]