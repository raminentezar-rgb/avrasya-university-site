from django.urls import path
from . import views

app_name = 'fakulteler'

urlpatterns = [
    path('', views.fakulteler, name='fakulteler'),
]