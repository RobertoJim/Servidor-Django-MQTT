import json
import requests
from datetime import datetime

#Quiero comprobar si dentro de una hora va a llover, si va a llover recojo toldo
#Tendria que ejecutar esa funcion cada hora(funcion recogerdatos)
#Por ejemplo, a las 16:00 compruebo tiempo de las 17:00.... A las 17:00 compruebo tiempo 18:00

#Ademas, tendria que ejecutar la funcion recogerdatos y el sensor detecta agua para comprobar el viento


def recogerDatos():

    api_key = "6159431fde89157c2c7bb8ff8a7e841a"
    lat = "36.720969"
    lon = "-4.474427"

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)

    #current = data["current"]["pressure"]

    dt = data["minutely"][60]["dt"]
    hora = str(datetime.fromtimestamp(dt))[11:] #Convierto la fecha a formato conocido y elimino 11 primeros caracteres (elimino fecha) 
                                                #para obtener solo la hora
                                    
    #prevision = data["hourly"][1]["weather"][0]['description'] #Ejemplo, cielo despejado

    prevision = data["minutely"][60]["precipitation"]


    print("La prevision para las " + hora + " es " + str(prevision))


    #current = data["hourly"][0]["pressure"]
