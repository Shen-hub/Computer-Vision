import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import morphology 

all_objects =[]
image = np.load('ps.npy.txt')

first = np.ones((4,6)) 
all_objects.append(first)

second = first 
second[:2,2:4] = 0
all_objects.append(second)

third = np.flip(second)
all_objects.append(third) 

fourth = np.transpose(second)
all_objects.append(fourth) 

fifth = np.transpose(third)
all_objects.append(fifth) 

count_objects = []

for i in range(5):
    new_objects = morphology.binary_hit_or_miss(image, all_objects[i])
    count_objects.append(np.sum(new_objects))
    print(f'Count of objects {i} - {count_objects[i]}')

print(f'All objects - {np.sum(count_objects)}')
