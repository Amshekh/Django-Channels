from django.urls import path
from .import consumers

websocket_urlpatterns = [
    path('ws/jwsc/<str:group__name>/', consumers.MyJsonWebsocketConsumer.as_asgi()),
    path('ws/ajwsc/<str:group__name>/', consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]