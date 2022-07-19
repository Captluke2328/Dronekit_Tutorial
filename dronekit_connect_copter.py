from dronekit import *

connection_string = '127.0.0.1:14550'
vehicle = connect(connection_string, wait_ready=True)
print("Virtual Copter is Ready")

