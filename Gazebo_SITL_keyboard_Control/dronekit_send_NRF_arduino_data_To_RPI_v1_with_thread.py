"""
Author : Lukas Johnny
Date : 23/8/2022
Description : This script is used to establish the connection between RPI to Arduino using RX and TX
             Arduino : Tx --Connect -- Rpi : Rx
             Arduino : Rx --Connect -- Rpi : Tx
             
             and also using Arduino port

             Before running this code do ensure to:
             1. sudo raspi-config and enable SPI
             2. disable Serial login shell connection and enable Serial interface connection
             3. go to sudo vi /boot/config.txt -last line. Disable bluetooth using this command
             "dtoverlay=disable-bt"
             4. Reboot the Pi
             8. if ttyAMAO is not in dev, please enable_uart=1 in /boot/config too.
             6. ttyAMAO is serial protocol to connect PI and Arduino
             
             This script will extract data from Arduino Receiver and send those data into RPI which
             will be read by this script. 
             
             This script will then classify those data and command Pixhawk controller to execute 
             Copter function based in MAVLink connection
             
             Below is Key input from Python and Arduino and its function
             Keyboard : Arduino : Function
               g           g     : GUIDED Mode
               h           h     : STABILIZE Mode
               UP          u     : TAKEOFF Mode
               d           d     : Go Right
               a           a     : Go Left
               w           w     : Move Front
               s           s     : Move backward
               q           q     : LAND Mode
               e           e     : Freeze
               r           r     : Reset
               LEFT        n     : Yaw left
               RIGHT       m     : Yaw Right
               
                           
"""
import socket
from time import sleep
import numpy as np
from dronekit import *
from dronekit_engine_for_RPI_with_thread import *
import keyboard as kp

