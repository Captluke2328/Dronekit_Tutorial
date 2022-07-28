from dronekit import *
import socket 
from time import sleep
from dronekit_engine import *
from dronekit_control_tab import * 

class Drone:
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
                
        self.is_active = True 
        self.control_tab = controlTab(self)
        
        # Return the drone class - used for non thread engine
        #self.engine = Engine(self)
    