from django.urls import path
from . import views

app_name = 'tuition'

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/<str:student_id>/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
]