class readdatafromArdtoRpi():
    
    # Connect to Copter
    def __init__(self):
        try:       
            #self.connection_string = '/dev/ttyAMA0,921600'
            #self.connection_string = '127.0.0.1:14550'
            
            '''Below IP adderess belong to current computer address taken from ZeroTier'''
            self.connection_string = '192.168.195.190:14553' 
            
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")

        except socket.error:
            print("No server exist")
        
        self.engine = Engine_Improve(self)
        self.engine.start()
        self.THRESHOLD_ALT = 0.3
        self.mode_g   = 0
        self.mode_l   = 0
        self.mode_s   = 0
        self.count    = 0
        self.takeoff = False
        self.takeoff_alt = 1.8

    # Connect to Arduino
    #def initConnection(self,portNo, baudRate):
    #    try:
    #        ser = serial.Serial(portNo, baudRate)
    #        print("Device Connected")
    #        return ser
    #    except:
    #        print("Not connected")

    # Extract data from Arduino NRF - Receiver
    #def getData(self,ser):
    #    try:
    #        data = ser.readline()
    #        data = data.decode("utf-8")
    #        data = data.split()
    #        data = data[0]
    #        return data
                 
    #    except:
    #        pass
    
    # Classifying input data from Arduino NRF - Receiver
    def getKeyboardInput(self):  

        # Set into Guided Mode    
        if (kp.is_pressed('g')):
            self.mode_g +=1        
            if self.mode_g < 2:   
                print("Vehicle Mode : Guided") 
                @self.vehicle.on_attribute('mode')
                def mode_callback(self,attr_name, value):
                    print(f">> Mode Updated: {value}")      
                            
                # We will not let the script to continue unless it changes to GUIDED
                self.vehicle.mode = VehicleMode("GUIDED")
                while not self.vehicle.mode.name == "GUIDED":
                    sleep(1)
                    
                self.mode_s   = 0
                self.mode_l   = 0
                    
                if (self.vehicle.mode.name == "GUIDED"):
                    if not self.vehicle.armed:
                        self.vehicle.armed = True
                        print("Waiting to take off")
                    
                    else:
                        # Disarm if landed
                        if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                            self.vehicle.armed = False
                            self.takeoff = False
                            print("Vehicle Mode : Disarmed")
                            
        elif (kp.is_pressed ('h')):
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")
                
            self.vehicle.mode = VehicleMode("STABILIZE")
            print("Vehicle Mode : Stabilize")
            while not self.vehicle.mode.name == "STABILIZE":
                sleep(1)
                
        # Go Up
        if (kp.is_pressed('UP')) and self.vehicle.armed:
            self.count +=1    
            if self.count < 2:     
                print("Vehicle Mode : Take Off")
                if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                    
                    self.vehicle.simple_takeoff(self.takeoff_alt)         
                    
                    while True:
                        current_high = self.vehicle.location.global_relative_frame.alt
                        print(f"Altitude : {current_high}")
                        
                        if current_high >= self.takeoff_alt * 0.98:
                            print("Altitude Reached")
                            self.takeoff = False
                            break
                        sleep(1)
                            
                    #while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
                    #    sleep(0.3)
                else:
                    if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
                        self.vehicle.mode = VehicleMode("LAND")
                        
        # Go Right
        elif (kp.is_pressed('d')) and self.vehicle.armed:
            print("Go Right")
            x,y = 0.0, 0.5 
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,      
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)

            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,z)

        # Go Left
        elif (kp.is_pressed('a')) and self.vehicle.armed:
            print("Go Left")
            x,y = 0.0, -0.5 
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,      
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)

            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,z)
            
        # Go Back
        elif (kp.is_pressed('s')) and self.vehicle.armed:
            print("Go Back")
            x, y = -0.5, 0.0  # meters
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)

            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,z)
            
        # Go Front
        elif (kp.is_pressed('w')) and self.vehicle.armed:
            print("Go Front")
            x, y = 0.5, 0.0  # meters
            z = 0
            # yaw = self.vehicle.attitude.yaw
            # self.engine.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     1,
            # )
            
            # 1st option
            #self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)
            
            # 3rd option
            self.engine.executeChangesNow(x,y,z)

        # Land   
        elif (kp.is_pressed('q')) and self.vehicle.armed:
            self.mode_l +=1
            if self.mode_l < 2:
                
                self.vehicle.armed = False
                self.takeoff = False
                self.mode_g = 0
                self.count = 0
                
                print("Vehicle Mode : Land")
                self.vehicle.channels.overrides = {}
                self.vehicle.mode = VehicleMode("LAND")
                
        # Stop Movement
        elif (kp.is_pressed('e')) and self.vehicle.armed:
            print("Vehicle Mode : Freeze")
            x,y,z = 0,0,0
            self.engine.send_global_velocity(
            x,
            y,
            z,
            1, 
            )
            
             # 1st option
            self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)

            # 3rd option
            #self.engine.executeChangesNow(x,y,z)
            
        # Yaw Left
        elif (kp.is_pressed('LEFT')) and self.vehicle.armed:
            print("Yaw Left")
            self.engine.rotate(-20)
            #self.engine.send_movement_command_YAW(-20)

        # Yaw Right
        elif (kp.is_pressed('RIGHT')) and self.vehicle.armed:
            print("Yaw RIGHT")
            self.engine.rotate(20)
            #self.engine.send_movement_command_YAW(20)

        elif (kp.is_pressed('r')):
            self.mode_s +=1
            if self.mode_s < 2:
                print("Warning : Reset Vehicle State")
                self.mode_g = 0
                self.mode_l = 0
                self.count  = 0

        # Stay hovering
        #elif (kp =='f') and self.vehicle.armed and self.takeoff:
        #    print("Vehicle Mode : Hovering")
        #    x,y,z = 0,0,0
        #    self.engine.send_global_velocity(
        #    x,
        #    y,
        #    z,
        #    2, 
        #    )
            
            # 1st option
        #    self.engine.send_global_velocity(0, 0, 0, 1)
            
            # 2nd option
            #self.engine.send_movement_command_XYA(x,y,self.takeoff_alt)

    #sleep(0.28)

if __name__ == "__main__":
    init = readdatafromArdtoRpi()
    
    """use tx and rx port connect to Arduino"""
    #ser = init.initConnection("/dev/ttyAMA0", 9600)

    """use usb connection port connect to Arduino"""
   # ser = init.initConnection("/dev/ttyUSB0", 9600)

    while True:
        #receivedata = init.getData(ser)
        #vals = init.getKeyboardInput(receivedata)
        vals = init.getKeyboardInput()

