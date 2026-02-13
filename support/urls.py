# support/urls.py
from django.urls import path
from . import views  # این الان تمام ویوها رو از __init__.py میاره

app_name = 'support'

urlpatterns = [
    path('search/', views.support_search, name='search'),

    # Student
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('taleplerim/', views.my_tickets, name='my_tickets'),

    # Department
    path('department/dashboard/', views.department_dashboard, name='department_dashboard'),
    path('department/ticket/<int:ticket_id>/reply/', views.reply_ticket, name='reply_ticket'),

    # Staff
    path('staff/ticket/<int:ticket_id>/respond/', views.respond_ticket, name='respond_ticket'),

    # Ajax / API
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('api/categories/', views.load_categories, name='api_categories'),

    # FAQ
    path('faq/', views.faq_list_view, name='faq_list'),
    path('faq/<int:pk>/', views.faq_detail, name='faq_detail'),

    # Knowledge Base
    path('knowledge/<int:pk>/', views.knowledge_detail, name='knowledge_detail'),
]
