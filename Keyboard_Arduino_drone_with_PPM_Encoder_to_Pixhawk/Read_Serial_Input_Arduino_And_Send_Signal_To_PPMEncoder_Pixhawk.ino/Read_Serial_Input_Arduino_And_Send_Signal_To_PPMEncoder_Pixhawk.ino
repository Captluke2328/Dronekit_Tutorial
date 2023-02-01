 /**************************************************************
  This configuration is based on FlySky Fs-i6 Mode 1 as follow:
  CH1 = Aileron (Roll) 
  CH2 = Elevator (Pitch)
  CH3 = Throttle
  CH4 = Rudder (Yaw)

  Here we mapped it into servo pin as follow:
  #############################################################################################
  SERVO PIN         = Fs-ia6B Channel-> PPM READER FROM ARDUINO
  #############################################################################################
  servo1.attach(5); = CH1 //roll     -> CH[0] (From PPM reader)
  servo2.attach(6); = CH2 //pitch    -> CH[1] (From PPM reader)
  servo3.attach(7); = CH3 //throttle -> CH[2] (From PPM reader)
  servo4.attach(8); = CH4 //yaw      -> CH[3] (From PPM reader)
  servo5.attach(9)  = CH5 //stabilize, altitude hold, loiter, guided -> CH[4] (From PPM reader)
  servo6.attach(10) = CH6 //land     -> CH[5] (From PPM reader)
  #############################################################################################
  
  Note : From Fs-ia6B Channel, we will use singal pin of Fs-ia6B which will be connected to D3 (interrupt pin) of 
  Arduino. 
  
  From Arduino, we will connect pin D3 to D10 to PPM Encoder Pin.
  From PPM Encoder Pin, we will connect Signal, VDD and GND pin to PIXHAWK

/**************************************************************/

#include <PPMReader.h>
#include <Servo.h>

#define CHANNEL_DEFAULT_VALUE 1500
int interruptPin = 3;

#define channelAmount 6
int CH[channelAmount];

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

PPMReader ppm(interruptPin, channelAmount); //PPM Library Object

int arm;
int disarm;
int althold;
int stabilize;
int loiter;
int guided;
int rtl;
int land;
int roll;
int pitch;
int throttle;
int yaw;

void setup() {
  Serial.begin(115200);
  Serial.println("1. arm");
  Serial.println("2. disarm");
  Serial.println("3. althold");
  Serial.println("4. stabilize");
  Serial.println("5. loiter");
  Serial.println("6. guided");
  Serial.println("7. rtl");
  Serial.println("8. land");
  Serial.println("9. roll");
  Serial.println("10. pitch");
  Serial.println("11. throttle");
  Serial.println("12. yaw");

  servo1.attach(5); //roll     -> CH[0]
  servo2.attach(6); //pitch    -> CH[1]
  servo3.attach(7); //throttle -> CH[2]
  servo4.attach(8); //yaw      -> CH[3]
  servo5.attach(9); //stabilize, altitude hold, loiter, guided -> CH[4]
  servo6.attach(10); //land    -> CH[5]
}

void ARM(){
  Serial.println("COPTER: Armed");
  servo2.write(2002); // pitch    -> CH2 
  servo3.write(1057); // throttle -> CH3
  servo4.write(2002); // yaw      -> CH4
}

void DISARM(){
  Serial.println("COPTER: Disarm");
  servo2.write(1500); // pitch    -> CH2
  servo3.write(1057); // throttle -> CH3
  servo4.write(1500); // yaw      -> CH4
}

void ALTHOLD(){
  Serial.println("COPTER: Altitude Hold");
  servo5.write(1260); // althold -> CH5
}

void STABILIZE(){
  Serial.println("COPTER: Stabilize");
  servo5.write(1100); // stabilize -> CH5
}

void LOITER(){
  Serial.println("COPTER: Copter");
  servo5.write(1420); // loiter -> CH5
}

void GUIDED(){
  Serial.println("COPTER: Guided");
  servo5.write(1900); // guided -> CH5
}

void RTL(){
  Serial.println("COPTER: RTL");
  servo5.write(1748); // guided -> CH5
  }

void LAND(){
  Serial.println("COPTER: Land");
  servo6.write(1852); // land -> CH6
}

void ROLL(){
  Serial.println("COPTER: Roll");
  servo1.write(0);  
}

void PITCH(){
  Serial.println("COPTER: Pitch");
  servo2.write(0);
}

void THROTTLE(){
  Serial.println("COPTER: Throttle");
  servo3.write(0);
}

void YAW(){
  Serial.println("COPTER:  Yaw");
  servo3.write(0);  
}

