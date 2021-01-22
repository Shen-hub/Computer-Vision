import cv2
import numpy as np
import random
import time
from array import array 

def set_upper(x):
    global colorUpper
    colorUpper[0] = x

def set_lower(x):
    global colorLower
    colorLower[0] = x
    
def ball(lower, upper):
    set_lower(lower)
    set_upper(upper)
                        
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        (curr_x, curr_y), radii = cv2.minEnclosingCircle(c)
        if radii > 10:
            cv2.circle(frame, (int(curr_x), int(curr_y)),
                       int(radii), (0,255,255), 2)
        return(curr_x)
    #return 0
    
def randomColors():
    colors = ["red", "green", "blue"]
    random.shuffle(colors)
    print(colors)
    return colors

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

colorLower = np.array([0,100,100],dtype = "uint8")
#red - 7/0
#blue - 124/84
#green - 86/30
colorUpper = np.array([255,255,255],dtype = "uint8")
colorBalls = randomColors()


while cam.isOpened():
    ret,frame = cam.read()
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    x = {}
    xRed = ball(0,7)
    if xRed is not None:
        x[xRed] = "red"
    xBlue = ball(84,124)
    if xBlue is not None:
        x[xBlue] = "blue"
    xGreen = ball(35,86)
    if xGreen is not None:
        x[xGreen] = "green"
        
    sorted(x)
    x_arr = array.fromlist(x)
    
    print(colorBalls)
    print(x_arr)
    #print([x[key] for key in sorted(x)])
    print(np.array_equal(colorBalls, x))
    
    if np.array_equal(colorBalls, x) == True:
        print("Очередность мячей совпала.")
        time.sleep(2)
        break;
    
    
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
