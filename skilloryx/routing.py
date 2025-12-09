from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video_call/<str:room_name>/', consumers.VideoCallConsumer.as_asgi()),
    path('ws/notifications/<str:username>/', consumers.NotificationConsumer.as_asgi()),
]
