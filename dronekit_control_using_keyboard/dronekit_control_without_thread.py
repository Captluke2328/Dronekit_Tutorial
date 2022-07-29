from sys import exc_info
from dronekit_config import *
from dronekit_engine import *
import keyboard as kp
from time import sleep
from dronekit_control_tab import *

class dronekitControlwithoutThread():
    def __init__(self,drone):
        self.daemon = True
        self.drone = drone
        self.isActive = True
        self.control_tab = drone.control_tab
        
    def control(self):
        while (self.isActive):
        #delay = 1
            try:             
                if kp.is_pressed('UP'):
                    self.control_tab.armAndTakeoff(10)
                    print("Takeoff") 
                    return
                    
                    #self.drone.engine.armAndTakeoff(10)
                    #self.engine.armAndTakeoff(10)
                    #sleep(delay)  
                    
                elif kp.is_pressed('DOWN'):
                    self.control_tab.land()
                    print("Landing")    
                    return
                    
                    #self.drone.engine.land()
                    #self.engine.land()
                    #sleep(delay)
                
                if kp.is_pressed('LEFT'):
                    self.control_tab.leftSpeedY()
                    print("LEFT")
                    return
                    
                    #self.drone.engine.left()
                    #self.engine.left()
                    #sleep(delay)
                    
                elif kp.is_pressed('RIGHT'):
                    self.control_tab.rightSpeedY()
                    print("RIGHT")
                    return

                    #self.drone.engine.right()
                    #self.engine.right()
                    #sleep(delay)
                    
                if kp.is_pressed('w'):
                    self.control_tab.increaseSpeedX()
                    print("Forward")
                    return

                    #self.drone.engine.forward()
                    #self.engine.forward()
                    #sleep(delay)
                    
                elif kp.is_pressed('s'):
                    self.control_tab.decreaseSpeedX()
                    print("Backward")
                    return

                    #self.engine.backward()
                    #sleep(delay)
                    
                if kp.is_pressed('a'):
                    self.control_tab.rotateLeft(45)
                    print("Rotate Left")
                    return

                    #self.drone.engine.rotate(-1,180) 
                    #self.engine.rotate(-1,180)
                    #sleep(delay)
                    
                elif kp.is_pressed('d'): 
                    self.control_tab.rotateRight(45)
                    print("Rotate Right")
                    return

                    #self.drone.engine.rotate(1,180)
                    #self.engine.rotate(1,180)
                    #sleep(delay)
                    
                if kp.is_pressed('q'):
                    self.control_tab.goHome(15)
                    print("RTL")
                    return
                
                    #self.drone.engine.goinghome()
                    #self.engine.goinghome()
                    #sleep(delay)
                    
                elif kp.is_pressed('e'):
                    self.control_tab.stopMovement()
                    print("Stop movement")
                    
                if kp.is_pressed('x'):
                    self.control_tab.loiter()
                    print("Set Loiter")
                    
            except Exception as e:
                print("Failed to send command")
                
        
        

