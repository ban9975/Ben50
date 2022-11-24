#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10,11);
bool start = false;
byte btRead;
//byte iter;
unsigned int sTime;
unsigned int cTime;
unsigned int anaIn;

void setup() {
  BTSerial.begin(38400);
  Serial.begin(9600);
}

void BTPrint(unsigned int);

void loop() {
  if(BTSerial.available()) {
    btRead = BTSerial.read();
    Serial.print("brRead:");
    Serial.println(btRead);
    if(!start) {
      start = true;
      Serial.println("start");
    }
    else if(btRead == 255) {
      Serial.println("end");
      while(1){}
    }
    else {
      for(byte j = 0; j < btRead; ++j) {
        sTime = millis();
        for(byte i = 0; i < 40; ++i) {
          cTime = millis();
          anaIn = analogRead(A0);
          Serial.println(anaIn);
          BTPrint(cTime - sTime);
          BTPrint(anaIn);
          delay(40);
        }
      }
      delay(1000);
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
