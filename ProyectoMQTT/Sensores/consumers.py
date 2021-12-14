import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

import ProyectoMQTT
from ProyectoMQTT.mqtt import arrayHora, arrayTemperatura, mensajeLed, temperatura, humedad, alertaBajarToldoLluvia, estadoPersiana, abrirPersiana,  mensajeLluvia, estadoToldo
from ProyectoMQTT.weather import precipitacion, velocidadViento, rafagaViento, hora

from datetime import datetime

class SensoresConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        
        while 1:
            
            await self.send(json.dumps({'value': ProyectoMQTT.mqtt.arrayTemperatura, 'hora': ProyectoMQTT.mqtt.arrayHora, 
            'bombilla': ProyectoMQTT.mqtt.mensajeLed, 'temperatura': ProyectoMQTT.mqtt.temperatura,  'humedad': ProyectoMQTT.mqtt.humedad,
            'lluvia': ProyectoMQTT.weather.precipitacion,'velocidadViento': ProyectoMQTT.weather.velocidadViento,'rafagaViento': ProyectoMQTT.weather.rafagaViento,
            'horaLluvia': ProyectoMQTT.weather.hora, 'estadoToldo' :ProyectoMQTT.mqtt.estadoToldo,
            'alertaToldo' :ProyectoMQTT.mqtt.alertaBajarToldoLluvia, 'mensajeLluvia' :ProyectoMQTT.mqtt.mensajeLluvia, 
            'abrirPersiana' : ProyectoMQTT.mqtt.abrirPersiana, 'estadoPersiana' : ProyectoMQTT.mqtt.estadoPersiana}))

            #print("Mi estado toldo ess" + str(ProyectoMQTT.mqtt.estadoToldo))
            #print("Mi alerta lluvia es " + str(ProyectoMQTT.mqtt.alertaBajarToldoLluvia))

            #print("Mi estado persiana es  " + str(ProyectoMQTT.mqtt.estadoPersiana))

            if(ProyectoMQTT.mqtt.alertaBajarToldoLluvia == 1):
                ProyectoMQTT.mqtt.alertaBajarToldoLluvia = 0
                ProyectoMQTT.mqtt.estadoToldo = 0 #Cambio el estado aqui en vez de en weather para que ambas variables cambien a la vez
                                                    #Si cambiaba el estado en weather, nunca llegaban a estar ambas a 1

            #print("mi estado toldo es: " + str(ProyectoMQTT.mqtt.estadoToldo))
            #print("mi mensaje lluvia es: " + str(ProyectoMQTT.mqtt.mensajeLluvia))
            if(ProyectoMQTT.mqtt.mensajeLluvia == 1):
                
                ProyectoMQTT.mqtt.mensajeLluvia = 0
                ProyectoMQTT.mqtt.estadoToldo = 0 #Cambio el estado aqui en vez de en weather para que ambas variables cambien a la vez
                                                    #Si cambiaba el estado en weather, nunca llegaban a estar ambas a 1

            #print("Abrir persiana " + str(ProyectoMQTT.mqtt.abrirPersiana))
            if(ProyectoMQTT.mqtt.abrirPersiana == 1):
                ProyectoMQTT.mqtt.abrirPersiana = 0
                



            #await self.send(json.dumps({'label': str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) }))
            #print("Es la hora " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))
            #print("El array que me llega a CONSUMER es: " + str(ProyectoMQTT.mqtt.arrayTemperatura))
            #print("Mi mensaje bombilla es: " + str(ProyectoMQTT.mqtt.mensajeLed))
            #await self.send(json.dumps({'bombilla': ProyectoMQTT.mqtt.mensajeLed}))
            await sleep(1)

