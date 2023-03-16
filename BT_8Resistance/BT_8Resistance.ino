#include <SoftwareSerial.h>
#include <Wire.h>
#include <ADS1X15.h>

SoftwareSerial BTSerial(8, 9);
//SoftwareSerial BTSerial(10,11);
ADS1015 ads1(0x49);
ADS1015 ads2(0x48);
bool start = false;
byte btRead;
unsigned int anaIn;
int16_t adc[8];
int nSensor = 8;
void setup() {
  BTSerial.begin(38400);
  Serial.begin(9600);
  ads1.begin();
  ads2.begin();
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
      for(byte j = 0; j < btRead; ++j) {
        for(byte i = 0; i < 20; ++i) {
          for(byte k = 0; k < 4; ++k) {
            adc[2*k] = ads1.readADC(k);
            adc[2*k+1] = ads2.readADC(k);
//            filter out abnormal value
//            while(adc[k] >= 1400) {
//              adc[k] = ads.readADC_SingleEnded(k);
//            }
            BTPrint(adc[2*k]);
            if(2*k == nSensor-1) break;
            BTPrint(adc[2*k+1]);
            if(2*k+1 == nSensor-1) break;
//            Serial.print(float(adc[2*k])*300/(5000-float(adc[2*k])*3));
//            Serial.print(' ');
//            Serial.print(adc[2*k]);
//            Serial.print("  ");
//            Serial.print(float(adc[2*k+1])*300/(5000-float(adc[2*k+1])*3));
//            Serial.print(' ');
//            Serial.print(adc[2*k+1]);
//            Serial.print("  ");
          }
//          Serial.println();
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
