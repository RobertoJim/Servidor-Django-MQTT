import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import arrayHora, arrayTemperatura, mensajeLed, temperatura, humedad, alertaBajarToldoLluvia, alertaBajarToldoViento, estadoPersiana, abrirPersiana,  mensajeLluvia, estadoToldo ,persianaAutomatica
from ProyectoMQTT.weather import precipitacion, velocidadViento, rafagaViento, hora

from datetime import datetime

class ChannelsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        while 1:
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.arrayTemperatura, 'hora': ProyectoMQTT.mqtt.arrayHora, 
            'bombilla': ProyectoMQTT.mqtt.mensajeLed, 'temperatura': ProyectoMQTT.mqtt.temperatura,  'humedad': ProyectoMQTT.mqtt.humedad, 'co2' : ProyectoMQTT.mqtt.CO2,
            'lluvia': ProyectoMQTT.weather.precipitacion,'velocidadViento': ProyectoMQTT.weather.velocidadViento,'rafagaViento': ProyectoMQTT.weather.rafagaViento,
            'horaLluvia': ProyectoMQTT.weather.hora, 'estadoToldo' :ProyectoMQTT.mqtt.estadoToldo,
            'alertaToldoLluvia' :ProyectoMQTT.mqtt.alertaBajarToldoLluvia, 'mensajeLluvia' :ProyectoMQTT.mqtt.mensajeLluvia, 
            'abrirPersiana' : ProyectoMQTT.mqtt.abrirPersiana, 'estadoPersiana' : ProyectoMQTT.mqtt.estadoPersiana,
            'persianaAutomatica': ProyectoMQTT.mqtt.persianaAutomatica,'alertaToldoViento': ProyectoMQTT.mqtt.alertaBajarToldoViento}))


            #print("AlertaBajoLLvuia " + str(ProyectoMQTT.mqtt.alertaBajarToldoLluvia))
            #print("El estado toldo es " + str(ProyectoMQTT.mqtt.estadoToldo))

            if(ProyectoMQTT.mqtt.alertaBajarToldoLluvia == 1):
                ProyectoMQTT.mqtt.alertaBajarToldoLluvia = 0
                ProyectoMQTT.mqtt.estadoToldo = 0 #Cambio el estado aqui en vez de en weather para que ambas variables cambien a la vez
                                                    #Si cambiaba el estado en weather, nunca llegaban a estar ambas a 1
         
            #print("AlertaBajoViento " + str(ProyectoMQTT.mqtt.alertaBajarToldoViento))
            #print("El estado toldo es " + str(ProyectoMQTT.mqtt.estadoToldo))

            if(ProyectoMQTT.mqtt.alertaBajarToldoViento == 1):
                ProyectoMQTT.mqtt.alertaBajarToldoViento = 0
                ProyectoMQTT.mqtt.estadoToldo = 0

            if(ProyectoMQTT.mqtt.mensajeLluvia == 1):        
                ProyectoMQTT.mqtt.mensajeLluvia = 0
                ProyectoMQTT.mqtt.estadoToldo = 0 #Cambio el estado aqui en vez de en weather para que ambas variables cambien a la vez
                                                    #Si cambiaba el estado en weather, nunca llegaban a estar ambas a 1
           # print("mensajelluvia " + str(ProyectoMQTT.mqtt.mensajeLluvia))
            if(ProyectoMQTT.mqtt.abrirPersiana == 1):
                ProyectoMQTT.mqtt.abrirPersiana = 0

            await sleep(1)

