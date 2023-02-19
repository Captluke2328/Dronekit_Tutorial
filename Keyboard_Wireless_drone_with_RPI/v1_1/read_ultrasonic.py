import threading
#from gpiozero import DistanceSensor

class Ultrasonic(threading.Thread):
    def __init__(self,D,A):
        threading.Thread.__init__(self)
        self.daemon   = True
        self.engine = D
        self.altitude = A
    

    def run(self):
        self.ultrasonic = DistanceSensor(echo=25, trigger=27)
        while True:         
            print(abs(self.ultrasonic.distance * 10))       
            if self.ultrasonic.distance <= abs(4):
                self.engine.executeChangesNow(-0.5,0,0,1.5)
                self.engine.send_movement_command_YAW(0)
                                                               
                                