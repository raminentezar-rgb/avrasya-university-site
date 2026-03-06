from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'chat'

urlpatterns = [
    # صفحه اصلی چت
    path('', views.chat_index, name='index'),
    
    # دریافت پیام‌های یک تاپیک
    path('thread/<int:thread_id>/messages/', views.thread_messages, name='thread_messages'),
    
    # ارسال پیام جدید
    path('send/', views.send_message, name='send_message'),
    
    # شروع مکالمه جدید
    path('start/', views.start_thread, name='start_thread'),
    
    # ویرایش پروفایل
    path('profile/', views.edit_profile, name='edit_profile'),
    
    # نشانه‌گذاری پیام‌ها به عنوان خوانده شده
    path('mark-read/', views.mark_as_read, name='mark_read'),
    
    # حذف مکالمه
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    
    # جستجوی کاربران
    path('search-users/', views.search_users, name='search_users'),
]

# اضافه کردن مسیر فایل‌های مدیا در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)