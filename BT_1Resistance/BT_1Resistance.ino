#include <SoftwareSerial.h>
#include <Wire.h>
#include <ADS1X15.h>
//#include <Adafruit_ADS1X15.h>

SoftwareSerial BTSerial(8, 9);
//SoftwareSerial BTSerial(10,11);
ADS1015 ads(0X48);
//Adafruit_ADS1015 ads;
bool start = false;
byte btRead;
unsigned int anaIn;
int16_t adc;
void setup() {
  BTSerial.begin(38400);
  Serial.begin(9600);
  ads.begin();
  
}

void BTPrint(unsigned int);

void loop() {
  if(BTSerial.available()) {
    btRead = BTSerial.read();
    if(btRead==1)
    {
      unsigned long start=millis();
      unsigned long cTime = millis();
      while(millis()-start<10000)
      {
        if(millis()-cTime >= 50) 
        {
          cTime = millis();
          adc = ads.readADC(0);
          BTPrint(adc);
        }
      }
      BTPrint(2048);
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
