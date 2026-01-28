from django.urls import path
from . import views

app_name = 'yuksekokullari'

urlpatterns = [
    path('', views.yuksekokullari, name='yuksekokullari'),
]