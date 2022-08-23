import keyboard as kp
import collections

net= None
camera = None

def test():
    test = []
    for i in range (0,15):
        id = i+1
        cx = i+2
        cy = i+3
        w = i+4
        h = i+5
        test.append([i,id,cx,cy,w,h])
    return test

# if __name__ == "__main__":
#     check = test()
#     print(check[12][2])
    
  
mode_G = 0
mode_S = 0
count = 0
armtrue = False

def readkeyboard():
    global armtrue
    global count
    global mode_G
    global mode_S
    
    if kp.is_pressed('g'):
        mode_G +=1
        if mode_G < 2:
            print("Vehicle Mode : Guided")
            armtrue = True
            
    if kp.is_pressed('h'):
        mode_S +=1
        if mode_S < 2:
            print("Vehicle Mode : Stabilize")
    
    if kp.is_pressed('u') and armtrue:
        count +=1
        if count < 2:        
            print("Vehicle Mode : Takeoff")
               
    if kp.is_pressed('l') and armtrue:
        print("Vehicle Mode : Land")
        armtrue =False
        mode_G = 0
        mode_S = 0
        count = 0
        
    if kp.is_pressed('r'):
        print("VWarning : Reset All")
        armtrue =False
        mode_G = 0
        mode_S = 0
        count = 0
        

    
         
                 
def initdetector():
    global net, Cam
    net = "net123"
    Cam = " /dev/video"
    
def cam() -> str:
    net = "net345"
    Cam = "/dev/video"
    
    return Cam, net

def onetimeiteration():
    for i in range(1):
        print("hello")


initdetector()

x = cam()
print(x)

onetimeiteration()

while True:
    readkeyboard()