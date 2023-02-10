#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1015 ads;
const float multiplier = 3.0F;
int16_t adc0_, adc1_b, adc2_y, adc3_o;
float r_, r_b, r_y, r_o;

float resSer(float, float, float);
float resPar(int16_t);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ads.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  adc0_ = ads.readADC_SingleEnded(0);
  adc1_b = ads.readADC_SingleEnded(1);
  adc2_y = ads.readADC_SingleEnded(2);
  adc3_o = ads.readADC_SingleEnded(3);

  r_ = resPar(adc0_);
  r_b = resPar(adc1_b);
  r_y = resPar(adc2_y);
  r_o = resPar(adc3_o);
//  r1 = resSer(1023, in0, r100);
//  r2 = resSer(in0, in2, r100);
//  r3 = resSer(in2, in3, r100);
//  r4 = resSer(in3, r100, r100);
  Serial.print(adc0_);
  Serial.print(' ');
  Serial.print(adc1_b);
  Serial.print(' ');
  Serial.print(adc2_y);
  Serial.print(' ');
  Serial.println(adc3_o);
  
  Serial.print(r_);
  Serial.print(' ');
  Serial.print(r_b);
  Serial.print(' ');
  Serial.print(r_y);
  Serial.print(' ');
  Serial.println(r_o);
  Serial.println();
  delay(5000);
  
  
}

float resSer(float high, float low, float r100) {
  return (100*(high-low)/r100);
}

float resPar(int16_t in) {
  float out = (float)in * multiplier * 100 / (5000 - in * multiplier);
  return out;
}
