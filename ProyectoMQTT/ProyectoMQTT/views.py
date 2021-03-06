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

def subirToldo(request):

    comprobarViento()
    return HttpResponse()

def bajarToldo(request):

    ProyectoMQTT.mqtt.estadoToldo = 0
    client.publish("esp32/toldo","down")  
    return HttpResponse()


def Persiana1(request):

    client.publish("esp32/persiana", "1")
    ProyectoMQTT.mqtt.estadoPersiana = 1
    return HttpResponse()

def Persiana2(request):

    client.publish("esp32/persiana", "2")
    ProyectoMQTT.mqtt.estadoPersiana = 2
    return HttpResponse()

def Persiana3(request):

    client.publish("esp32/persiana", "3")
    ProyectoMQTT.mqtt.estadoPersiana = 3
    return HttpResponse()

def Persiana4(request):

    client.publish("esp32/persiana", "4")
    ProyectoMQTT.mqtt.estadoPersiana = 4
    return HttpResponse()

def Persiana5(request):

    client.publish("esp32/persiana", "5")
    ProyectoMQTT.mqtt.estadoPersiana = 5
    return HttpResponse()

def deshabilitar(request):

    ProyectoMQTT.mqtt.persianaAutomatica = 0
    return HttpResponse()

def habilitar(request):

    ProyectoMQTT.mqtt.persianaAutomatica = 1
    return HttpResponse()
