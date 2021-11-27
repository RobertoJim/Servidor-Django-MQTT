from django.urls import path

from .consumers import SensoresConsumer


ws_urlspatterns = [
    path('ws/Sensores/', SensoresConsumer.as_asgi())
]