from dronekit import *
from dronekit_engine_improve import *
import keyboard as kp
import socket
from time import sleep
import numpy as np

class control_improvise():
    def __init__(self):
        try:
            self.THRESHOLD_ALT = 0.3
            self.connection_string = '127.0.0.1:14550'
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")
       
        except socket.error:
            print("No server exist")
        
        self.engine_imp = Engine_Improve(self)
                    
    def getKeyboardInput(self):         
        if kp.is_pressed('g'):    
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")      
                          
            # ## We will not let the script to continue unless it changes to GUIDED
            self.vehicle.mode = VehicleMode("GUIDED")
            while not self.vehicle.mode.name == "GUIDED":
                sleep(1)
                
            if (self.vehicle.mode.name == "GUIDED"):
                if not self.vehicle.armed:
                    self.vehicle.armed = True
                
                else:
                    # Disarm if landed
                    if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                        self.vehicle.armed = False
                         
        elif kp.is_pressed('h'):
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")
                
            self.vehicle.mode = VehicleMode("STABILIZE")
            while not self.vehicle.mode.name == "STABILIZE":
                sleep(1)
                
        # Go Up
        if kp.is_pressed('UP') and self.vehicle.armed:
            print("Take Off")
            if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                takeoff_alt = 5
                self.vehicle.simple_takeoff(takeoff_alt)
                while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
                    sleep(0.3)
            else:
                if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
                    self.vehicle.mode = VehicleMode("LAND")
        
        # Go Right
        elif kp.is_pressed('d') and self.vehicle.armed:
            print("Go Right")
            x,y = 0.0, 2.0 
            yaw = self.vehicle.attitude.yaw
            self.engine_imp.send_global_velocity(
                x * np.cos(yaw) - y * np.sin(yaw),
                x * np.sin(yaw) + y * np.cos(yaw),
                0,
                2,      
            )
            self.engine_imp.send_global_velocity(0,0,0,1)

        # Go Left
        elif kp.is_pressed('a') and self.vehicle.armed:
            print("Go Left")
            x,y = 0.0, -2.0 
            yaw = self.vehicle.attitude.yaw
            self.engine_imp.send_global_velocity(
                x * np.cos(yaw) - y * np.sin(yaw),
                x * np.sin(yaw) + y * np.cos(yaw),
                0,
                2,      
            )
            self.engine_imp.send_global_velocity(0,0,0,1)
            
        # Go Back
        elif kp.is_pressed('s') and self.vehicle.armed:
            print("Go Back")
            x, y = -2.0, 0.0  # meters
            yaw = self.vehicle.attitude.yaw
            self.engine_imp.send_global_velocity(
                x * np.cos(yaw) - y * np.sin(yaw),
                x * np.sin(yaw) + y * np.cos(yaw),
                0,
                2,
            )
            self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
        # Go Front
        elif kp.is_pressed('w') and self.vehicle.armed:
            print("Go Front")
            x, y = 2.0, 0.0  # meters
            yaw = self.vehicle.attitude.yaw
            self.engine_imp.send_global_velocity(
                x * np.cos(yaw) - y * np.sin(yaw),
                x * np.sin(yaw) + y * np.cos(yaw),
                0,
                2,
            )
            self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
        elif kp.is_pressed('q') and self.vehicle.armed:
            print("Return To Launch")
            self.vehicle.mode = VehicleMode("RTL")
            self.vehicle.armed = False
            
    sleep(0.25)
            
if __name__ == '__main__':
    init = control_improvise()
    while True:
        vals = init.getKeyboardInput()  
            
            
        
            


