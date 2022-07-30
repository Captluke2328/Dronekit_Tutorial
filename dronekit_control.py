from dronekit import *
import keyboard as kp
import socket
from time import sleep
from dronekit_engine import Engine

class control():
    def __init__(self):      
        try:
            self.connection_string = '127.0.0.1:14550'
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")
                 
        # Bad TCP connection
        except socket.error:
            print("No server exist")

        # Bad TTY connection
        except OSError:
            print("No serial exists !")
            
        # API Error
        except APIException:
            print("Timeout")

        # Other Error
        except Exception:
            print("Some other error")
               
        ## This is observer callback function to check if mode change to GUIDED
        ## @allow to monitor the changes and update
        @self.vehicle.on_attribute('mode')
        def mode_callback(self,attr_name, value):
            print(f">> Mode Updated: {value}")

        ## We will not let the script to continue unless it changes to GUIDED
        self.vehicle.mode = VehicleMode("GUIDED")
        while not self.vehicle.mode.name == "GUIDED":
            sleep(1)
            

    def getKeyboardInput(self):
        lr,fb,ud,yv = 0,0,0,0,
        
        if kp.is_pressed('UP'):
            fb = Engine.armAndTakeoff(self,10)
            print("Takeoff")
            
        elif kp.is_pressed('DOWN'):
            fb = Engine.land(self)
            print("Landing")
            sleep(2)
            
        if kp.is_pressed('LEFT'): 
            lr = Engine.left(self)
            sleep(5)

        elif kp.is_pressed('RIGHT'):
            lr = Engine.right(self)
            sleep(5)
    
        if kp.is_pressed('w'):
            ud = Engine.forward(self)
            print("Forward")
            sleep(2)
            
        elif kp.is_pressed('s'):
            ud = Engine.backward(self)
            print("Backward")
            sleep(2)
            
        if kp.is_pressed('a'):
            yv = Engine.rotate(self,-1,180)
            print("Rotate Left")
            sleep(2)
            
        elif kp.is_pressed('d'): 
            yv = Engine.rotate(self,1,180)
            print("Rotate Right")
            sleep(2)
            
        if kp.is_pressed('q'):
            print("RTL")
            Engine.goinghome(self)
            sleep(1)
            
        if kp.is_pressed('e'): pass
    
    
        #return [lr,fb,ud,yv]

if __name__ == '__main__':
    init = control()
    while True:
        vals = init.getKeyboardInput()

    
    # def armAndTakeoff(altitude):
#     # Poll the vehicle until armable
#     while not vehicle.is_armable == True:
#         print(f"Performing Pre-Arm Checks....")
#         sleep(2)
        
#     print("Armable")

#     # Set mode into GUIDED
#     vehicle.mode = VehicleMode("GUIDED")
    
#     # Arm the vehicle. Poll until True
#     vehicle.armed = True
    
#     while not vehicle.mode.name == "GUIDED" and not vehicle.armed:
#         print("Getting ready to take off ....")
#         sleep(2)
    
#     # Pass a traget altitude
#     vehicle.simple_takeoff(altitude)
    
#     # Poll until the altitude is reached
#     while True:
#         # Altitude indicator
#         print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
        
#         # Break and return when within 5% of target altitude
#         if vehicle.location.global_relative_frame.alt >= altitude*0.95:
#             print("Reached target altitude\n")
#             break
#         sleep(1)   
  
# def land():
#     vehicle.mode = VehicleMode("LAND")
 
# def forward():
#     msg = vehicle.message_factory.set_position_target_local_ned_encode(
#     0,       # time_boot_ms (not used)
#     0, 0,    # target system, target component
#     mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
#     0b0000111111000111, # type_mask (only positions enabled)
#     0, 0, 0,
#     30, 0 ,0,
#     #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
#     0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
#     0, 0)
    
#     vehicle.send_mavlink(msg)
#     vehicle.flush()
    
# def backward():
#     msg = vehicle.message_factory.set_position_target_local_ned_encode(
#     0,       # time_boot_ms (not used)
#     0, 0,    # target system, target component
#     mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
#     0b0000111111000111, # type_mask (only positions enabled)
#     0, 0, 0,
#     -30, 0 ,0,
#     #self.control_tab.speed_x, self.control_tab.speed_y, self.control_tab.speed_z, # x, y, z velocity in m/s
#     0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
#     0, 0)
#     vehicle.send_mavlink(msg)
#     vehicle.flush()

# def rotateleft(direction, rotation_angle):
#     msg = vehicle.message_factory.command_long_encode(
#     0, 0,    # target system, target component
#     mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
#     0, #confirmation
#     rotation_angle,  # param 1, yaw in degrees
#     1,          # param 2, yaw speed deg/s
#     direction,          # param 3, direction -1 ccw, 1 cw
#     True, # param 4, 1 - relative to current position offset, 0 - absolute, angle 0 means North
#     0, 0, 0)    # param 5 ~ 7 not used
#     vehicle.send_mavlink(msg)
#     vehicle.flush()
     
# def goinghome():
#     vehicle.mode = VehicleMode("RTL")
    
    

        
