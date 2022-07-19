from logging import raiseExceptions
from dronekit import *
import socket
from time import sleep
import math

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
    vehicle.simple_goto(location, groundspeed=20) # in meters/second
    time.sleep(30)
    # vehicle.mode = VehicleMode("RTL")
    # print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
    # vehicle.close()

launch_seq(10)
goto_location()

# Distance from original location to North or East Distance
# Return a locationGlobal object that contain lat/lon 'dNorth' and 'dEast' metres from
# the specified 'original location'.
# This function is helfpul when you want to move the vehicle around specifying locations to the current
# vehicle positions.

location = LocationGlobalRelative(-35.36311304, 149.16775127,10)  # latitude, longtitude and altitude (we use 10 meter for horizontal flat travel)

def get_location_metres(original_location, dNorth, dEast):
    earth_radius=6378137.0 #Radius of "spherical" earth
    
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    
    if type(original_location) is LocationGlobal:
        targetlocation = LocationGlobal(newlat, newlon, original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation = LocationGlobalRelative(newlat, newlon, original_location.alt)
    else:
        raise Exception("Invalid location object passed")
    
    return targetlocation

# Checking proximity of our desired locations instead of using time
# aLocation1 - Our location aLocation2 - desired location
# This would be so helpful to pass our current location & desired locations
# Check if differences between our location and desired location get smaller
# Return ground distance in metre between 2 locationsGlobal objects.
# This methos is an approximation and will not be accurate over larger distance and close to the earth pole
def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong * dlong)) * 1.113195e5

# def get_bearing(aLocation1, aLocation2):
#     pass

target = get_location_metres(location,15,20) #15 metres to north and 20 meters to the east
vehicle.simple_goto(target)

distance = get_distance_metres(location, target)
print(f"Distance {distance}")

# bearing = get_bearing(location, target)
# print(bearing)


