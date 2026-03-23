# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<thread_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/support/(?P<session_key>\w+)/$', consumers.SupportConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]