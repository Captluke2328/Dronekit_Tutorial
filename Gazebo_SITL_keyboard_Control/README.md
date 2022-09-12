
## This Userguide explain on how to run this script using Gazebo and SITl 

### On Ubuntu with Gazebo Installed, run following command to launch Gazebo software
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world

### On Ubuntu with SiTl installed, run following command to launch SiTl 
cd ~/ardupilot/ArduCopter/

sim_vehicle.py -v ArduCopter -f gazebo-iris --console --map --out 192.168.195.190:14553 (This IP address is referring to drone IP address or our RaspberryPi)
 
 ### On Desktop or RPI, git clone this Directory and amend the changes as follow
 
 open dronekit_send_NRF_arduino_data_To_RPI_v1_with_thread.py and change "connection_string" to above address or current RaspberryPi address of our drone
 
self.connection_string = '192.168.195.190:14553'

## On Desktop or RPI, run following script

python3 dronekit_send_NRF_arduino_data_To_RPI_v1_with_thread.py

