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
float adc[8];
int nSensor = 8;
void setup() {
  Serial.begin(9600);
  ads1.begin();
  ads2.begin();
//  ads1.setGain(0);
//  ads2.setGain(0);
  if(!ads1.isConnected()) {
    Serial.println("ads not connect");
  }
}

void BTPrint(unsigned int);

void loop() {
  float f1 = ads1.toVoltage(), f2 = ads2.toVoltage();
  Serial.println(f1, 10);
  Serial.println(f2, 10);
  for(byte i = 0; i < 4; ++i) {
    adc[2*i] = ads1.toVoltage(ads1.readADC(i));
    adc[2*i+1] = ads2.toVoltage(ads2.readADC(i));
    Serial.print(float(adc[2*i])*100/(5-float(adc[2*i])), 10);
    Serial.print(' ');
    Serial.print(adc[2*i], 10);
    Serial.print("  ");
    Serial.print(float(adc[2*i+1])*100/(5-float(adc[2*i+1])), 10);
    Serial.print(' ');
    Serial.print(adc[2*i+1], 10);
    Serial.print("  ");
  }
  Serial.println();
  delay(30000);
}

void BTPrint(unsigned int output) {
  BTSerial.write(output >> 8);
  BTSerial.write(output);
}
