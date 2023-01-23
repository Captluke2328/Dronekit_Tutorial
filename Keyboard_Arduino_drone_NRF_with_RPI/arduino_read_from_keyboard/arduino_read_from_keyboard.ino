
void setup() {  
  Serial.begin(115200);
  while (!Serial) {
  }
}

void loop() {
 if (Serial.available() > 0)
    {
      char c =Serial.read();
      Serial.println(c);
   }
}
