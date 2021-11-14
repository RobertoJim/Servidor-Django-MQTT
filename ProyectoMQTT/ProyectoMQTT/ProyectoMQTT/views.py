from typing import ContextManager
from django import template
from django.http import HttpResponse
import datetime
from django.template import Template, Context, context
from django.template import loader
from django.shortcuts import render
import ProyectoMQTT

from ProyectoMQTT.mqtt import *


def MQTT(request):
    
    #print("Me llega el mensaje de la temperatura:" + ProyectoMQTT.mqtt.mensaje1)
    #print("Me llega el mensaje de la humedad:" + ProyectoMQTT.mqtt.mensaje2)

   
    #client.publish("esp32/output","on")

    return HttpResponse(ProyectoMQTT.mqtt.documento)