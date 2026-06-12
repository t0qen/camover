#include <Wire.h>

const int pin = D0;
float vin[4];
float vin_round = 0.0;

void setup() {
  Serial.begin(9600);
  pinMode(pin, INPUT);
  analogReadResolution(12);
  Wire.begin(0x08);
  Wire.onRequest(send);
}

void loop() {
  for (int i = 0; i < 4; i++) { // make 4 time the measure to be more precise
    vin[i] = (4.67 *  (analogRead(pin) * (3.3/4095.0)) ) + 1.13; // analog input -> battery voltage
    Serial.println(vin[i]);
    delay(500);
  }
  /*
  float v1 = min(vin[0], vin[1]);
  float v2 = min(vin[2], vin[3]);
  Serial.println("-----");
  Serial.println(v1);
  Serial.println(v2);
  vin_round = (v1 + v2) / 2.0;
  Serial.print("Round : ");
  Serial.println(vin_round);
  Serial.println("-----");
  */
}

void send() {
  vin_round = (vin[0] + vin[1] + vin[2] + vin[3]) / 4.0;
  Wire.write((byte*)&vin_round, 4);
}