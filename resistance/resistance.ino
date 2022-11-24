float input = 0;
float avg = 0;

void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  pinMode(5, INPUT);

}

void loop() {
  for(int j = 0; j < 5; ++j) {
    input = 0;
    avg = 0;
    for(int i = 0; i < 40; ++i) {
      input = (float)analogRead(A0);
      Serial.print(100 * input / (1023 - input));
      Serial.print(' ');
      delay(40);
      avg += input;
    }
    avg /= 40;
    Serial.println(' ');
    Serial.print(100 * avg / (1023 - avg));
    Serial.println("\n\n");
    delay(1000);
  }
  while(1) {
    continue;
  }
}
