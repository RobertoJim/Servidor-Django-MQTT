"""ProyectoMQTT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ProyectoMQTT.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MQTT),
    path('subirToldo', subirToldo),
    path('bajarToldo', bajarToldo),
    path('Persiana1', Persiana1),
    path('Persiana2', Persiana2),
    path('Persiana3', Persiana3),
    path('Persiana4', Persiana4),
    path('Persiana5', Persiana5),
    path('deshabilitar', deshabilitar),
    path('habilitar', habilitar),
]
