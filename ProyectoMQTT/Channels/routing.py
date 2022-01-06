from django.urls import path

from .consumers import ChannelsConsumer


ws_urlspatterns = [
    path('ws/Channels/', ChannelsConsumer.as_asgi())
]