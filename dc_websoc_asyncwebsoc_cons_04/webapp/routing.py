from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/wsc/<str:group__name>/', consumers.MyWebsocketConsumer.as_asgi()),
    path('ws/awsc/<str:group__name>/', consumers.MyAsyncWebsocketConsumer.as_asgi()),
]