void loop()   
{   
  //while (Serial.available() == 0) {}
  while (Serial.available() > 0) {
  int menuChoice = Serial.parseInt();

  // using if else statement
  if      (menuChoice == 1)  {Serial.print("ARM --> "      );       ARM();}
  else if (menuChoice == 2)  {Serial.print("DISARM --> "   );    DISARM();}
  else if (menuChoice == 3)  {Serial.print("ALTHOLD --> "  );   ALTHOLD();}
  else if (menuChoice == 4)  {Serial.print("STABILIZE --> "); STABILIZE();}
  else if (menuChoice == 5)  {Serial.print("LOITER --> "   );    LOITER();}
  else if (menuChoice == 6)  {Serial.print("GUIDED --> "   );    GUIDED();}
  else if (menuChoice == 7)  {Serial.print("RTL --> "      );       RTL();}
  else if (menuChoice == 8)  {Serial.print("LAND --> "     );      LAND();}
  else if (menuChoice == 9)  {Serial.print("ROLL --> "     );      ROLL();}
  else if (menuChoice == 10) {Serial.print("PITCH --> "    );     PITCH();}
  else if (menuChoice == 11) {Serial.print("THROTTLE --> " );  THROTTLE();}
  else if (menuChoice == 12) {Serial.print("YAW --> "      );       YAW();}

  // using switch statement
  /* switch (menuChoice) {
    case 1:
    Serial.print("Arm: ");
    ARM();
    break;

    case 2:
    Serial.print("Disarm: ");
    break;

    case 3:
    Serial.print("Althold: ");
    break;

    case 4:
    Serial.print("Stabilize: ");
    break;

    case 5:
    Serial.print("loiter: ");
    break;

    case 6:
    Serial.print("guided: ");
    break;

    case 7:
    Serial.print("rtl: ");
    break;

    case 8:
    Serial.print("land: ");
    break;

    case 9:
    Serial.print("roll: ");
    break;

    case 10:
    Serial.print("pitch: ");
    break;

    case 11:
    Serial.print("throttle: ");
    break;

    case 12:
    Serial.print("yaw: ");
    break;
   } */
   } 
  
    // Serial.println("Enter your name.");  
    // while (Serial.available() == 0)   
    // { //Wait for user input  }  
    // name = Serial.readString(); //Reading the Input string from Serial port.  
    // Serial.println("Enter your Moblie No.");  
    // while (Serial.available() == 0) {}  
    // Mobile = Serial.readString();  
    // Serial.println("Enter your Address.");  
    // while (Serial.available() == 0) {}  
    // Address = Serial.readString();  
    // Serial.println("Enter your Email.");  
    // while (Serial.available() == 0) {}  
    // Email = Serial.readString();  
    // Serial.println("-------------------------"); //Showing the details  
    // Serial.println("YOUR NAME:" + name);  
    // Serial.println("YOUR MOBILE NO:" + Mobile);  
    // Serial.println("YOUR ADDRESS:" + Address);  
    // Serial.println("YOUR EMAIL:" + Email);  
    // Serial.println("Thanks You...");  
    // Serial.println("");  
    // while (Serial.available() == 0) {}  
}

void PPM_width_values()
{
  /***DAPATKAN MAKLUMAT PPM UNTUK SETIAP CHANNEL***/
   CH[0] = ppm.latestValidChannelValue(1, 2006);
   CH[1] = ppm.latestValidChannelValue(2, 1050);
   CH[2] = ppm.latestValidChannelValue(3, 2008); //modify this value according to Radio Calibration value which in this case is Max
   CH[3] = ppm.latestValidChannelValue(4, 2006);
   CH[4] = ppm.latestValidChannelValue(5, 2006);
   CH[5] = ppm.latestValidChannelValue(6, 2006);  

   //LAKUKAN SEBARANG AKTIVITI PROJECT SELEPAS DATA CHANNEL DITERIMA
  //>Code di sini
  servo1.write(CH[0]); 
  servo2.write(CH[1]);
  servo3.write(CH[2]);
  servo4.write(CH[3]);
  servo5.write(CH[4]);
  servo6.write(CH[5]);

  Serial.print("CH1:"); // roll
  Serial.print(CH[0]);
 
  Serial.print(" CH2:"); //pitch
  Serial.print(CH[1]);

  Serial.print(" CH3:"); //throttle
  Serial.print(CH[2]);

  Serial.print(" CH4:"); //yaw
  Serial.print(CH[3]);

  Serial.print(" CH5:");
  Serial.print(CH[4]);

  Serial.print(" CH6:");
  Serial.print(CH[5]);

  Serial.println();

}





