from dronekit import *
from pymavlink import mavutil
from time import sleep
from dronekit_engine_with_thread import *

class controlTab:
    def __init__(self,drone):
        self.vehicle = drone.vehicle
        self.drone = drone
        
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        
        self.increment_value_x = 0.5
        self.increment_value_y = 0.5
        self.increment_value_z = 0.2
        self.engine = Engine(drone,self)
        self.engine.start()
        
    def stopMovement(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.engine.executeChangesNow()
    
    # Yaw Left   
    def rotateLeft(self,angle):
        self.engine.rotate(-1,angle)
    
    # Yaw Right
    def rotateRight(self, angle):
        self.engine.rotate(1, angle)
    
    # Forward
    def increaseSpeedX(self):
        self.speed_x = 1 #self.speed_x + self.increment_value_x
        self.engine.executeChangesNow()
        
    # Backward
    def decreaseSpeedX(self):
        self.speed_x = -1 #self.speed_x - self.increment_value_x
        self.engine.executeChangesNow()
    
    # Move Left
    def leftSpeedY(self):
        self.speed_y = -1 #self.speed_y - self.increment_value_y
        self.engine.executeChangesNow()
    
    # Move Right
    def rightSpeedY(self):
        self.speed_y = 1 #self.speed_y + self.increment_value_y
        self.engine.executeChangesNow()
    
    # Cancel XMOVE
    def stopSpeedXY(self):
        self.speed_x = 0
        self.speed_y = 0
        self.engine.executeChangesNow()
    
    # Up 
    def increaseSpeedZ(self):
        self.speed_z = self.speed_z - self.increment_value_z
        self.engine.executeChangesNow()
    
    # Down
    def decreaseSpeedZ(self):
        self.speed_z = self.speed_z + self.increment_value_z
        self.engine.executeChangesNow()
    
    # Cancel Z move
    def stopSpeedZ(self):
        self.speed_z = 0
        self.engine.executeChangesNow()
    
    # Kill the Motor  
    def killMotorsNow(self):
        self.engine.killMotorsNow()
        
        
    def armAndTakeoff(self, takeoff_alt):
        print("Arming") 
        
        #self.vehicle.mode = VehicleMode("GUIDED")   

        self.vehicle.armed = True
        time.sleep(1)
    
        while not self.vehicle.armed:
            print('self.vehicle.armed: '+str(self.vehicle.armed))
            self.vehicle.armed = True
            time.sleep(1)
        
        self.vehicle.simple_takeoff(takeoff_alt)
        print("Takeoff")

        while True:
            current_hight = self.vehicle.location.global_relative_frame.alt
        
            if current_hight >= takeoff_alt * 0.95:
                print("Altitude reached")
                #commanding movement to the same location to unlock Yaw
                self.vehicle.simple_goto( self.vehicle.location.global_relative_frame)
                break
            time.sleep(1)
    
    # Return to Launch 
    def goHome(self, rtl_alt):
        print('Going Home')
        self.vehicle.mode = VehicleMode("GUIDED")

        for _ in range(0,10):
            self.increaseSpeedZ()
            time.sleep(0.5)
        
        while True:
            current_high = self.vehicle.location.global_relative_frame.alt
        
            if current_high >= rtl_alt * 0.95:
                print("Safe RTL Altitude reached")
                self.vehicle.mode = VehicleMode("RTL")
                break
            time.sleep(1)
    
    # Land
    def land(self):
        print("Landing")
        self.vehicle.channels.overrides = {}
        self.vehicle.mode = VehicleMode("LAND")
        
    def loiter(self):
        self.vehicle.channels.overrides['3'] = 1500

        
        
        