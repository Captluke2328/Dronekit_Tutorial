from dronekit import *
import socket
from time import sleep
from control_tab import *
from engines import *
#from read_lidar import *

class Drone:
    def __init__(self):
        try:            
            '''RPI'''
            self.connection_string = '/dev/ttyAMA0,921600'

            '''Gazebo'''
            #self.connection_string = '192.168.8.146:14553'

            '''SiTL'''
            #self.connection_string = '127.0.0.1:14550'

            '''ZeroTier'''
            #self.connection_string = '192.168.8.146:14553'
            
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is ready")

        # Bad TCP connection
        except socket.error:
            print("No server exist")
        
        # API Error
        except APIException:
            print("Timeout")

        # Other Error
        except Exception:
            print("Some other error")
            
        print("Waiting to change to GUIDED Mode")

        ## This is observer callback function to check if mode change to GUIDED
        ## @allow to monitor the changes and update
        @self.vehicle.on_attribute('mode')
        def mode_callback(self,attr_name, value):
            print(f">> Mode Updated: {value}")

        ## We will not let the script to continue unless it changes to GUIDED
        #self.vehicle.mode = VehicleMode("GUIDED")
        #while not self.vehicle.mode.name == "GUIDED":
        #    sleep(1)
                        
        self.is_active   = True 
        #self.lidar      = Read_Lidar(self)
        self.engines     = Engines(self)
        self.control_tab = controlTab(self)
        

        
