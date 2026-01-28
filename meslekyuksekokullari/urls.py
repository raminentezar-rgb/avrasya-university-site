from django.urls import path
from . import views

app_name = 'meslekyuksekokullari'

urlpatterns = [
    path('', views.meslekyuksekokullari, name='meslekyuksekokullari'),
]