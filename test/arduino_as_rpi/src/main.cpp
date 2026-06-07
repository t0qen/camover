#include <Arduino.h>

const int m2b = 5;
const int m2a = 3;
const int m1b = 10;
const int m1a = 9;
 

void setup() {
  pinMode(m2b, OUTPUT);
  pinMode(m2a, OUTPUT);
  pinMode(m1b, OUTPUT);
  pinMode(m1a, OUTPUT);
  delay(5000);
  analogWrite(m2a, 255);
  analogWrite(m1a, 255);
  delay(10000);
  analogWrite(m2a, 0);
  analogWrite(m1a, 0);
}

void loop() {
  
}
