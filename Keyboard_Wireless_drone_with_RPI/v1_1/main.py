from config import *
from read_ultrasonic import *
import keyboard as kp
import threading

altitude = 1.5
  
if __name__ == "__main__":
    
    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            print(str(e))
            sleep(2)
    
    ultrasonic = Ultrasonic(drone,altitude)
    ultrasonic.start()
    
    while drone.is_active:
        key = keyboard.read_key()
        run = threading.Thread(target=getKeyboardInput,args=(key))
        run.start()
        
        
        