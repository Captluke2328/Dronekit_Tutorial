from dronekit import *

'''
    This script used to read Channel values from RC Tx.
    Below channel represent its functionality
    
    Ch1 =Roll, Ch 2=Pitch, Ch 3=Throttle, Ch 4=Yaw
    
'''
#connection_string = '10.60.216.198:14550'

'''Using SiTL Connection'''
connection_string = '127.0.0.1:14550'

'''Using SiTL Connection from  different computer - This IP address below to receiver device for example RPI
   This IP address is based on given ZeroTier IP address'''
#connection_string = '192.168.195.204:14551'
#connection_string = '192.168.195.204:14553'
#connection_string = '192.168.195.190:14553'

'''Using Uart Serial Rx->Tx and Tx-Rx connection'''
#connection_string = '/dev/ttyTHS1,921600'

''' Using USB Connection '''
#connection_string = '/dev/ttyACM0'

#Connect to Vehicle
vehicle = connect(connection_string, wait_ready = True)
print("Virtual Copter is Ready")

#Get all original channel values (before override)
print("Channel values from RC Tx:", vehicle.channels)

# Access channels individually
print("Read channels individually:")
print(" Ch1: %s" % vehicle.channels['1'])
print(" Ch2: %s" % vehicle.channels['2'])
print(" Ch3: %s" % vehicle.channels['3'])
print(" Ch4: %s" % vehicle.channels['4'])
print(" Ch5: %s" % vehicle.channels['5'])
print(" Ch6: %s" % vehicle.channels['6'])
print(" Ch7: %s" % vehicle.channels['7'])
print(" Ch8: %s" % vehicle.channels['8'])
print("Number of channels: %s" % len(vehicle.channels))

# Override channels
print("\nChannel overrides: %s" % vehicle.channels.overrides)

# print("Set Ch2 override to 200 (indexing syntax)")
# vehicle.channels.overrides['2'] = 200
# print(" Channel overrides: %s" % vehicle.channels.overrides)
# print(" Ch2 override: %s" % vehicle.channels.overrides['2'])

# print("Set Ch3 override to 300 (dictionary syntax)")
# vehicle.channels.overrides = {'3':300}
# print(" Channel overrides: %s" % vehicle.channels.overrides)

# print("Set Ch1-Ch8 overrides to 110-810 respectively")
# vehicle.channels.overrides = {'1': 110, '2': 210,'3': 310,'4':4100, '5':510,'6':610,'7':710,'8':810}
# print(" Channel overrides: %s" % vehicle.channels.overrides) 

# Clear override by setting channels to None
# print("\nCancel Ch2 override (indexing syntax)")
# vehicle.channels.overrides['2'] = None
# print(" Channel overrides: %s" % vehicle.channels.overrides) 

# print("Clear Ch3 override (del syntax)")
# del vehicle.channels.overrides['3']
# print(" Channel overrides: %s" % vehicle.channels.overrides) 

# print("Clear Ch5, Ch6 override and set channel 3 to 500 (dictionary syntax)")
# vehicle.channels.overrides = {'5':None, '6':None,'3':500}
# print(" Channel overrides: %s" % vehicle.channels.overrides) 

# print("Clear all overrides")
# vehicle.channels.overrides = {}
# print(" Channel overrides: %s" % vehicle.channels.overrides) 

# #Close vehicle object before exiting script
# print("\nClose vehicle object")
# vehicle.close()