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
    