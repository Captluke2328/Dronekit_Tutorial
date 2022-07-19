from dronekit import *
import socket

try:
    connection_string = '127.0.0.1:14550'
    vehicle = connect(connection_string, wait_ready=True)
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
@vehicle.on_attribute('mode')
def mode_callback(self,attr_name, value):
    print(f">> Mode Updated: {value}")

## We will not let the script to continue unless it changes to GUIDED
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name == "GUIDED":
    time.sleep(1)



