import paho.mqtt.client as mqtt

mensaje1="";mensaje2=""

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt" + str(rc))
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")

def on_message(client, userdata, msg):

    global mensaje1
    global mensaje2
    if str(msg.topic) == "esp32/temperature":
        mensaje1 = str(msg.payload)
        print("la temperatura es:" + mensaje1)        
        print(msg.topic+ " "+str(msg.payload))
        
    if str(msg.topic) == "esp32/humidity":
        mensaje2 = str(msg.payload)
        print("la humedad es:" + mensaje2)       
        print(msg.topic+ " "+str(msg.payload))
    
    
   


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.35", 1883, 60)
#client.loop_start()
#client.loop_start()