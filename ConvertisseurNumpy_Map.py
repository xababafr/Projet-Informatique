import numpy as np

class Rien():
    pass

def tableauToMap(array):
    rien = Rien()
    r = []
    l = len(array)
    for i in range(l):
        r.append([])
        for j in range(l):
            r[i].append([array[i,j],rien])
    return np.array(r)
    
 #test   
m = np.array([
    [1,2,1,0],
    [0,0,3,1],
    [1,1,1,1],
    [2,2,2,2]
])

def mapToTableau(map):
    r = []
    l = len(map)
    for i in range(l):
        r.append([])
        for j in range(l):
            r[i].append(map[i,j][0])
    return np.array(r)
 
#test
R = Rien()
    
m2 = np.array([
    [[1,R],[0,R]],
    [[0,R],[1,R]]
])