#include <Wire.h>
#include <WiFi.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <PubSubClient.h>
#include <ArduinoJson.h>


// Replace the next variables with your SSID/Password combination
const char* ssid = "PUTODIGI";
const char* password = "123tunometescabra!";

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.1.35";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
StaticJsonDocument <256> doc;
char out[256];

//uncomment the following lines if you're using SPI
/*#define BME_SCK 5 //SCL
#define BME_MISO 16 //SDO
#define BME_MOSI 17 //SDA
#define BME_CS 4 //CS*/

#define pinLDR 34
#define pinLED 13
#define sensorPIR 18

//Persiana
#define motor1Pin1 23    // 28BYJ48 In1
#define motor1Pin2 15    // 28BYJ48 In2
#define motor1Pin3 19   // 28BYJ48 In3
#define motor1Pin4 5   // 28BYJ48 In4

//Toldo
#define motor2Pin1 16    // 28BYJ48 In1
#define motor2Pin2 4    // 28BYJ48 In2
#define motor2Pin3 0   // 28BYJ48 In3
#define motor2Pin4 2   // 28BYJ48 In4

#define rainAnalog 35

Adafruit_BME680 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI
//Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK);



float temperature = 0;
float humidity = 0;
float pressure = 0; 
float CO2 = 0;

int PIR = 0;
int tiempo3 = 0, tiempo4=0;
int led = 0;
int medidaLluvia = 0;
int estadoToldo = 0;

const int motorSpeed = 1200;   //variable para fijar la velocidad
int stepCounter1 = 0;     // contador para los pasos
int stepCounter2 = 0;     // contador para los pasos
const int stepsPerRev = 2048;  // pasos para una vuelta completa

//secuencia media fase
const int numSteps = 8;
const int stepsLookup[8] = { B1000, B1100, B0100, B0110, B0010, B0011, B0001, B1001 };

void setup() {
  Serial.begin(115200);
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
    if (messageTemp == "up") {
      Serial.println("up persiana");
      
      for (int i = 0; i < stepsPerRev * 2; i++)
      {
        clockwise1();
        delayMicroseconds(motorSpeed);
      }
    }
    else if (messageTemp == "down") {
      
      Serial.println("down persiana");
      for (int i = 0; i < stepsPerRev * 2; i++)
      {
        anticlockwise1();
        delayMicroseconds(motorSpeed);
      }
    }
  }

  if (String(topic) == "esp32/toldo") {
    Serial.print("Changing output to ");
    if (messageTemp == "up") {
      Serial.println("up toldo");
      estadoToldo = 1;
      for (int i = 0; i < stepsPerRev * 2; i++)
      {
        clockwise2();
        delayMicroseconds(motorSpeed);
      }
    }
    else if (messageTemp == "down") {
      Serial.println("down toldo");
      estadoToldo = 0;
      for (int i = 0; i < stepsPerRev * 2; i++)
      {
        anticlockwise2();
        delayMicroseconds(motorSpeed);
      }
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

void Sensores() {

  // Temperature in Celsius
  temperature = bme.readTemperature();
  // Convert the value to a char array
  char tempString[8];
  dtostrf(temperature, 1, 2, tempString);
  /*Serial.print("Temperature: ");
    Serial.println(tempString);
    client.publish("esp32/temperature", tempString);*/
  doc["temperature"] = temperature;

  humidity = bme.readHumidity();
  // Convert the value to a char array
  char humString[8];
  dtostrf(humidity, 1, 2, humString);
  /*Serial.print("Humidity: ");
    Serial.println(humString);
    client.publish("esp32/humidity", humString);*/
  doc["humidity"] = humidity;

  pressure = bme.readPressure() / 100.0;
  // Convert the value to a char array
  char presString[8];
  dtostrf(pressure, 1, 2, presString);
  /*Serial.print("Pressure: ");
    Serial.println(presString);
    client.publish("esp32/pressure", presString);*/
  doc["pressure"] = pressure;

  serializeJson(doc, out);
  client.publish("esp32/sensor", out);
  Serial.println(out);
}

void LED() {

  PIR = digitalRead(sensorPIR);//Leemos el estado del del sensor PIR
  if(led==0){ //Este if hace que no se mande el topic led = 1 todas las veces que entra en el bucle durante los 10s
    if ((PIR == 1) && (analogRead(pinLDR) < 600))
    {
      digitalWrite(pinLED, HIGH);//Encendemos la luz
      client.publish("esp32/LED", "1");
      led = 1;
    }
  }
  if (millis() > tiempo3 + 10000) {

    tiempo3 = millis();
    Serial.print("Luz: ");
    Serial.println(digitalRead(pinLED));
    Serial.print("LDR: ");
    Serial.println(analogRead(pinLDR));
    if (digitalRead(pinLED) == 1) {
      digitalWrite(pinLED, LOW);//Luego la apagamos

      client.publish("esp32/LED", "0");
      led = 0;
      PIR = 0;//Asignamos el valor "0" a la variable PIR para que deje de cumplirse la condición
    }

  }

}

void lluvia() {


  if (millis() > tiempo4 + 2000) {

    medidaLluvia = analogRead(rainAnalog);
    tiempo4 = millis();
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

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    Sensores();

    

  }
  LED();
  lluvia();

}