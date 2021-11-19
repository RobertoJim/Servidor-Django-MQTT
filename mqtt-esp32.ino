/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com
*********/

#include <Wire.h>
#include <WiFi.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <PubSubClient.h>


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


#define SEALEVELPRESSURE_HPA (1024) //Presion a nivel del mar Málaga

//uncomment the following lines if you're using SPI
#define BME_SCK 5 //SCL
#define BME_MISO 16 //SDO
#define BME_MOSI 17 //SDA
#define BME_CS 4 //CS

#define pinLDR 34
#define pinLED 13
#define sensorPIR 18

#define motorPin1 23    // 28BYJ48 In1
#define motorPin2 22    // 28BYJ48 In2
#define motorPin3 21   // 28BYJ48 In3
#define motorPin4 15   // 28BYJ48 In4

#define rainDigital 35

//Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI
Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK);
float temperature = 0;
float humidity = 0;
float pressure = 0;

int PIR = 0;
int tiempo3 = 0;
int toldo = 1;

int motorSpeed = 1200;   //variable para fijar la velocidad
int stepCounter = 0;     // contador para los pasos
int stepsPerRev = 2048;  // pasos para una vuelta completa

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
  bme.setGasHeater(320, 150); // 320*C for 150 ms

  pinMode(pinLED, OUTPUT);
  pinMode(sensorPIR, INPUT);

  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);

  pinMode(rainDigital, INPUT);
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
  if (String(topic) == "esp32/output") {
    Serial.print("Changing output to ");
    if (messageTemp == "on") {
      Serial.println("on");
      digitalWrite(pinLED, HIGH);
    }
    else if (messageTemp == "off") {
      Serial.println("off");
      digitalWrite(pinLED, LOW);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      //client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void clockwise()
{
  stepCounter++;
  if (stepCounter >= numSteps) stepCounter = 0;
  setOutput(stepCounter);
}

void anticlockwise()
{
  stepCounter--;
  if (stepCounter < 0) stepCounter = numSteps - 1;
  setOutput(stepCounter);
}

void setOutput(int step)
{
  digitalWrite(motorPin1, bitRead(stepsLookup[step], 0));
  digitalWrite(motorPin2, bitRead(stepsLookup[step], 1));
  digitalWrite(motorPin3, bitRead(stepsLookup[step], 2));
  digitalWrite(motorPin4, bitRead(stepsLookup[step], 3));
}

void BME() {

  // Temperature in Celsius
  temperature = bme.readTemperature();
  // Convert the value to a char array
  char tempString[8];
  dtostrf(temperature, 1, 2, tempString);
  Serial.print("Temperature: ");
  Serial.println(tempString);
  client.publish("esp32/temperature", tempString);

  humidity = bme.readHumidity();
  // Convert the value to a char array
  char humString[8];
  dtostrf(humidity, 1, 2, humString);
  Serial.print("Humidity: ");
  Serial.println(humString);
  client.publish("esp32/humidity", humString);

  pressure = bme.readPressure() / 100.0;
  // Convert the value to a char array
  char presString[8];
  dtostrf(pressure, 1, 2, presString);
  Serial.print("Pressure: ");
  Serial.println(presString);
  client.publish("esp32/pressure", presString);
}

void LED() {

  PIR = digitalRead(sensorPIR);//Leemos el estado del del sensor PIR
  if ((PIR == 1) && (analogRead(pinLDR) < 600))
  {
    digitalWrite(pinLED, HIGH);//Encendemos la luz
    client.publish("esp32/LED", "Luz encendida");
  }
  if (millis() > tiempo3 + 2000) {

    tiempo3 = millis();
    Serial.print("Luz: ");
    Serial.println(digitalRead(pinLED));
    Serial.print("LDR: ");
    Serial.println(analogRead(pinLDR));
    if (digitalRead(pinLED) == 1) {
      digitalWrite(pinLED, LOW);//Luego la apagamos
      client.publish("esp32/LED", "Luz apagada");
      PIR = 0;//Asignamos el valor "0" a la variable PIR para que deje de cumplirse la condición
    }

  }

}

void lluvia() {

  if ((digitalRead(rainDigital) == LOW) && (toldo == 1)) {
    Serial.println("Detectada lluvia");
    client.publish("esp32/toldo", "Toldo recogido");
    toldo = 0;
    for (int i = 0; i < stepsPerRev * 2; i++)
    {
      clockwise();
      delayMicroseconds(motorSpeed);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }


  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    BME();
  }
  LED();
  lluvia();

  client.loop();

}
