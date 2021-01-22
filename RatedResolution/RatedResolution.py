def RatedResolution(image,size):
    max = 0
    min = len(image)
    for i in range(len(image)):
        count = 0
        for j in range(len(image[0])):
            if image[i][j] == '1':
                temp_max = j/2
                count += 1
                temp_min = temp_max - count + 1
                if temp_min < min:
                    min = temp_min
                if temp_max > max:
                    max = temp_max
    if min == len(image) and max == 0:
        return 0
    return (float(size)/(max-min))

for i in range(6):
    file = open("figure"+str(i+1)+".txt")
    size = file.readline()
    image = file.readlines()[1:]
    file.close()
    result = RatedResolution(image,size)
    print("figure", i+1, "- rated resolution: ", result)
    
