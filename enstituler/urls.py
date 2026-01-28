from django.urls import path
from . import views

app_name = 'enstituler'

urlpatterns = [
    path('', views.enstituler, name='enstituler'),
]