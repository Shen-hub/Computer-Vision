import cv2                                         
import numpy as np
from skimage.filters import threshold_mean
from mss import mss
import pyautogui
import time


tRex = cv2.imread('tRex.png',0)          
width, height = tRex.shape[::-1]

def press():
    pyautogui.keyDown('space')
    
def down():
    pyautogui.keyDown('down')
    time.sleep(0.01)
    pyautogui.keyUp('down')
    
def up():
    pyautogui.keyDown('up')
                                    
def get_img():
   with mss() as sct:                 
        monitor = {"top": 0, "left" : 0, "width": 1400, "height": 600}
        img_rgb =np.array(sct.grab(monitor))                                      
   return img_rgb
    
def find_trex(img_rgb):          
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)      #
    res = cv2.matchTemplate(img_gray,tRex,cv2.TM_CCOEFF_NORMED)    #    
    threshold = 0.8            
    try:                      
        loc = np.where(  res >= threshold)   
        position = list( zip(*loc[::-1]))[0]    
        center = position [0]+(width//2), position[1]+(height//2)      
    except:                                                              
        return False                                             
    return center 
                                                                                                                                                                                                      
def game  (center):                
    global V                  
    global zone    
    global img_rgb   
    global zone2 
    global count_of_jps
    state = 0                                                
    V = 110.0                                                                                                                                                                          
    count_of_jps = 0           
    for i in  range(100000):
        img_rgb = get_img()
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)                                                               
        thresh = threshold_mean(img_gray)        
        binary = (img_gray > thresh).astype(int)  
        x_start, x_end = center[0] + width//2, center[0] + width//2 + int(V)        
        y_start, y_end = center[1]- height//2, center[1] + height//2 - 15 
        zone = binary[y_start: y_end, x_start: x_end]
        
        yt_start, yt_end = center[1] - height//2, center[1] + height//2 - 15
        zone2 = binary[yt_start: yt_end, x_start : x_end ]   
        if  0 in zone and state == 0:            
            press()  
            count_of_jps+=1   
            V  += (8.0 /60) 
            state = 1             
        if (0 not in zone2 ) and state == 1: 
            state = 2          
            down()          
        if  (0 in zone2) and state == 2:
            state = 0
    
if __name__ == "__main__":        
    
    t = 0
    center = False
    for i in range(100000):
        center = find_trex(get_img())
        if center:
            print("FIND!")
            if t == 5:                
                game(center) 
            else:
                t+=1
                continue
