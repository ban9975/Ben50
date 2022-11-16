#include  <SoftwareSerial.h>  
#define Bluetooth_EN 9
#define Bluetooth_RxD 11
#define Bluetooth_TxD 10

SoftwareSerial BTSerial(Bluetooth_TxD, Bluetooth_RxD);

void setup() 
{ 
  pinMode(Bluetooth_EN, OUTPUT);
  // entering AT command mode
  digitalWrite(Bluetooth_EN, HIGH);

  Serial.begin(38400);
  Serial.print("Enter AT commands:");

  BTSerial.begin(38400);
}     

void loop()
{           
  // Keep reading from HC-05 and send to Arduino Serial Monitor
  if (BTSerial.available())
  {
    // if receive data from BTSerial
    char BTSerial_read;
    BTSerial_read = BTSerial.read();

    Serial.write(BTSerial_read);
    if(BTSerial_read == '\n')
    {
      delay(10);
      if(BTSerial.available() == 0)
      {
        // BT transmission ended
        Serial.print("Enter AT commands:");
      }  
    }
  }
  // Keep reading from Arduino Serial Monitor and send to HC-05
  if (Serial.available())
  {
    char Serial_read;
    Serial_read = Serial.read();
    Serial.print(Serial_read);
    BTSerial.write(Serial_read);
  }
}  
