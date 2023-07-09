from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:group__name>/', consumers.MySyncConsumer.as_asgi()), # give a different group name here, i have used group__name
    path('ws/ac/<str:group__name>/', consumers.MyAsyncConsumer.as_asgi()), # this group__name will be used to print in consumers.py
]