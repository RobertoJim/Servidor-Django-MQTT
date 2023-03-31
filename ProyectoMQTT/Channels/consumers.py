import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import arrayHora, arrayTemperatura, mensajeLed, temperatura, humedad, alertaBajarToldoLluvia, alertaBajarToldoViento, estadoPersiana, abrirPersiana,  mensajeLluvia, estadoToldo ,persianaAutomatica
from ProyectoMQTT.weather import precipitacion, velocidadViento, rafagaViento, hora
from ProyectoMQTT.ccm2w import arrayPotencia, arrayHoraPotencia

from datetime import datetime

class ChannelsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        while 1:
            
            await self.send(
                json.dumps({
                    'value' : ProyectoMQTT.mqtt.arrayTemperatura, 'hora': ProyectoMQTT.mqtt.arrayHora,
                    'potencia': ProyectoMQTT.ccm2w.arrayPotencia, 'arrayHoraPotencia' : ProyectoMQTT.ccm2w.arrayHoraPotencia,
                    'temperatura': ProyectoMQTT.mqtt.temperatura,  'humedad': ProyectoMQTT.mqtt.humedad, 'co2' : ProyectoMQTT.mqtt.CO2
                    })
            )

            await sleep(1)

