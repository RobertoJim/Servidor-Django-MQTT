#include <Wire.h>
#include <WiFi.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "HardwareSerial.h"

// Replace the next variables with your SSID/Password combination
const char* ssid = "PUTODIGI";
const char* password = "123tunometescabra!";

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.1.45";

WiFiClient espClient;
PubSubClient client(espClient);
char msg[50];
int value = 0;
StaticJsonDocument <256> doc, doc2;
char out[256], out2[256];

#define pinLDR_LED 34
#define pinLED 13
#define sensorPIR 12

#define pinLDR_persiana 32
//Persiana
#define motor1Pin1 23    // 28BYJ48 In1
#define motor1Pin2 19    // 28BYJ48 In2
#define motor1Pin3 18   // 28BYJ48 In3W
#define motor1Pin4 5   // 28BYJ48 In4

//Toldo
#define motor2Pin1 4    // 28BYJ48 In1
#define motor2Pin2 0    // 28BYJ48 In2
#define motor2Pin3 2   // 28BYJ48 In3
#define motor2Pin4 15   // 28BYJ48 In4

#define rainAnalog 35

Adafruit_BME680 bme; // I2C

float temperature = 0;
float humidity = 0;
float pressure = 0; 
int CO2;

int PIR = 0;
unsigned long tiempo1 = 0, tiempo2=0, tiempo3 = 0, lastMsg = 0, lastMsg2 = 0;
char tempString[8];
int led = 0;
int medidaLluvia = 0;
int estadoToldo = 0;
int estadoPersiana = 0; //Variable para ver si persiana esta subida o no, si esta a posicion4 o menos se considera bajada

const int motorSpeed = 1200;   //variable para fijar la velocidad
int stepCounter1 = 0;     // contador para los pasos
int stepCounter2 = 0;     // contador para los pasos
const int stepsPerRev = 4096;  // pasos para una vuelta completa

int posPersianaActual = 1;
int posPersianaAnterior = 1;

//secuencia media fase
const int numSteps = 8;
const int stepsLookup[8] = { B1000, B1100, B0100, B0110, B0010, B0011, B0001, B1001 };

//Senseair S8
HardwareSerial K_30_Serial(2); 

byte readCO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};  //Command packet to read Co2 (see app note)
byte response[] = {0,0,0,0,0,0,0};  //create an array to store the response

//multiplier for value. default is 1. set to 3 for K-30 3% and 10 for K-33 ICB
int valMultiplier = 1;

