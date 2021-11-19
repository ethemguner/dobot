from django.urls import path
from dobot.consumers import MainWebSocketConsumer

ws_urlpatterns = [
    path("ws/main_consumer/<str:group_name>/", MainWebSocketConsumer.as_asgi())
]
