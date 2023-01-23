//------------Include Configuration For Lidar------------- 
#include <TFMPlus.h>  // Include TFMini Plus Library v1.5.0
TFMPlus tfmP;         // Create a TFMini Plus object
#include "printf.h"   // Modified to support Intel based Arduino
#include <SoftwareSerial.h>

SoftwareSerial mySerial(3,2); //RX, TX

int16_t tfDist = 0;    // Distance to object in centimeters
int16_t tfFlux = 0;    // Strength or quality of return signal
int16_t tfTemp = 0;    // Internal temperature of Lidar sensor chip
int counter = 0;
char dist[11];

//-------------------------------------------------------

//------------Include Configuration for NRF----------------
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(8, 7); // CE, CSN
const byte address[6] = "00001";

struct Received_data {
  char ch1;

};

Received_data received_data;

char ch1_value;

unsigned long eventInterval = 1000;
unsigned long previousTime1 = 0;
unsigned long previousTime2 = 0;

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setAutoAck(false);
  radio.setPALevel(RF24_PA_MIN);
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(0,address);
  radio.startListening();

  Serial.begin(115200);
  delay(20);               // Give port time to initalize
  printf_begin();          // Initialize printf.
  printf("\r\nTFMPlus Library Example - 10SEP2021\r\n");  // say 'hello'

  mySerial.begin( 115200);  // Initialize TFMPLus device serial port.
  delay(20);               // Give port time to initalize
  tfmP.begin( &mySerial);   // Initialize device library object and...
  // tfmP.begin( &Serial1);   // Initialize device library object and...

  // pass device serial port to the object.

  // Send some example commands to the TFMini-Plus
  // - - Perform a system reset - - - - - - - - - - -
  printf( "Soft reset: ");
  if( tfmP.sendCommand( SOFT_RESET, 0))
  {
    printf( "passed.\r\n");
  }
  else tfmP.printReply();

  delay(500);  // added to allow the System Rest enough time to complete

  // - - Display the firmware version - - - - - - - - -
  printf( "Firmware version: ");
  if( tfmP.sendCommand( GET_FIRMWARE_VERSION, 0))
  {
    printf( "%1u.", tfmP.version[ 0]); // print three single numbers
    printf( "%1u.", tfmP.version[ 1]); // each separated by a dot
    printf( "%1u\r\n", tfmP.version[ 2]);
  }
  else tfmP.printReply();
  // - - Set the data frame-rate to 20Hz - - - - - - - -
  printf( "Data-Frame rate: ");
  if( tfmP.sendCommand( SET_FRAME_RATE, FRAME_20))
  {
    printf( "%2uHz.\r\n", FRAME_20);
  }
  else tfmP.printReply();
}

unsigned long last_Time =0;

void receive_the_data()
{
  if(radio.available()> 0)
  {
    radio.read(&received_data, sizeof(Received_data));
    last_Time = millis();
  }
}


void loop() {
  unsigned long currentTime=millis();
  if ((currentTime - previousTime1) >=50)
  {
  delay(20);   // Loop delay to match the 20Hz data frame rate
  counter++;
  if( tfmP.getData( tfDist, tfFlux, tfTemp)) // Get data from the device.
  {
    // printf( "Dist:%04icm ", tfDist);   // display distance,
    // printf( "Flux:%05i ",   tfFlux);   // display signal strength/quality,
    // printf( "Temp:%2i%s",  tfTemp, "C");   // display temperature,
    printf( "\r\n");                   // end-of-line.
    if(counter >= 10){
      sprintf (dist, "%04i", tfDist);
      counter=0;
    }
  }

  else                  // If the command fails...
  {
    tfmP.printFrame();  // display the error and HEX dataa
  }
    previousTime1 = currentTime;
  }

  // if ((currentTime - previousTime2) >=200)
  // {
    receive_the_data();
    ch1_value = received_data.ch1;
  //   previousTime2 = currentTime;
  // }

  if (tfDist < 0050)
  {
    Serial.println("b");
  }

  else
  {
    Serial.println(ch1_value);
  }
 }


