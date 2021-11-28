from typing import ContextManager
from django import template
from django.http import HttpResponse
import datetime
from django.template import Template, Context, context
from django.template import loader
from django.shortcuts import render

import ProyectoMQTT

from ProyectoMQTT.mqtt import *
from ProyectoMQTT.weather import recogerDatos

def MQTT(request):

    return HttpResponse(ProyectoMQTT.mqtt.documento)

def subirPersiana(request):

    client.publish("esp32/persiana","up")

    return HttpResponse()

def bajarPersiana(request):

    client.publish("esp32/persiana","down")

    return HttpResponse()
    