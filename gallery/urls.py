from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_main, name='main'),
    path('kategori/<slug:slug>/', views.gallery_category, name='category_detail'),
    path('fotograf/<int:image_id>/', views.gallery_detail, name='image_detail'),
]