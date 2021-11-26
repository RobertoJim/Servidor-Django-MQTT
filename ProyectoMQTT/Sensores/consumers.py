import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import *

class SensoresConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        for i in range(1000):
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.temperatura}))
            print("La temperatura que me llega es:" + str(ProyectoMQTT.mqtt.temperatura))
            await sleep(6)
