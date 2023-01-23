import keyboard as kp
from time import sleep
import socket
import numpy as np
from dronekit import *
from dronekit_engine_for_RPI import *
import os

class ReadKeyboard:
    def __init__(self):
        try:       
            self.connection_string = '/dev/ttyAMA0,921600'
            #self.connection_string = '127.0.0.1:14550'
            #self.connection_string = '192.168.8.146:14553'
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")

        except socket.error:
            print("Failed to connect to Vehicle")
            
        self.engine = Engine_Improve(self)
        self.engine.start()
        self.THRESHOLD_ALT = 0.3
        self.mode_g   = 0
        self.mode_l   = 0
        self.mode_s   = 0
        self.count    = 0
        self.takeoff = False
        self.takeoff_alt = 1.5
        
                        
    def getKeyboardInput(self):  
        # Set into Guided Mode    
        if kp.is_pressed('g'): 
            print("Guided Mode")
            self.mode_g +=1        
            if self.mode_g < 2:
                print("Vehicle Mode : Guided") 
                @self.vehicle.on_attribute('mode')
                def mode_callback(self,attr_name, value):
                    print(f">> Mode Updated: {value}")
                
                # We will not let the script to continue unless it changes to GUIDED
                self.vehicle.mode = VehicleMode("GUIDED")
                while not self.vehicle.mode.name == "GUIDED":
                    sleep(1)
                    
                self.mode_s   = 0
                self.mode_l   = 0
                
                if (self.vehicle.mode.name == "GUIDED"):
                    if not self.vehicle.armed:
                        self.vehicle.armed = True
                        print("Waiting to take off")
                        
                else:
                    # Disarm if landed
                    if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                        self.vehicle.armed = False
                        self.takeoff = False
                        print("Vehicle Mode : Disarmed")
                    
                    
        elif kp.is_pressed('h'):
            print("Stabilized Mode")
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")
                
            self.vehicle.mode = VehicleMode("STABILIZE")
            print("Vehicle Mode : Stabilize")
            while not self.vehicle.mode.name == "STABILIZE":
                sleep(1)
             
        # Go Up
        elif kp.is_pressed('UP') and self.vehicle.armed :
            print("Take Off")
            self.count +=1    
            if self.count < 2:     
                print("Vehicle Mode : Take Off")
                if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                    
                    self.vehicle.simple_takeoff(self.takeoff_alt)         
                    
                    while True:
                        current_high = self.vehicle.location.global_relative_frame.alt
                        print(f"Altitude : {current_high}")
                        
                        if current_high >= self.takeoff_alt * 0.95:
                            print("Altitude Reached")
                            self.takeoff = False
                            break
                        sleep(1)
                            
                    #while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
                    #    sleep(0.3)
                    
                else:
                    if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
                        self.vehicle.mode = VehicleMode("LAND")
            
        # Go Right
        elif kp.is_pressed('d') and self.vehicle.armed:
            print("Go Right")
            x,y=0.0,0.5
            z=0
            self.engine.executeChangesNow(x,y,self.takeoff_alt)
            
        # Go Left
        elif kp.is_pressed('a') and self.vehicle.armed:
            print("Go Left")
            x,y = 0.0, -0.5 
            z = 0
            self.engine.executeChangesNow(x,y,self.takeoff_alt)

        # Go Back
        elif kp.is_pressed('s') and self.vehicle.armed:
            print("Go Back")
            x, y = -0.5, 0.0  # meters
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,self.takeoff_alt)
            
        # Go Front
        elif kp.is_pressed('w') and self.vehicle.armed:
            print("Go Front")
            x, y = 0.5, 0.0  # meters
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
             # 3rd option
            self.engine.executeChangesNow(x,y,self.takeoff_alt)

        # Land   
        elif kp.is_pressed('q') and self.vehicle.armed:
            print("Land")
            self.mode_l +=1
            if self.mode_l < 2:
                self.vehicle.armed = False
                self.takeoff = False
                self.mode_g = 0
                self.count = 0
                
                print("Vehicle Mode : Land")
                self.vehicle.channels.overrides = {}
                self.vehicle.mode = VehicleMode("LAND")

        # Stop Movement
        elif kp.is_pressed('e') and self.vehicle.armed:
            print("Stop movement")
            print("Vehicle Mode : Freeze")
            x,y,z = 0,0,0
            # self.engine.send_global_velocity(
            # x,
            # y,
            # z,
            # 1, 
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,self.takeoff_alt)    
                    
        # Reset
        elif kp.is_pressed('r') and self.vehicle.armed:
            print("Reset")
            #elif (kp.is_pressed('r')):
            self.mode_s +=1
            if self.mode_s < 2:
                print("Warning : Reset Vehicle State")
                self.mode_g = 0
                self.mode_l = 0
                self.count  = 0

        # Yaw Left
        elif kp.is_pressed('LEFT') and self.vehicle.armed:
            print("Yaw Left")
            #self.engine.rotate(-5)
            self.engine.send_movement_command_YAW(-8)

        # Yaw Right
        elif kp.is_pressed('RIGHT') and self.vehicle.armed:
            print("Yaw RIGHT")
            #self.engine.rotate(5)
            self.engine.send_movement_command_YAW(8)
                    
    sleep(0.25)

if __name__ == "__main__":
    init = ReadKeyboard()
    while True:
        init.getKeyboardInput()
    