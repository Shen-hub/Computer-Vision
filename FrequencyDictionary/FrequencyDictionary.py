import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import morphology
from skimage.filters import threshold_otsu, threshold_triangle
from skimage.measure import label, regionprops


def lakes(image):
    B=~image
    BB=np.ones((B.shape[0]+2, B.shape[1]+2))
    BB[1:-1,1:-1]=B
    return (np.max(label(BB))-1)

def has_vline(image):
    lines= np.sum(image,0) // image.shape[0]
    return 1 in lines

def has_bline(image):
    lines = np.sum(image, 1) // image.shape[1]
    return 1 in lines

def has_bay(image):
    b=~image
    bb=np.zeros((b.shape[0]+1, b.shape[1])).astype("uint8")
    bb[:-1, :]=b
    return lakes(bb)-1

def count_bays(image):
    holes = ~image.copy()
    return np.max(label(holes))

def recognize(image):
    lc=lakes(image)
    if lc == 2:
        
        if count_bays(image) > 4:
            return '8'
        else:
            return 'B'
    if lc ==1:   
        
        bays = count_bays(image)
        if has_vline(image):
            if bays > 3:
                return '0'
            else:
                if (region.perimeter ** 2 / region.area) < 58:
                    return 'P'
                else:
                    return 'D'
        else:
            if bays < 5:
                return 'A'
            else:
                return '0'   
    if lc == 0:

        bays = count_bays(image)
        
        if bays == 2:
            return '/'
        
        if has_vline(image):

            if np.all(image == 1):
                return '-'

            if bays == 5:
                return '*'
            return '1'

        if bays == 5:
            if has_bline(image):
                return '*'
            return 'W'

        if count_bays(image[2:-2, 2:-2]) == 5:
            return '*'
        else:
            return 'X'    
    
    
    return None


image = plt.imread("symbols.png")
image=np.sum(image,2)
image[image>0]=1

labeled= label(image)
print(np.max(labeled))

regions = regionprops(labeled)
d={}
for region in regions:
    symbol=recognize(region.image)
    if symbol not in d:
        d[symbol]=1
    else:
        d[symbol] +=1
        
print("Total number of symbols: ", sum(d.values()))
print(d)
        
for key in d.keys():
    percent = d.get(key) / sum(d.values()) * 100      
    print(key," - ", percent, "%")

#plt.figure()
#plt.subplot(121)
#plt.imshow(image)
#plt.subplot(122)
#plt.imshow(labeled)
#plt.show()
