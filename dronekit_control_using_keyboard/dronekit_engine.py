import time, threading, logging
from dronekit import VehicleMode, Command
from pymavlink import mavutil
from time import  sleep

class Engine ():
    def __init__(self,drone):
        self.drone = drone
        self.vehicle = drone.vehicle
        print("Engine has started")    

        
    def forward(self):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111000111, # type_mask (only positions enabled)
        0, 0, 0,
        30, 0 ,0,
        #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)
        
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def backward(self):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111000111, # type_mask (only positions enabled)
        0, 0, 0,
        -30, 0 ,0,
        #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def right(self):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111000111, # type_mask (only positions enabled)
        0, 0, 0, #altitude
        0, 10 ,0,
        #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def left(self): 
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111000111, # type_mask (only positions enabled)
        0, 0, 0, #altitude
        0, -10 ,0,
        #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def rotate(self,direction, rotation_angle):
        msg = self.vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        rotation_angle,  # param 1, yaw in degrees
        10,          # param 2, yaw speed deg/s #default 1
        direction,          # param 3, direction -1 ccw, 1 cw
        True, # param 4, 1 - relative to current position offset, 0 - absolute, angle 0 means North
        0, 0, 0)    # param 5 ~ 7 not used
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def goinghome(self):
        self.vehicle.mode = VehicleMode("RTL")
        
    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
    
    def stabilize(self):
        self.vehicle.mode = VehicleMode("STABILIZE")
        
    def armAndTakeoff(self,altitude):
        # Poll the vehicle until armable
        while not self.vehicle.is_armable == True:
            print(f"Performing Pre-Arm Checks....")
            sleep(2)
        
        print("Armable")

        # Set mode into GUIDED
        self.vehicle.mode = VehicleMode("GUIDED")
            
        # Arm the vehicle. Poll until True
        self.vehicle.armed = True
    
        while not self.vehicle.mode.name == "GUIDED" and not self.vehicle.armed:
            print("Getting ready to take off ....")
            sleep(2)
    
        # Pass a traget altitude
        self.vehicle.simple_takeoff(altitude)
        
        # Poll until the altitude is reached
        while True:
            # Altitude indicator
            print(f"Altitude: {self.vehicle.location.global_relative_frame.alt}")
            
            # Break and return when within 5% of target altitude
            if self.vehicle.location.global_relative_frame.alt >= altitude*0.95:
                print("Reached target altitude\n")
                break
            sleep(1)       
