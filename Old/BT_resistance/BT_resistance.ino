#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>

SoftwareSerial BTSerial(10,11);
Adafruit_ADS1015 ads;
const float multiplier = 3.0F;
bool start = false;
byte btRead;
unsigned int anaIn;
int16_t adc0;

void setup() {
  BTSerial.begin(38400);
  Serial.begin(9600);
  ads.begin();
}

void BTPrint(unsigned int);

void loop() {
  if(BTSerial.available()) {
    btRead = BTSerial.read();
//    Serial.print("brRead:");
//    Serial.println(btRead);
    if(!start) {
      start = true;
//      Serial.println("start");
    }
    else if(btRead == 255) {
//      Serial.println("end");
      while(1){}
    }
    else {
      for(byte j = 0; j < btRead; ++j) {
        for(byte i = 0; i < 20; ++i) {
          adc0 = ads.readADC_SingleEnded(0);
          Serial.println(adc0 * 300.0F / (5000-adc0));
          BTPrint(adc0);
          delay(30);
        }
      }
      delay(3000);
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
