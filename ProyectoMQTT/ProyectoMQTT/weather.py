import json
import requests

from time import sleep
import threading
import ProyectoMQTT
from ProyectoMQTT.mqtt import *
from suntime import Sun

velocidadViento = 0; rafagaViento = 0; precipitacion = 0 ; vientoMax = 0
mensajeViento = ""; api_key = ""; lat = ""; lon = ""


def openWeatherMap():

    conf()
    comprobarSalidaPuestaSol()
    thread = threading.Thread(target=recogerDatos, daemon=True) #Hilo demonio para que se elimine al finalizar el programa
    thread.start()
    


def recogerDatos():

    global velocidadViento; global rafagaViento; global precipitacion; global hora; global mensajeViento

    while 1:

        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
        response = requests.get(url)
        data = json.loads(response.text)

        dt = data["hourly"][1]["dt"]
        
        hora = str(datetime.fromtimestamp(dt))[11:]  #Convierto la fecha a formato conocido y elimino 11 primeros caracteres (elimino fecha) 
                                                    #para obtener solo la hora
        
        precipitacion = data["hourly"][1]["pop"]

        velocidadViento = data["hourly"][1]["wind_speed"] # Comprobando velocidad del viento en la siguiente hora
        rafagaViento = data["hourly"][1]["wind_gust"]


        if rafagaViento < vientoMax: #Guardo el mensaje para que aparezca en la alerta al pulsar el boton
            mensajeViento = "Subiendo toldo"           
        else:          
            mensajeViento = "Hace mucho viento, peligro de que se rompa el toldo"
            if(ProyectoMQTT.mqtt.estadoToldo == 1):
                client.publish("esp32/toldo","down")
                ProyectoMQTT.mqtt.bajaToldoViento = 1

        if ((precipitacion >= 15) and (ProyectoMQTT.mqtt.estadoToldo == 1)): #Bajo toldo si se espera precipitacion
            client.publish("esp32/toldo","down") #Cambio la variable estadoToldo en consumers.py, alli explicacion
            ProyectoMQTT.mqtt.bajaToldoLluvia = 1

        
        #Compruebo hora salida y puesta sol todos los dias a las 1 de la madrugada
        if(str(datetime.now(pytz.timezone('Europe/Madrid')))[11:][:-19] == "01"):
            comprobarSalidaPuestaSol()
            
        sleep(1800)

def comprobarViento():

    if rafagaViento < vientoMax:

        ProyectoMQTT.mqtt.estadoToldo = 1
        client.publish("esp32/toldo","up")


def comprobarSalidaPuestaSol():

    sun = Sun(float(lat),float(lon))

    ProyectoMQTT.mqtt.salidaSol = float(str(sun.get_local_sunrise_time())[11:][:-9].replace(':', '.')) #Cambio ':' por '.' para poder convertirlo en float y poder comparar con la hora actual en mqtt.py (LDR persiana)
    print("La hora de la salida del sol para el día " + str(sun.get_local_sunrise_time())[:-15] + " son las " + str(sun.get_local_sunrise_time())[11:][:-9])
    ProyectoMQTT.mqtt.puestaSol = float(str(sun.get_local_sunset_time())[11:][:-9].replace(':', '.'))
    print("La hora de la puesta del sol para el día " +  str(sun.get_local_sunset_time())[:-15] + " son las " + str(sun.get_local_sunset_time())[11:][:-9])

def conf():

    global vientoMax; global api_key; global lat; global lon

    f = open("conf.txt", "r")
    vientoMax = int(f.readline()[:-1])
    lat = f.readline()[:-1] #[:-1] para quitar \n
    lon = f.readline()[:-1] #[:-1] para quitar \n
    api_key = f.readline()
    f.close()
