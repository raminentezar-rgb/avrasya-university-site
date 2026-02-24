from django.urls import path
from . import views

app_name = 'sks'

urlpatterns = [
    path('', views.sks, name='home'),
    
    # Haberler
    path('haberler/', views.news_list, name='news_list'),
    path('haber/<slug:slug>/', views.news_detail, name='news_detail'),
    path('kategori/<slug:category_slug>/', views.news_by_category, name='news_by_category'),
    
    # Duyurular
    path('duyurular/', views.announcements_list, name='announcements_list'),
    path('duyuru/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
]