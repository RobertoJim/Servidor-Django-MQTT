from typing import ContextManager
from django import template
from django.http import HttpResponse
import datetime
from django.template import Template, Context, context
from django.template import loader
from django.shortcuts import render

import ProyectoMQTT

from ProyectoMQTT.mqtt import *
from ProyectoMQTT.weather import comprobarViento,  mensajeViento, estadoToldo


def MQTT(request):
  
    return render(request, 'inicio.html', context={'bombilla': ProyectoMQTT.mqtt.mensajeLed,
      'mensajeViento' : ProyectoMQTT.weather.mensajeViento})


def potencia(request):
    return render(request, 'potencia.html')
