from dronekit import *
import socket
from time import sleep
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
    
    
def launch_seq(altitude):
    # Poll the vehicle until armable
    while not vehicle.is_armable == True:
        print(f"Performing Pre-Arm Checks....")
        sleep(2)
        
    print("Armable")

    # Set mode into GUIDED
    vehicle.mode = VehicleMode("GUIDED")
    
    # Arm the vehicle. Poll until True
    vehicle.armed = True
    
    while not vehicle.mode.name == "GUIDED" and not vehicle.armed:
        print("Getting ready to take off ....")
        sleep(2)
    
    # Pass a traget altitude
    vehicle.simple_takeoff(altitude)
    
    # Poll until the altitude is reached
    while True:
        # Altitude indicator
        print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
        
        # Break and return when within 5% of target altitude
        if vehicle.location.global_relative_frame.alt >= altitude*0.95:
            print("Reached target altitude\n")
            break
        sleep(1)    
    
def goto_location():
    location = LocationGlobalRelative(-35.36311304, 149.16775127,10)  # latitude, longtitude and altitude (we use 10 meter for horizontal flat travel)
    vehicle.simple_goto(location, groundspeed=50) # in meters/second
    time.sleep(10)
    #vehicle.mode = VehicleMode("RTL")
    #print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
    
    print(vehicle.location.global_relative_frame.lat, location.lat)
    #if (vehicle.location.global_relative_frame.alt == location.alt) and (vehicle.location.global_relative_frame.lon == location.lon):
    #    print("Equal")
  
    vehicle.close()

if __name__ == "__main__":
    launch_seq(10)
    while True:
        goto_location()