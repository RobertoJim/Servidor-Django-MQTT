import paho.mqtt.client as mqtt
import json


from datetime import datetime

SensorJson={};temperatura="";humedad="";presion="";mensaje4=""; mensaje5 = ""

arrayTemperatura = ['', '', '', '', '', '', '', '', '', '', '', '']
arrayHora = ['', '', '', '', '', '', '', '', '', '', '', '']


#def comprobarLluvia():

    #Si la presion es mayor  a X(se esperan lluvias) o  sensor detecta agua, recojo toldo y muestro mensaje en pantalla
    
#def comprobarViento():

    #Si me llega peticion MQTT de extender toldo:

    # Compruebo si el viento es mayor a X, no dejo extender toldo y muestro en pagina mensaje

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt" + str(rc))
    client.subscribe("esp32/sensor")
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")
    client.subscribe("esp32/pressure")
    client.subscribe("esp32/LED")
    

def on_message(client, userdata, msg):

    global SensorJson; global mensaje4; global mensaje5; global temperatura; global humedad ; global presion
    
    global arrayTemperatura; global arrayHora
    
    if str(msg.topic) == "esp32/sensor":

        SensorJson = json.loads(msg.payload)
        temperatura = SensorJson['temperature']
        humedad = SensorJson['humidity']
        presion = SensorJson['pressure']

        #Monto array de temperatura y hora para la gráfica
        arrayTemperatura.pop(0) # Similar a shift en javascript 
        arrayTemperatura.append(temperatura) # Similar a push en javascript

        arrayHora.pop(0) # Similar a shift en javascript 
        arrayHora.append((str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))) # Similar a push en javascript
        #print("Esta es mi array de horas: " + str(arrayHora))



    if str(msg.topic) == "esp32/LED":
        mensaje4 = str(msg.payload)[2:][:-1] #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        #print(mensaje4)       
        #print(msg.topic+ " "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.36", 1883, 60)
#client.loop_start()
#client.loop_start()