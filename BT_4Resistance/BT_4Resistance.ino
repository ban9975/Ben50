#include <SoftwareSerial.h>
#include <Wire.h>
#include <ADS1X15.h>
//#include <Adafruit_ADS1X15.h>

SoftwareSerial BTSerial(8, 9);
//SoftwareSerial BTSerial(10,11);
ADS1015 ads(0X48);
//Adafruit_ADS1015 ads;
bool start = false;
const int nSensor=3;
byte btRead;
unsigned int anaIn;
int16_t adc[4];
void setup() {
  BTSerial.begin(38400);
  Serial.begin(9600);
  ads.begin();
  
}

void BTPrint(unsigned int);

void loop() {
  if(BTSerial.available()) {
    btRead = BTSerial.read();
    Serial.println(btRead);
    if(!start) {
      start = true;
    }
    else if(btRead == 255) {
      while(1){}
    }
    else {
      Serial.println("loop");
      for(byte j = 0; j < btRead; ++j) {
        for(byte i = 0; i < 20; ++i) {
          for(byte k = 0; k < nSensor; ++k) {
            adc[k] = ads.readADC(k);
//              adc[k] = ads.readADC_SingleEnded(k);
//            filter out abnormal value
              // Serial.print(adc[k]);
            // while(adc[k] >= 1450 || adc[k] <=1150) {
            //   adc[k] = ads.readADC(k);
            // }
            BTPrint(adc[k]);
            // Serial.print(float(adc[k])*300/(5000-float(adc[k])*3));
            Serial.print(' ');
            Serial.print(adc[k]);
            // Serial.print("  ");
          }
          Serial.println();
        }
      }
      BTSerial.flush();
//      delay(3000);
    }
  }
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
