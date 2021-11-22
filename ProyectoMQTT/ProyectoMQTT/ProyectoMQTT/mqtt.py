import paho.mqtt.client as mqtt

mensaje1="";mensaje2="";mensaje3="";mensaje4=""; mensaje5 = ""
documento = ""

def on_connect(client, userdata, flags, rc):
    print("Se conecto con mqtt" + str(rc))
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")
    client.subscribe("esp32/pressure")
    client.subscribe("esp32/LED")

def on_message(client, userdata, msg):

    global mensaje1
    global mensaje2
    global mensaje3
    global mensaje4
    global mensaje5
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

    if str(msg.topic) == "esp32/LED":
        mensaje4 = str(msg.payload)[2:][:-1] #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print(mensaje4)       
        #print(msg.topic+ " "+str(msg.payload))

    if str(msg.topic) == "esp32/toldo":
        mensaje4 = str(msg.payload)[2:][:-1] #elimino los dos primeros caracteres y el ultimo (mensaje original: b'22.22')
        print(mensaje5)       
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
    <h2>
    %s
    <h2/>
    <h2>
    %s
    <h2/>
    <input type="button" id='script' name="Subir persiana" value=" Subir persiana " onclick="subirPersiana()">

    <input type="button" id='script' name="Bajar persiana" value=" Bajar persiana " onclick="bajarPersiana()">


    <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

    <script>
        function subirPersiana(){
            $.ajax({
              url: "/subirPersiana",
             context: document.body
            }).done(function() {
             alert('Subiendo persiana');;
            });
        }
    </script>

    <script>
        function bajarPersiana(){
            $.ajax({
              url: "/bajarPersiana",
             context: document.body
            }).done(function() {
             alert('Bajando persiana');;
            });
        }
    </script>


    </body>
    </html>""" %(mensaje1, mensaje2, mensaje3, mensaje4, mensaje5)

    #la linea <meta http-equiv="refresh" content="5" /  es para actualziar la pagina cada 5 segundos

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.46", 1883, 60)
#client.loop_start()
#client.loop_start()