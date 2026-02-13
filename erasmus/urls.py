from django.urls import path
from . import views

app_name = 'erasmus' 

urlpatterns = [
    path('', views.erasmus, name='erasmus'),
    
]