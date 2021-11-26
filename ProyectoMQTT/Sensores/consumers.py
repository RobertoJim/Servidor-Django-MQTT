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
        
        
        for i in range(1000):
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.temperatura, 'hora': (str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))}))
            #await self.send(json.dumps({'label': str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) }))
            print("Es la hora " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))
            await sleep(6)
