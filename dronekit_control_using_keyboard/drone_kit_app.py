from dronekit import *
from dronekit_config import *
from dronekit_control import *

from time import sleep

from dronekit_control_using_keyboard.dronekit_control import dronekitControl
        
if __name__ == '__main__':
    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            print(str(e))
            sleep(2)
            
    while drone.is_active:
        try:
            
            # Without using Thread
            control = dronekitControl(drone)
            control.control()
            
        except Exception as e:
            print(str(e))
            
    print("Drone Offline")
            
            
        
    