void setup() {
  Serial.begin(115200);
  K_30_Serial.begin(9600);    //Opens the virtual serial port with a baud of 9600
  // default settings
  // (you can also pass in a Wire library object like &Wire2)
  //status = bme.begin();
  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Set up oversampling and filter initialization                                              //PARÁMETROS: BME680_OS_NONE: apaga la lectura;
  bme.setTemperatureOversampling(BME680_OS_8X); //Ajuste de sobremuestreo de temperatura          BME680_OS_1X    BME680_OS_2X   BME680_OS_4X   BME680_OS_8X  BME680_OS_16X
  bme.setHumidityOversampling(BME680_OS_2X);  // Establece el sobremuestreo de humedad
  bme.setPressureOversampling(BME680_OS_4X);  // Ajuste de sobremuestreo de presiçon
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);  // El sensor BME680 integra un filtro IIR interno para reducir los cambios a corto plazo en los valores de salida del sensor causados ​​por perturbaciones externas.

  pinMode(pinLED, OUTPUT);
  pinMode(sensorPIR, INPUT);

  pinMode(motor1Pin1, OUTPUT); // Persiana
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor1Pin3, OUTPUT);
  pinMode(motor1Pin4, OUTPUT);

  pinMode(motor2Pin1, OUTPUT); // Toldo
  pinMode(motor2Pin2, OUTPUT);
  pinMode(motor2Pin3, OUTPUT);
  pinMode(motor2Pin4, OUTPUT);

  //pinMode(rainDigital, INPUT);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
  // Changes the output state according to the message
  if (String(topic) == "esp32/persiana") {
    Serial.print("Changing output to ");
    if (messageTemp == "1") {
      Serial.println(" persiana 1"); 
      estadoPersiana = 0;
      posPersianaAnterior = posPersianaActual; 
      posPersianaActual = 1;
      if(posPersianaAnterior < posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaActual-posPersianaAnterior+1)); i++)
        {
          clockwise1();
          delayMicroseconds(motorSpeed);
        }
      } else if(posPersianaAnterior > posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaAnterior-posPersianaActual+1)); i++)
        {
          anticlockwise1();
          delayMicroseconds(motorSpeed);
        }
      }
      
    }
    else if (messageTemp == "2") {    
      Serial.println("persiana 2");
      estadoPersiana = 0;
      posPersianaAnterior = posPersianaActual; 
      posPersianaActual = 2;
      if(posPersianaAnterior < posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaActual-posPersianaAnterior+1)); i++)
        {
          clockwise1();
          delayMicroseconds(motorSpeed);
        }
      } else if(posPersianaAnterior > posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaAnterior-posPersianaActual+1)); i++)
        {
          anticlockwise1();
          delayMicroseconds(motorSpeed);
        }
      }
    }else if (messageTemp == "3") {    
      Serial.println("persiana 3");
      estadoPersiana = 0;
      posPersianaAnterior = posPersianaActual; 
      posPersianaActual = 3;
       if(posPersianaAnterior < posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaActual-posPersianaAnterior+1)); i++)
        {
          clockwise1();
          delayMicroseconds(motorSpeed);
        }
      } else if(posPersianaAnterior > posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaAnterior-posPersianaActual+1)); i++)
        {
          anticlockwise1();
          delayMicroseconds(motorSpeed);
        }
      }
    }else if (messageTemp == "4") {    
      Serial.println("persiana 4");
      estadoPersiana = 0;
      posPersianaAnterior = posPersianaActual; 
      posPersianaActual = 4;
       if(posPersianaAnterior < posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaActual-posPersianaAnterior+1)); i++)
        {
          clockwise1();
          delayMicroseconds(motorSpeed);
        }
      } else if(posPersianaAnterior > posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaAnterior-posPersianaActual+1)); i++)
        {
          anticlockwise1();
          delayMicroseconds(motorSpeed);
        }
      }
    }else if (messageTemp == "5") {    
      Serial.println("persiana 5");
      estadoPersiana = 1;
      posPersianaAnterior = posPersianaActual; 
      posPersianaActual = 5;
      if(posPersianaAnterior < posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaActual-posPersianaAnterior+1)); i++)
        {
          clockwise1();
          delayMicroseconds(motorSpeed);
        }
      } else if(posPersianaAnterior > posPersianaActual)
      {
        for (int i = 0; i < ((stepsPerRev/5)*(posPersianaAnterior-posPersianaActual+1)); i++)
        {
          anticlockwise1();
          delayMicroseconds(motorSpeed);
        }
      }
    }
  }

  if (String(topic) == "esp32/toldo") {
    Serial.print("Changing output to ");
    if (messageTemp == "up") {
      Serial.println("up toldo");
      estadoToldo = 1;
      for (int i = 0; i < stepsPerRev; i++)
      {
        clockwise2();
        delayMicroseconds(motorSpeed);
      }
    }
    else if (messageTemp == "down") {
      Serial.println("down toldo");
      estadoToldo = 0;
      for (int i = 0; i < stepsPerRev; i++)
      {
        anticlockwise2();
        delayMicroseconds(motorSpeed);
      }
    }
  }
  if (String(topic) == "esp32/estados") {
    if (messageTemp == "solicitud") {
      doc2["estadoToldo"] = estadoToldo;
      doc2["estadoPersiana"] = posPersianaActual;
      serializeJson(doc2, out2);
      client.publish("esp32/estados", out2);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/persiana");
      client.subscribe("esp32/toldo");
      client.subscribe("esp32/estados");
      //Mando primer mensaje que para el led aparezca en la inerfaz apagado
      client.publish("esp32/LED", "0"); //Para que aparezca la imagen de bombilla apagada en la interfaz al iniciar la aplicacion
      Serial.println("Mando este primre mensaje");
      led = 0; //Quizas innecesario, ya que el led se inicializa a 0
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
  //Envio aqui primer dato de la grafica, ya que si lo pongo en el setup se intenta enviar antes de que este conectado al broker MQTT
  //Se envia este dato para que apaarezca un primer valor en la grafica al iniciar el sistema
  dtostrf(bme.readTemperature(), 4, 2, tempString); 
  client.publish("esp32/grafica", tempString);
}

void clockwise1()
{
  stepCounter1++;
  if (stepCounter1 >= numSteps) stepCounter1 = 0;
  setOutput1(stepCounter1);
}

void anticlockwise1()
{
  stepCounter1--;
  if (stepCounter1 < 0) stepCounter1 = numSteps - 1;
  setOutput1(stepCounter1);
}

void setOutput1(int step)
{
  digitalWrite(motor1Pin1, bitRead(stepsLookup[step], 0));
  digitalWrite(motor1Pin2, bitRead(stepsLookup[step], 1));
  digitalWrite(motor1Pin3, bitRead(stepsLookup[step], 2));
  digitalWrite(motor1Pin4, bitRead(stepsLookup[step], 3));
}

void clockwise2()
{
  stepCounter2++;
  if (stepCounter2 >= numSteps) stepCounter2 = 0;
  setOutput2(stepCounter2);
}

void anticlockwise2()
{
  stepCounter2--;
  if (stepCounter2 < 0) stepCounter2 = numSteps - 1;
  setOutput2(stepCounter2);
}

void setOutput2(int step)
{
  digitalWrite(motor2Pin1, bitRead(stepsLookup[step], 0));
  digitalWrite(motor2Pin2, bitRead(stepsLookup[step], 1));
  digitalWrite(motor2Pin3, bitRead(stepsLookup[step], 2));
  digitalWrite(motor2Pin4, bitRead(stepsLookup[step], 3));
}

void sendRequest(byte packet[])
{
  while(!K_30_Serial.available())  //keep sending request until we start to get a response
  {
    K_30_Serial.write(readCO2,7);
    delay(50);
  }
  
  int timeout=0;  //set a timeoute counter
  while(K_30_Serial.available() < 7 ) //Wait to get a 7 byte response
  {
    timeout++;  
    if(timeout > 10)    //if it takes to long there was probably an error
      {
        while(K_30_Serial.available())  //flush whatever we have
          K_30_Serial.read();
          
          break;                        //exit and try again
      }
      delay(50);
  }
  
  for (int i=0; i < 7; i++)
  {
    response[i] = K_30_Serial.read();
  }  
}

unsigned long getValue(byte packet[])
{
    int high = packet[3];                        //high byte for value is 4th byte in packet in the packet
    int low = packet[4];                         //low byte for value is 5th byte in the packet

  
    unsigned long val = high*256 + low;                //Combine high byte and low byte with this formula to get value
    return val* valMultiplier;
}

void datosSensores() {

  doc["temperature"] = bme.readTemperature();

  doc["humidity"] = bme.readHumidity();

  doc["pressure"] = bme.readPressure() / 100.0;

  sendRequest(readCO2);
  unsigned long valCO2 = getValue(response);
  doc["co2"] = valCO2;

  serializeJson(doc, out);
  client.publish("esp32/sensor", out);
  Serial.println(out);
}

void LED() {

  PIR = digitalRead(sensorPIR);//Leemos el estado del del sensor PIR
  if(led==0){ //Este if hace que no se mande el topic led = 1 todas las veces que entra en el bucle durante los 10s
    if ((PIR == 1) && (analogRead(pinLDR_LED) < 600))
    {
      digitalWrite(pinLED, HIGH);//Encendemos la luz
      client.publish("esp32/LED", "1");
      led = 1;
    }
  }
  if (millis() - tiempo1 > 10000) {

    tiempo1 = millis();
    Serial.print("Luz: ");
    Serial.println(digitalRead(pinLED));
    Serial.print("LDR LED: ");
    Serial.println(analogRead(pinLDR_LED));
    if (digitalRead(pinLED) == 1) {
      digitalWrite(pinLED, LOW);//Luego la apagamos

      client.publish("esp32/LED", "0");
      led = 0;
      PIR = 0;//Asignamos el valor "0" a la variable PIR para que deje de cumplirse la condición
    }

  }

}

void lluvia() {


  if (millis() - tiempo2 > 2000) {

    medidaLluvia = analogRead(rainAnalog);
    tiempo2 = millis();
    Serial.print("LLuvia: ");
    Serial.println(medidaLluvia);
    if((medidaLluvia < 1500) && (estadoToldo == 1)){

      client.publish("esp32/lluvia", "1");
      for (int i = 0; i < stepsPerRev * 2; i++)
      {
        anticlockwise2();
        delayMicroseconds(motorSpeed);
      }
    }
    
  }

  /*if ((digitalRead(rainDigital) == LOW) && (toldo == 1)) {
    Serial.println("Detectada lluvia");
    client.publish("esp32/toldo", "Toldo recogido");
    toldo = 0;
    for (int i = 0; i < stepsPerRev * 2; i++)
    {
      clockwise();
      delayMicroseconds(motorSpeed);
    }
    }*/
}

void LDR_persiana(){

    if (millis() - tiempo3 > 2000) {
    tiempo3 = millis();
    Serial.print("LDR persiana: ");
    Serial.println(analogRead(pinLDR_persiana));
    Serial.print("Mi estado persiana es :");
    Serial.println(estadoPersiana);

    if ((analogRead(pinLDR_persiana) < 600) and (estadoPersiana == 0) )
    {
        client.publish("esp32/LDR_persiana", "1");
    }

  }
    
}
  


void loop() {
  
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  if (millis() - lastMsg > 5000) {
    lastMsg = millis();
    datosSensores();
  }
  if (millis() - lastMsg2 > 1800000) {
    lastMsg2 = millis();
    dtostrf(bme.readTemperature(), 4, 2, tempString);
    client.publish("esp32/grafica", tempString);
  }
  LED();
  lluvia();
  LDR_persiana();
}