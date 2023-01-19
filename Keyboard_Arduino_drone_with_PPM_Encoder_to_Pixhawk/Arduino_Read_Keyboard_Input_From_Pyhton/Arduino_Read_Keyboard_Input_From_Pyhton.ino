#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//Declare pin state
char c;

RF24 radio(8, 7); // CE, CSN
const byte address[6] = "00001";

//Create a struct that do not exceed 32 bytes
struct Data_to_be_sent {
  char ch1;
  //byte ch2;
};

Data_to_be_sent sent_data;

void setup() {
  Serial.begin(9600);

  radio.begin();
  radio.setAutoAck(false);
  radio.setPALevel(RF24_PA_MIN);
  radio.setDataRate(RF24_250KBPS);
  radio.openWritingPipe(address);
  radio.stopListening();  

}

void loop() {

 while (Serial.available() > 0)
    {
      c =Serial.read();
      Serial.println(c);
      delay(100);
      
      //sent_data.ch1 = c;
   }

//radio.write(&sent_data, sizeof(Data_to_be_sent));
//Serial.println(sent_data.ch1);
}