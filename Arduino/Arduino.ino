void setup() {
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 20; i < 60; i++){
    Serial.println(String(i));
    Serial.flush();
    delay(100);
  }
  for(int i = 60; i > 20; i--){
    Serial.println(String(i));
    Serial.flush();
    delay(100);
  }
}
9