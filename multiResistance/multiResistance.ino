float r100;
float in0, in2, in3;
float r1, r2, r3, r4;

float resSer(float, float, float);
float resPar(float);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  in0 = analogRead(A0);
  in2 = analogRead(A2);
  in3 = analogRead(A3);
  r100 = analogRead(A5);

  r1 = resPar(in0);
  r2 = resPar(in2);
  r3 = resPar(in3);
  r4 = resPar(r100);
//  r1 = resSer(1023, in0, r100);
//  r2 = resSer(in0, in2, r100);
//  r3 = resSer(in2, in3, r100);
//  r4 = resSer(in3, r100, r100);
  Serial.print(r1);
  Serial.print(' ');
  Serial.print(r2);
  Serial.print(' ');
  Serial.print(r3);
  Serial.print(' ');
  Serial.println(r4);
  delay(2000);
  
  
}

float resSer(float high, float low, float r100) {
  return (100*(high-low)/r100);
}

float resPar(float in) {
  return (100*in/(1023-in));
}
