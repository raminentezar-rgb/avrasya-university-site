from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'core'

urlpatterns = [
    path('home/', cache_page(60 * 5)(views.home), name='home'),
    path('anasyafa/', cache_page(60 * 60)(views.anasyafa), name='anasyafa'),
    path('', cache_page(60 * 5)(views.index), name='index'),
   
    path('elements/', views.elements, name='elements'),
    path('avrasya_iletisim/', cache_page(60 * 60)(views.iletisim), name='iletisim'),
    path('test/', views.test, name='test'),
    path('set-language/', views.set_language, name='set_language'),




    path("asistan/", views.qa_search, name="qa_search"),

    
]


