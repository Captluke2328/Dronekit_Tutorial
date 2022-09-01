from dronekit import *
from dronekit_engine_improve import *
import keyboard as kp
import socket
from time import sleep
import numpy as np
import threading

class control_improvise():
    def __init__(self):
        try:
            
            self.connection_string = '127.0.0.1:14550'
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")
       
        except socket.error:
            print("No server exist")
        
        self.engine_imp = Engine_Improve(self)
        self.THRESHOLD_ALT = 0.3
        self.mode_g   = 0
        self.mode_l   = 0
        self.mode_s   = 0
        self.count    = 0
        self.takeoff = False
        self.takeoff_alt = 1.8
                    
    def getKeyboardInput(self):         
        if kp.is_pressed('g'):
            self.mode_g +=1
            if self.mode_g < 2:
                print("Vehicle Mode : Guided")    
                @self.vehicle.on_attribute('mode')
                def mode_callback(self,attr_name, value):
                    print(f">> Mode Updated: {value}")      
                            
                # ## We will not let the script to continue unless it changes to GUIDED
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
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")
                
            self.vehicle.mode = VehicleMode("STABILIZE")
            print("Vehicle Mode : Stabilize")
            while not self.vehicle.mode.name == "STABILIZE":
                sleep(1)
                
        # Go Up
        if kp.is_pressed('UP') and self.vehicle.armed:
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
                            self.takeoff = True
                            break
                        sleep(1)
                        
                    # while self.vehicle.location.global_relative_frame.alt < (self.takeoff_alt - self.THRESHOLD_ALT):
                    #     sleep(0.3)
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
            self.mode_l +=1
            if self.mode_l < 2:
                self.vehicle.armed = False
                self.takeoff = False
                self.mode_g = 0
                self.count = 0
                
                print("Vehicle Mode : Return To Launch")
                self.vehicle.channels.overrides = {}
                
                # Change RTL altitude to 5m (500 cm) - Default is 15m
                self.vehicle.parameters['RTL_ALT'] = 500
                self.vehicle.mode = VehicleMode("RTL")
                
                print(self.vehicle.location.global_relative_frame.alt)
                 
        elif kp.is_pressed('e') and self.vehicle.armed:
            print("Vehicle Mode : Freeze")
            x,y,z = 0,0,0
            self.engine_imp.send_global_velocity(
            x,
            y,
            z,
            2, 
            )
            # 1st option
            self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
        elif kp.is_pressed('r'):
            self.mode_s +=1
            if self.mode_s < 2:      
                print("Warning : Reset Vehicle State")
                self.mode_g = 0
                self.mode_l = 0
                self.count = 0
            
        #else:
        #    if self.vehicle.armed and self.takeoff :
        #        print("Vehicle Mode : Hovering")
        #        x,y,z = 0,0,0
        #        self.engine_imp.send_global_velocity(
        #        x,
        #        y,
        #        z,
        #        2, 
        #        )
                # 1st option
        #        self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
    sleep(0.25)
            
if __name__ == '__main__':
    init = control_improvise()
    while True:
        try:
            #vals = threading.Thread(target=init.getKeyboardInput)
            vals = init.getKeyboardInput()  
            
        except Exception as e:
            print(str(e))
            
            
            
        
            


