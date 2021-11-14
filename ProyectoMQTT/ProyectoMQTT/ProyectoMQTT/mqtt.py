import paho.mqtt.client as mqtt

mensaje1="";mensaje2="";mensaje3=""
documento = ""

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt" + str(rc))
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")
    client.subscribe("esp32/pressure")

def on_message(client, userdata, msg):

    global mensaje1
    global mensaje2
    global mensaje3
    global documento
    if str(msg.topic) == "esp32/temperature":
        mensaje1 = str(msg.payload)[2:][:-1] + " ºC"#elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print("La temperatura es:" + mensaje1)        
       # print(msg.topic+ " "+str(msg.payload))
        
    if str(msg.topic) == "esp32/humidity":
        mensaje2 = str(msg.payload)[2:][:-1] + " %"#elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print("La humedad es:" + mensaje2)       
        #print(msg.topic+ " "+str(msg.payload))
    
    if str(msg.topic) == "esp32/pressure":
        mensaje3 = str(msg.payload)[2:][:-1] + " hPa"#elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print("La presion es:" + mensaje2)       
        #print(msg.topic+ " "+str(msg.payload))

    documento = """<html>
    <meta http-equiv="refresh" content="5" / 
    <body>
    <h2>
    La temperatura es: %s
    </h2>
    <h2>
    La humedad es: %s
    <h2/>
    <h2>
    La presion es: %s
    <h2/>
   
    </body>
    </html>""" %(mensaje1, mensaje2, mensaje3)

    #la linea <meta http-equiv="refresh" content="5" /  es para actualziar la pagina cada 5 segundos

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.35", 1883, 60)
#client.loop_start()
#client.loop_start()