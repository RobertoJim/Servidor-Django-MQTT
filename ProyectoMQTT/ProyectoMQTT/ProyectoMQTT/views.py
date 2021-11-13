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
    
    print("Me llega el mensaje de la temperatura:" + ProyectoMQTT.mqtt.mensaje1)
    print("Me llega el mensaje de la humedad:" + ProyectoMQTT.mqtt.mensaje2)

    documento = """<html>
    <body>
    <h2>
    La temperatura es: %s
    </h2>
    <h2>
    La humedad es: %s
    <h2/>
    </body>
    </html>""" %(ProyectoMQTT.mqtt.mensaje1, ProyectoMQTT.mqtt.mensaje2)
    

    return HttpResponse(documento)