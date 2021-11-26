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

    
    
    #if ProyectoMQTT.mqtt.documento == "":
    #    ProyectoMQTT.mqtt.documento = "No se ha encontrado servidor MQTT" #Solo funciona cuando se arranca y no hay MQTT, si se han recibido datos antes
                                                                        # documento ya no es igual a """
   
    #client.publish("esp32/output","on")

        #if request.method == 'POST' and 'run_script' in request.POST:

    #client.publish("esp32/output","on")

    
    return HttpResponse(ProyectoMQTT.mqtt.documento)

def subirPersiana(request):

    client.publish("esp32/persiana","up")

    return HttpResponse()

def bajarPersiana(request):

    client.publish("esp32/persiana","down")

    return HttpResponse()
    