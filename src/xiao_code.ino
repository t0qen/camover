#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESPping.h>
#include <HTTPClient.h>

const char *ssid = "Livebox-B780";           // wifi
const char *password = "5tCVCnX9kFXfrPXNR7"; // mot de passe wifi
const char *mqtt_server = "192.168.1.23";    // broker mqtt

const int pin = D0;   // entree adc batterie
const int relay = D9; // sortie relais

IPAddress pi_ip(192, 168, 1, 37);

bool connected = false;
float vin[4];          // mesures batterie
float vin_round = 0.0; // moyenne batterie

WiFiClient espClient;           // client wifi
PubSubClient client(espClient); // client mqtt

unsigned long last_mqtt_try = 0; // timer reconnexion mqtt

void sendNotification(const char *title, const char *message, const char *topic, const char *priority)
{
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("WiFi not connected. Skipping notification.");
    return;
  }

  HTTPClient http;

  String url = "https://ntfy.lostpacket.org/";
  url += topic;

  http.begin(url);
  http.addHeader("Title", title);
  http.addHeader("Priority", priority);
  http.addHeader("Tags", "zap");

  int httpCode = http.POST(message);

  if (httpCode == 200)
  {
    Serial.printf("Notification sent: %s\n", message);
  }
  else
  {
    Serial.printf("Failed to send notification: HTTP %d\n", httpCode);
  }

  http.end();
}
void callback(char *topic, byte *payload, unsigned int length)
{

  String message = ""; // message recu

  for (unsigned int i = 0; i < length; i++)
  { // reconstruction chaine
    message += (char)payload[i];
  }

  Serial.print("mqtt : ");
  Serial.println(message);

  if (message == "ON")
  { // allumage relais

    digitalWrite(relay, HIGH);

    client.publish(
        "camover/power/state",
        "ON",
        true);

    Serial.println("relais on");
  }

  if (message == "OFF")
  { // extinction relais

    digitalWrite(relay, LOW);

    client.publish(
        "camover/power/state",
        "OFF",
        true);

    Serial.println("relais off");
  }
}

void send()
{
  Serial.println("battery sent");
  Wire.write((byte *)&vin_round, 4); // envoi tension batterie via i2c
}

void setup()
{
  Serial.begin(9600);     // port serie
  pinMode(pin, INPUT);    // adc batterie
  pinMode(relay, OUTPUT); // sortie relais
  digitalWrite(relay, LOW);
  analogReadResolution(12);   // adc 12 bits
  Wire.begin(0x08);           // i2c esclave
  Wire.onRequest(send);       // callback i2c
  WiFi.begin(ssid, password); // connexion wifi
  Serial.print("connexion wifi");
  int i = 0;
  while (WiFi.status() != WL_CONNECTED)
  { // attente wifi
    Serial.print(".");
    if (i >= 600)
    {
      Serial.println("Timeout 5mn");
      break;
    }
    i++;
    delay(500);
  }
  connected = true;
  if (WiFi.status() != WL_CONNECTED)
  {
    connected = false;
    digitalWrite(relay, HIGH);
  }

  if (connected)
  {
    Serial.println();
    Serial.println("wifi connecte");
    Serial.println(WiFi.localIP());

    client.setServer(mqtt_server, 1883); // broker mqtt
    client.setCallback(callback);        // callback mqtt

    sendNotification("camover notification", "xiao has started", "camover_xiao", "high");
  }
  else
  {
    Serial.println("Not connected");
  }
}

void loop()
{
  if (connected)
  {
    if (!client.connected())
    { // verification mqtt

      if (millis() - last_mqtt_try > 5000)
      { // tentative toutes les 5s
        last_mqtt_try = millis();
        Serial.println("connexion mqtt...");

        if (client.connect("camover"))
        { // connexion broker

          Serial.println("mqtt connecte");

          client.subscribe("camover/power/set"); // topic commande relais

          client.publish(
              "camover/power/state",
              digitalRead(relay) ? "ON" : "OFF",
              true); // publication etat relais
        }
        else
        {
          Serial.print("erreur mqtt : ");
          Serial.println(client.state());
        }
      }
    }

    client.loop(); // traitement mqtt
  }

  for (int i = 0; i < 4; i++)
  {                                                              // make 4 time the measure to be more precise
    vin[i] = (4.67 * (analogRead(pin) * (3.3 / 4095.0))) + 1.13; // analog input -> battery voltage
    // Serial.println(vin[i]);
    delay(500);
  }
  vin_round = (vin[0] + vin[1] + vin[2] + vin[3]) / 4.0;
  if (vin_round <= 10.4)
  {
    Serial.println("critical battery power");
    if (connected)
    {
      bool ret = Ping.ping(pi_ip);

      if (ret)
      {
        Serial.println("pi on, so force shutdown it");
        sendNotification("camover urgent", "critical battery power, power off the pi", "camover_xiao", "urgent");
        digitalWrite(relay, LOW);
      }
      else
      {
        sendNotification("camover urgent", "critical battery power, TURN OFF SWITCH", "camover_xiao", "urgent");
      }
    }
  }
}
