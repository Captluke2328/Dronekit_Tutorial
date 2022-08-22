
import keyboard as kp
from time import sleep
import numpy as np
import serial
import os

class KeyboardArduino:
    def initConnection(self,portNo, baudrate):
        #os.system('sudo chmod 666 /dev/cu.usbmodem1101')
        try:
            self.ser = serial.Serial(portNo, baudrate)
            print("Device Connected")   
                     
        except:
            print("Not connected")
            
    def sendData(self,data):
        myString= "$"
        
        #for d in data:
        #   myString += str(d)
        myString = data
        
        try:
            self.ser.write(myString.encode())
            print(myString)         
        except:
            print("Data Transmission Failed")
           
    def getKeyboardInput(self):  
        
        # Set into Guided Mode    
        if kp.is_pressed('g'): 
            #print("Guided Mode") 
            self.sendData('g')  

        elif kp.is_pressed('h'):
            #print("Stabilized Mode")
            self.sendData('h')
             
        # Go Up
        elif kp.is_pressed('UP') :
            #print("Take Off")
            self.sendData('u')

        # Go Right
        elif kp.is_pressed('d'):
            #print("Go Right")
            self.sendData('d')

        # Go Left
        elif kp.is_pressed('a'):
            #print("Go Left")
            self.sendData('a')
        
        # Go Back
        elif kp.is_pressed('s') :
            #print("Go Back")
            self.sendData('s')
         
        # Go Front
        elif kp.is_pressed('w'):
            #print("Go Front")
            self.sendData('w')

        # Land   
        elif kp.is_pressed('q'):
            #print("Land")
            self.sendData('q')

        # Stop Movement
        elif kp.is_pressed('e'):
            #print("Stop movement")
            self.sendData('e')

        # Yaw Left
        elif kp.is_pressed('LEFT'):
            #print("Yaw Left")
            self.sendData('l')

        # Yaw Right
        elif kp.is_pressed('RIGHT'):
            #print("Yaw RIGHT")
            self.sendData('r')
        
        # Reset
        else:
            self.sendData('f')
                
    sleep(0.25)
            
if __name__ == '__main__':
    
    init = KeyboardArduino()
    
    ser = init.initConnection("/dev/cu.usbmodem1201","9600")
    
    while True:
        vals = init.getKeyboardInput()  
            
        
            


