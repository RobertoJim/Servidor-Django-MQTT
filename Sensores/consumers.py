import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import *

from datetime import datetime

class SensoresConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        while 1:
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.arrayTemperatura, 'hora': ProyectoMQTT.mqtt.arrayHora}))
            #await self.send(json.dumps({'label': str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) }))
            #print("Es la hora " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))
            #print("El array que me llega a CONSUMER es: " + str(ProyectoMQTT.mqtt.arrayTemperatura))
            await sleep(5)
