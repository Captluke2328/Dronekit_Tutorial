from dronekit import *
from dronekit_config import *
from dronekit_control_without_thread import *

from time import sleep
        
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
            
            # Using Thread - which is not working now
            #control = dronekitControlThread(drone)
            #control.start()
            
            # Without using Thread
            control = dronekitControlwithoutThread(drone)
            control.control()
            
        except Exception as e:
            print(str(e))
            
    print("Drone Offline")
            
            
        
    