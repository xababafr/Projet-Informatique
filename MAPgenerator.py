import numpy as np
import random

#(0 = herbe, 1 = eau, 2 = sol, 3 = roche)

#class Generator():
#    """
#        Classe permettant de générer la map
#    """
#       
#    def __init__(self,abscisse,ordonee,source):
    

def proptexture(h=45,e=0,s=45,r=10):
    herbe = []
    eau = []
    sol = []
    roche = []
    texture = []
    for i in range (0,h):
        herbe.append(0)
        #print (herbe)
    for i in range (0,e):
        eau.append(1)
    #print (eau)
    for i in range (0,s):
        sol.append(2)
        #print (sol)
    for i in range (0,r):
        roche.append(3)
        #print (roche)
    texture = herbe+eau+sol+roche
    return texture

#def source(e=10):
#    eau = []
#    for i in range (0,e):
#        eau.append(1)
#    return eau
    

def genererMap(x=20,y=20,source=5):
    texture = proptexture()
    #print (random.choice(texture))
    absc = 0
    ordo = 0
    alea = 0
    case_proche = []
    MAP=np.zeros((x,y),int)
### On genere la carte avec les textures herbe =0, sol =2 et roche =3
    for i in range (0,x-1):
        for j in range (0,y-1):
            if MAP[i][j] == 0 :
                MAP[i][j] = random.choice(texture)
### On genere les sources d'eau
    for k in range (0,source):
        absc = random.randint(0,x-1)
        ordo = random.randint(0,y-1)
        MAP[absc][ordo]=1
## On dévellope les sources d'eau
    devS=6
    for k in range (0,devS):
        for i in range (0,x):
            for j in range (0,y):
                if MAP[i][j] == 1 :
                    #case_proche = [[i+1,j],[i,j+1],[i-1,j],[i,j-1],[i+1,j+1],[i-1,j-1],[i+1,j-1],[i-1,j+1]        
                    #print(case_proche)                     #MAP[case_proche[l[0]]][case_proche[l[1]]]=1
                    alea = random.randint(0,100)
                    if alea>85 and i+1<x:                   #del case_proche[0:4:6]     #case_proche.remove[0,4,6]
                        MAP[i+1][j]=5 
                    alea = random.randint(0,100)
                    if alea>85 and i+1<x and j+1<y:         #del case_proche[2:5:7]     #case_proche.remove[2,5,7]
                        MAP[i+1][j+1]=5 
                    alea = random.randint(0,100)
                    if alea>85 and i+1<x and j-1>0:         #del case_proche[3:5:6]     #case_proche.remove[3,5,6]
                        MAP[i+1][j-1]=5 
                        
                    alea = random.randint(0,100)
                    if alea>90 and i-1>0:                   #del case_proche[1:4:7]     #case_proche.remove[1,4,7]
                        MAP[i-1][j]=5
                    alea = random.randint(0,100)
                    if alea>90 and i-1>0 and j+1<y:
                        MAP[i-1][j+1]=5
                    alea = random.randint(0,100)
                    if alea>90 and i-1>0 and j-1>0:
                        MAP[i-1][j-1]=5
                    
                    alea = random.randint(0,100)
                    if alea>90 and j-1>0:
                        MAP[i][j-1]=5
                    alea = random.randint(0,100)
                    if alea>90 and j+1<y:     
                        MAP[i][j+1]=5
                for u in range (0,x):
                    for v in range (0,y):
                        if MAP[u][v] == 5:
                            MAP[u][v] = 1
    herbe =0
    eau = 0
    sol = 0
    roche = 0                        
    for i in range (0,x):
       for j in range (0,y):
           if MAP[i][j] == 0 :
               herbe +=1
           if MAP[i][j] == 1 :
               eau +=1
           if MAP[i][j] == 2 :
               sol +=1
           if MAP[i][j] == 3 :
               roche +=1
    print(herbe, eau, sol, roche)
    return MAP

    
        