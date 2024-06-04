#include <SoftwareSerial.h>
#include <Wire.h>
#include <ADS1X15.h>

SoftwareSerial BTSerial(8, 9);
ADS1015 ads(0X48);
bool start = false;
unsigned int anaIn;
const int nSensor=3;
int32_t btRead = 0;
int16_t adc[4];
void setup() {
  BTSerial.begin(9600);
  Serial.begin(9600);
  ads.begin();
  
}

void BTPrint(unsigned int);

void loop() {
  if(BTSerial.available()) {
    btRead = BTSerial.readString().toInt();
    Serial.println(btRead);
    if(btRead>0)
    {
      unsigned long start=millis();
      unsigned long cTime = millis();
      while(millis()-start<btRead*1000)
      {
        if(millis()-cTime >= 10)
        {
          cTime = millis();
          for(int k = 0; k < nSensor; ++k) {
            adc[k] = ads.readADC(k);
            // Serial.println(adc[k]);
            BTPrint(adc[k]);
          }
        }
      }
      BTPrint(2048);
      BTPrint(2048);
      BTPrint(2048);
      BTPrint(2048);
      BTPrint(2048);
      Serial.println(2048);
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
