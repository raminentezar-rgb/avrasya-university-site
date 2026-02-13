from django.urls import path
from . import views


app_name = 'international'



urlpatterns = [
    path('',views.international,name='international'),
    path('campus_life/',views.campus_life,name='campus_life'),
    path('city_of_trabzon/',views.city_of_trabzon,name='city_of_trabzon'),
    path('application/',views.application,name='application'),
    path('academic_enviorment/',views.academic_enviorment,name='academic_enviorment'),
    path('programers/',views.programers,name='programers'),
    path('application_form/',views.application_form,name='application_form'),



    
]
