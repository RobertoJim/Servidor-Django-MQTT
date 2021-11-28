from typing import ContextManager
from django import template
from django.http import HttpResponse
import datetime
from django.template import Template, Context, context
from django.template import loader
from django.shortcuts import render

import ProyectoMQTT

from ProyectoMQTT.mqtt import *
from ProyectoMQTT.weather import comprobarViento

def MQTT(request):
    
    return render(request, 'inicio.html', context={'temperatura' : ProyectoMQTT.mqtt.temperatura, 'humedad' : ProyectoMQTT.mqtt.humedad, 'presion' : ProyectoMQTT.mqtt.presion, 'toldo' : ProyectoMQTT.mqtt.mensaje5})


def subirPersiana(request):

    client.publish("esp32/persiana","up")

    return HttpResponse()

def bajarPersiana(request):

    client.publish("esp32/persiana","down")

    return HttpResponse()

def subirToldo(request):

    comprobarViento()
    #client.publish("esp32/toldo","up")

    return HttpResponse()

def bajarToldo(request):

    client.publish("esp32/toldo","down")

    return HttpResponse()
    