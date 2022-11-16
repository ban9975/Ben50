#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10,11);
const int pin_0 = A0;
unsigned int pinIn_0;
unsigned int i;
unsigned int sTime;
unsigned int cTime;
unsigned int ben10;
bool start = false;

void setup() {
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  BTSerial.begin(38400);
  Serial.begin(9600);
}

void BTPrint(unsigned int);

void loop() {
  if(!start) {
    if(BTSerial.available()) {
      start = true;
      i = 0;
      sTime = millis();
      Serial.println("start");
    }
  }
  else {
    cTime = millis();
    pinIn_0 = analogRead(pin_0);

    BTPrint(cTime-sTime);
    BTPrint(pinIn_0);
    i += 1;
    delay(100);
    if(cTime - sTime > 10000000) {
      BTPrint(-1);
      BTPrint(-1);
      while(1) {  
      }
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
