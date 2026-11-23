from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('home/', RedirectView.as_view(pattern_name='core:index', permanent=True), name='home'),
    path('anasyafa/', RedirectView.as_view(pattern_name='core:index', permanent=True), name='anasyafa'),
    path('', views.index, name='index'),
    path('avrasya_iletisim/', views.iletisim, name='iletisim'),
    path('set-language/', views.set_language, name='set_language'),
    path("asistan/", views.qa_search, name="qa_search"),
]


