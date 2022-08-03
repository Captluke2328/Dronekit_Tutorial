from dronekit import *

'''
    ## This is how to port forward data from Mavproxy (Ground Stations) to Copter (IP address)
    10.60 address is from ifconfig of the connected wifi, to enable this run:
    
    USING USB  : mavproxy.py --master=/dev/ttyACM0 --out=udp:10.60.216.198
    USING UART : mavproxy.py --master=/dev/ttyTHS1,921600 --out=udp:10.60.216.198:14550

'''
#connection_string = '10.60.216.198:14550'

'''Using SiTL Connection'''
#connection_string = '127.0.0.1:14550'

'''Using Uart Serial Rx->Tx and Tx-Rx connection'''
connection_string = '/dev/ttyTHS1,921600'

''' Using USB Connection '''
#connection_string = '/dev/ttyACM0'

vehicle = connect(connection_string, wait_ready = True)
print("Virtual Copter is Ready")


