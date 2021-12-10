import json
import requests
from datetime import date, datetime
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


velocidadViento = 0; rafagaViento = 0; precipitacion = 0 #Cuando arranca el sistema el toldo esta cerrado
mensajeViento = ""


def openWeatherMap():

    thread = threading.Thread(target=recogerDatos, daemon=True) #Hilo demonio para que finalice al pulsar Ctrl-C??
    thread.start()
    


def recogerDatos():

    global velocidadViento; global rafagaViento; global precipitacion; global hora; global mensajeViento

    while 1:

        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
        response = requests.get(url)
        data = json.loads(response.text)


        #dt = data["minutely"][60]["dt"]
        dt = data["hourly"][1]["dt"]
        
        hora = str(datetime.fromtimestamp(dt))[11:]  #Convierto la fecha a formato conocido y elimino 11 primeros caracteres (elimino fecha) 
                                                    #para obtener solo la hora
        
        #prevision = data["hourly"][1]["weather"][0]['description'] #Ejemplo, cielo despejado

        #precipitacion = data["minutely"][60]["precipitation"] #Prevision precipitacion para dentro de una hora desde el momento en el que se mira
        precipitacion = data["hourly"][1]["pop"]
       # precipitacion=1
        print("La prevision para las " + hora + " es " + str(precipitacion))

        velocidadViento = data["hourly"][1]["wind_speed"] # Estoy comprobando la velocidad del viento dentro de una hora, quizas seria mejor comprobar la actual
        rafagaViento = data["hourly"][1]["wind_gust"]

        if (velocidadViento < 7) and (rafagaViento < 12): #Guardo el mensaje para que aparezca en la alerta al pulsar el boton
            mensajeViento = "Subiendo toldo"
            
        else:          
            mensajeViento = "Hace mucho viento, peligro de que se rompa el toldo"

        print("La prevision de viento  para las " + hora + " es Velocidad:  " + str(velocidadViento) + " y Rafaga: " + str(rafagaViento))
        
        
        #Precipitacion es el dato que obtengo de OpenWeatherMap
        if ((precipitacion > 0) and (ProyectoMQTT.mqtt.estadoToldo == 1)): #Esta condicion creo que no deberia estar aqui, ya que al empezar la aplicacion
                                                        #estado estadoToldo nunca va estar a 1 y no se va a ejecutar
            client.publish("esp32/toldo","down") #Cambio la variable estadoToldo en consumers.py, alli explicacion
            ##estadoToldo = 0
            ProyectoMQTT.mqtt.bajaToldoLluvia = 1 #Quizas pueda ahorrarme esta variable utilizando la variable precipitacion
            

        #current = data["hourly"][0]["pressure"]
        

        sleep(18)

def comprobarViento():



    if (velocidadViento < 7) and (rafagaViento < 12):

        ProyectoMQTT.mqtt.estadoToldo = 1
        print("He entrado donde deberia de cambiar estado toldo")
        client.publish("esp32/toldo","up")


def comprobarMes():
    #Mirar como hacr para descargar horario


    if(date.today().month == 1):

       ProyectoMQTT.mqtt.salidaSol = 8.20
       ProyectoMQTT.mqtt.puestaSol = 18.40
    elif(date.today().month == 2):
        ProyectoMQTT.mqtt.salidaSol = 7.50
        ProyectoMQTT.mqtt.puestaSol = 19.10
    elif(date.today().month == 3):  #En marzo cambia a horario verano, habria que comprobar tambien el dia que es, ya que la hora cambia
        ProyectoMQTT.mqtt.salidaSol = 7.50
        ProyectoMQTT.mqtt.puestaSol = 20.40
    elif(date.today().month == 4):
        ProyectoMQTT.mqtt.salidaSol = 7.25
        ProyectoMQTT.mqtt.puestaSol = 21.05
    elif(date.today().month == 5):
        ProyectoMQTT.mqtt.salidaSol = 7.00
        ProyectoMQTT.mqtt.puestaSol = 21.30
    elif(date.today().month == 6):
        ProyectoMQTT.mqtt.salidaSol = 7.00
        ProyectoMQTT.mqtt.puestaSol = 21.40
    elif(date.today().month == 7):
        ProyectoMQTT.mqtt.salidaSol = 7.03
        ProyectoMQTT.mqtt.puestaSol = 21.40
    elif(date.today().month == 8):
        ProyectoMQTT.mqtt.salidaSol = 7.24
        ProyectoMQTT.mqtt.puestaSol = 21.25
    elif(date.today().month == 9):
        ProyectoMQTT.mqtt.salidaSol = 7.50
        ProyectoMQTT.mqtt.puestaSol = 20.46
    elif(date.today().month == 10): #Aqui vuelvo a cambiar el horario
        ProyectoMQTT.mqtt.salidaSol = 7.40
        ProyectoMQTT.mqtt.puestaSol = 20.00
    elif(date.today().month == 11):
        ProyectoMQTT.mqtt.salidaSol = 7.41
        ProyectoMQTT.mqtt.puestaSol = 18.21
    elif(date.today().month == 12):
        ProyectoMQTT.mqtt.salidaSol = 8.12
        ProyectoMQTT.mqtt.puestaSol = 18.12
    
    print("En el mes " + str(date.today().month) + " SALIDA : " + str(ProyectoMQTT.mqtt.salidaSol) + " y PUESTA: " + str(ProyectoMQTT.mqtt.puestaSol))






#def bajarToldo():

    #ProyectoMQTT.mqtt.estadoToldo = 0
    #client.publish("esp32/toldo","down")        
    
       
