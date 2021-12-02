import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import arrayHora, arrayTemperatura, mensajeLed, temperatura, humedad
from ProyectoMQTT.weather import precipitacion, velocidadViento, rafagaViento, hora

from datetime import datetime

class SensoresConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        while 1:
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.arrayTemperatura, 'hora': ProyectoMQTT.mqtt.arrayHora, 
            'bombilla': ProyectoMQTT.mqtt.mensajeLed, 'temperatura': ProyectoMQTT.mqtt.temperatura,  'humedad': ProyectoMQTT.mqtt.humedad,
            'lluvia': ProyectoMQTT.weather.precipitacion,'velocidadViento': ProyectoMQTT.weather.velocidadViento,'rafagaViento': ProyectoMQTT.weather.rafagaViento,
            'horaLluvia': ProyectoMQTT.weather.hora}))
            #await self.send(json.dumps({'label': str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) }))
            #print("Es la hora " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))
            #print("El array que me llega a CONSUMER es: " + str(ProyectoMQTT.mqtt.arrayTemperatura))
            #print("Mi mensaje bombilla es: " + str(ProyectoMQTT.mqtt.mensajeLed))
            #await self.send(json.dumps({'bombilla': ProyectoMQTT.mqtt.mensajeLed}))
            await sleep(1)

