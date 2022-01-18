import paho.mqtt.client as mqtt
import json
import socket

from datetime import datetime
import pytz


SensorJson={};temperatura="";humedad=""; CO2="";mensajeLed=""; bajaToldoViento = 0; alertaBajarToldoViento = 0; bajaToldoLluvia = 0; alertaBajarToldoLluvia = 0; estadoToldo = 0
mensajeLluvia= 0

arrayTemperatura = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
arrayHora = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

puestaSol = 0 ; salidaSol = 0; abrirPersiana = 0; estadoPersiana = 1; persianaAutomatica = 1


#def comprobarLluvia():

    #Si la presion es mayor  a X(se esperan lluvias) o  sensor detecta agua, recojo toldo y muestro mensaje en pantalla
    
#def comprobarViento():

    #Si me llega peticion MQTT de extender toldo:

    # Compruebo si el viento es mayor a X, no dejo extender toldo y muestro en pagina mensaje

def on_connect(client, userdata, flags, rc):
    client.subscribe("esp32/sensor")
    client.subscribe("esp32/LED")
    client.subscribe("esp32/toldo")
    client.subscribe("esp32/lluvia")
    client.subscribe("esp32/LDR_persiana")
    client.subscribe("esp32/estados")
    client.subscribe("esp32/grafica")
    
    

def on_message(client, userdata, msg):

    global SensorJson; global mensajeLed; global temperatura; global humedad ; global CO2
    global bajaToldoLluvia; global alertaBajarToldoLluvia; global mensajeLluvia; global bajaToldoViento; global alertaBajarToldoViento
    global estadoPersiana; global estadoToldo
    
    global arrayTemperatura; global arrayHora

    global salidaSol; global puestaSol; global abrirPersiana
    
    if str(msg.topic) == "esp32/sensor":

        SensorJson = json.loads(msg.payload)
        temperatura = SensorJson['temperature']
        humedad = SensorJson['humidity']
        CO2 = SensorJson['co2']

    if str(msg.topic) == "esp32/LED":
        mensajeLed = str(msg.payload)[2:][:-1] #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print("Mi mensaje led es: " + mensajeLed)
        #print(mensaje4)       
        #print(msg.topic+ " "+str(msg.payload))

    if str(msg.topic) == "esp32/toldo":
        if((str(msg.payload)[2:][:-1] == "down") and (bajaToldoLluvia == 1)): #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
            bajaToldoLluvia = 0
            print("Aqui deberia cambiar la alerta lluvia ")
            alertaBajarToldoLluvia = 1
        if((str(msg.payload)[2:][:-1] == "down") and (bajaToldoViento == 1)): #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
            bajaToldoViento = 0
            print("Aqui deberia cambiar la alerta viento ")
            alertaBajarToldoViento = 1
        
    if str(msg.topic) == "esp32/lluvia": 
        mensajeLluvia= 1

    if str(msg.topic) == "esp32/LDR_persiana": 

        global salidaSol, puestaSol, persianaAutomatica
        
        if persianaAutomatica == 1:
            hora = float((str(datetime.now(pytz.timezone('Europe/Madrid')).hour) + "." + str(datetime.now().minute)))
            if((hora > salidaSol) and (hora < puestaSol)):
                client.publish("esp32/persiana","5")
                print("Entro aqui")
                estadoPersiana = 5
                abrirPersiana = 1
    
    if str(msg.topic) == "esp32/estados":
        if(str(msg.payload)[2:][:-1] != "solicitud"):
            estadoToldo = json.loads(msg.payload)['estadoToldo']
            estadoPersiana = json.loads(msg.payload)['estadoPersiana']

    if str(msg.topic) == "esp32/grafica":
        #Monto array de temperatura y hora para la gráfica
        arrayTemperatura.pop(0) # Similar a shift en javascript 
        arrayTemperatura.append(temperatura) # Similar a push en javascript

        arrayHora.pop(0) # Similar a shift en javascript 
        arrayHora.append((str(datetime.now(pytz.timezone('Europe/Madrid')).hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))) # Similar a push en javascript

        
def iniciarEstados():
    client.publish("esp32/estados", "solicitud")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

global IP
IP = socket.gethostbyname(socket.gethostname())

client.connect('192.168.1.45', 1883, 60)
#client.loop_start()
#client.loop_start()