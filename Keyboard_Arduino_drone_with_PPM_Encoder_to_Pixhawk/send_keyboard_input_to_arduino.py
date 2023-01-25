"""
Author : Lukas Johnny
Date : 23/8/2022
Description : This script is used to send data from Keyboard using Python library to Arduino integrated
              with NRF which act as a transmitter.

              Below is Key input from Python and Arduino and its function
              Keyboard : Arduino : Function
               g           g     : GUIDED Mode
               h           h     : STABILIZE Mode
               UP          u     : TAKEOFF Mode
               d           d     : Go Right
               a           a     : Go Left
               w           w     : Move Front
               s           s     : Move backward
               q           q     : LAND Mode
               e           e     : Freeze
               r           r     : Reset
               LEFT        n     : Yaw left
               RIGHT       m     : Yaw Right
                        
"""
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
            
        # Reset
        elif kp.is_pressed('r'):
            #print("Reset")
            self.sendData('r')

        # Yaw Left
        elif kp.is_pressed('LEFT'):
            #print("Yaw Left")
            self.sendData('n')

        # Yaw Right
        elif kp.is_pressed('RIGHT'):
            #print("Yaw RIGHT")
            self.sendData('m')
        
        # Reset
        # else:
        #     self.sendData('f')
                
    sleep(0.25)
            
if __name__ == '__main__':
    
    init = KeyboardArduino()
    
    ser = init.initConnection("COM4","115200")
    
    while True:
        vals = init.getKeyboardInput()  
            
        
            

