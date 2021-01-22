import numpy as np

def img(filename):
    temp = []
    lines = open(filename).readlines()
    for line in lines[2:]:
        temp.append(line.split())

    return np.array(temp, dtype='int32')

def find_point(img):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x] == 1:
                return y, x

img1 = img("img1.txt")
img2 = img("img2.txt")

y1, x1 = find_point(img1)
y2, x2 = find_point(img2)

print(f'Смещение ({y2-y1};{x2-x1})')
