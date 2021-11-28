import json
import requests
from datetime import datetime
from time import sleep

import threading

import ProyectoMQTT
from ProyectoMQTT.mqtt import *

#Quiero comprobar si dentro de una hora va a llover, si va a llover recojo toldo
#Tendria que ejecutar esa funcion cada hora(funcion recogerdatos)
#Por ejemplo, a las 16:00 compruebo tiempo de las 17:00.... A las 17:00 compruebo tiempo 18:00

#Ademas, tendria que ejecutar la funcion recogerdatos y el sensor detecta agua para comprobar el viento

api_key = "6159431fde89157c2c7bb8ff8a7e841a"
lat = "36.720969"
lon = "-4.474427"

velocidadViento = 0; rafagaViento = 0


def openWeatherMap():

    thread = threading.Thread(target=recogerDatos, daemon=True) #Hilo demonio para que finalice al pulsar Ctrl-C??
    thread.start()


def recogerDatos():

    global velocidadViento; global rafagaViento

    while 1:

        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
        response = requests.get(url)
        data = json.loads(response.text)


        #dt = data["minutely"][60]["dt"]
        dt = data["hourly"][1]["dt"]
        hora = str(datetime.fromtimestamp(dt))[11:] #Convierto la fecha a formato conocido y elimino 11 primeros caracteres (elimino fecha) 
                                                    #para obtener solo la hora
                                        
        #prevision = data["hourly"][1]["weather"][0]['description'] #Ejemplo, cielo despejado

        #precipitacion = data["minutely"][60]["precipitation"] #Prevision precipitacion para dentro de una hora desde el momento en el que se mira
        precipitacion = data["hourly"][1]["pop"]
        print("La prevision para las " + hora + " es " + str(precipitacion))

        velocidadViento = data["hourly"][1]["wind_speed"] # Estoy comprobando la velocidad del viento dentro de una hora, quizas seria mejor comprobar la actual
        rafagaViento = data["hourly"][1]["wind_gust"]

        if (velocidadViento < 5) or (rafagaViento < 8): #Guardo el mensaje para que aparezca en la alerta al pulsar el boton
            ProyectoMQTT.mqtt.mensaje5 = "Subiendo toldo"
        else:          
            ProyectoMQTT.mqtt.mensaje5 = "Hace mucho viento, peligro de que se rompa el toldo"

        print("La prevision de viento  para las " + hora + " es Velocidad:  " + str(velocidadViento) + " y Rafaga: " + str(rafagaViento))

        if precipitacion > 0:

            client.publish("esp32/toldo","down")

        #current = data["hourly"][0]["pressure"]

        sleep(1800)

def comprobarViento():

    if (velocidadViento < 5) or (rafagaViento < 8):
        client.publish("esp32/toldo","up")
    
       
