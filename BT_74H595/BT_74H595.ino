#include <ADS1X15.h>
int latchPin = 8;   // STCP
int clockPin = 12;  // SHCP
int dataPin = 11;   // DS
ADS1015 ads(0X48);
int16_t adc[4];
void setup() {
  // Set all the pins of 74HC595 as OUTPUT
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  ads.begin();
  Serial.begin(9600);
}

void loop() {
  // Serial.println("measure");
  // for (int i = 0; i < 4; i++) {
  //   digitalWrite(latchPin, LOW);
  //   shiftOut(dataPin, clockPin, LSBFIRST, pow(2, 7 - i));
  //   adc[i] = ads.readADC(0);
  //   digitalWrite(latchPin, HIGH);
  //   delay(300);
  //   Serial.print(float(adc[i]) * 300 / (5000 - float(adc[i]) * 3));
  //   Serial.print(' ');
  //   Serial.print(adc[i]);
  //   Serial.print("  ");
  // }
  // Serial.println();
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, 128);
  int adc0=ads.readADC(0);
  digitalWrite(latchPin, HIGH);
  // delay(300);
  Serial.println(float(adc0) * 300 / (5000 - float(adc0) * 3));
  delay(3000);
}
