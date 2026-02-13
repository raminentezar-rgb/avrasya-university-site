from django.urls import path
from . import views

app_name = 'akademik'  # این خط باید وجود داشته باشد

urlpatterns = [
    path('', views.academic_page, name='akademik'),
    # سایر مسیرها...
]