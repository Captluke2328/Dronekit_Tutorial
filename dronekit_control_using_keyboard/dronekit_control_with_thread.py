from sys import exc_info
import threading
from dronekit import *
from dronekit_control_using_keyboard.dronekit_config import *
import keyboard as kp
import threading
from time import sleep
from dronekit_engine import *

class dronekitControlThread(threading.Thread):
    def __init__(self,drone):
        threading.Thread.__init__(self)
        self.daemon = True
        self.drone = drone
        self.isActive = True
                
        # self.engine = Engine(drone)
        
        #print(self.drone.location.global_relative_frame)
       
    def run(self):
        
        while(self.isActive):
            try:
                pass
                #if kp.is_pressed('UP'):
                    #self.engine.armAndTakeoff(10)
                    #print("Takeoff")  
                    
                # elif kp.is_pressed('DOWN'):
                #     self.engine.land(self)
                #     print("Landing")
                
                # if kp.is_pressed('LEFT'):
                #     self.engine.left(self)
                #     print("LEFT")
                    
                # elif kp.is_pressed('RIGHT'):
                #     self.engine.right(self)
                #     print("RIGHT")
                    
                # if kp.is_pressed('w'):
                #     self.engine.forward(self)
                #     print("Forward")
                #     sleep(2)
                    
                # elif kp.is_pressed('s'):
                #     self.engine.backward(self)
                #     print("Backward")
                #     sleep(2)
                    
                # if kp.is_pressed('a'):
                #     self.engine.rotate(self,-1,180)
                #     print("Rotate Left")
                #     sleep(2)
                    
                # elif kp.is_pressed('d'): 
                #     self.engine.rotate(self,1,180)
                #     print("Rotate Right")
                #     sleep(2)
                    
                # if kp.is_pressed('q'):
                #     print("RTL")
                #     self.engine.goinghome(self)
                #     sleep(1)
                    
            except Exception as e:
                print("Failed to send command")
            
    def stop(self):
        self.isActive = False
            
            
        

            
            
        
    