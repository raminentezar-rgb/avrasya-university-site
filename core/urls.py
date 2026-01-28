from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('anasyafa/', views.anasyafa, name='anasyafa'),
    path('', views.index, name='index'),
   
    path('elements/', views.elements, name='elements'),
    path('avrasya_iletisim/', views.iletisim, name='iletisim'),
    path('test/', views.test, name='test'),
    path('set-language/', views.set_language, name='set_language'),



    path("asistan/", views.qa_search, name="qa_search"),

    
]


