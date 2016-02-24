## representation d'une map
# C'est un tableau n x n, et chaque case de ce tableau
# est une liste [indice_sol,objet_animal]
# indice_sol = 0,1,2 = sol, eau, herbe (ou potentiellement des objets)
# objet_animal = instance de la classe concernee

# In [16]: a = Animal('gerard')
# In [17]: L = [0,a]
# In [18]: L2  =[0,0]
# In [19]: L2[1] = L[1]
# In [20]: L[1] = 0
# In [21]: L2
# Out[21]: [0, <__main__.Animal at 0x1097350b8>]
# In [22]: L2[1].n
# Out[22]: 'gerard'
# In [23]: a
# Out[23]: <__main__.Animal at 0x1097350b8>


## truc utile : 
# a = np.empty((50,50),dtype=object)
# a[3,2] = Case()

## array-numpy.tolist()
# pour la vision aux frontieres, 2 solutoion : 
# 1) riviere geante entourant la map de la taille de la vision max des animaux
# 2) en dehors c'est le brouillard de guerre, si voisinnage renvoi [], on diminie les visions de 1
# jusqu'a obtenir un array contenant de vraies infos (onreduit leur vision aux frontieres)

import numpy as np
from math import sqrt

mappy = [
    [[0,None],[0,None],[0,None],[0,None],[0,None],[1,None]],
    [[1,None],[1,None],[0,None],[0,None],[0,None],[1,None]],
    [[0,None],[0,None],[0,None],[1,None],[0,None],[0,None]],
    [[0,None],[1,None],[1,None],[0,None],[0,None],[1,None]],
    [[0,None],[1,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[1,None],[0,None],[0,None],[0,None],[0,None]]
]

mappy2 = [
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[0,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[1,None],[1,None],[1,None],[0,None]]
]

class Map:

    def __init__(self, MAP):
        self.MAP = MAP
        self.dim = len(MAP)
        
    # je suppose pr le moment qu'un n'y a qu'un animal par case

        
    def infos(self,position):
        return self.MAP[position[0],position[1]] # ou alors pk pas surcharger __getitem__()
        
    # sol = 0
    # herbe = 1
    # eau = 2
        
    # retourne un array vide si on est au bord et que la vision ne va pas sufissament loin
    def voisinnage(self,position,vision):
        # position est un tuple(x,y)
        # vision est un int 
        Px = position[0]
        Py = position[1]
        V = self.MAP[Px-vision:Px+vision+1,Py-vision:Py+vision+1]
        return V
        
    def deplacer(self,position,position2):
        # position est un tuple (x,y) 
        # position2 est un tuple (x2,y2)
        Px = position[0]
        Py = position[1]
        Dx = position2[0]
        Dy = position2[1]    
        self.MAP[Dx,Dy][1] = self.MAP[Px,Py][1]
        self.MAP[Px,Py][1] = Rien()
        
    def suppression(self,position):
        # position est un tuple (x,y)
        Px = position[0]
        Py = position[1]
        self.MAP[Px,Py][1] = Rien()
        
    def distance_max(self):
        xmin = 0
        ymin = 0
        xmax = len(self.MAP)
        ymax = len(self.MAP)
        Dmax = sqrt((xmax-xmin)**2+(ymax-ymin)**2)
        return (Dmax)
        
    def distance(self,position,position2):
        # position est un tuple(x,y)
        # position2 est un tuple (x2,y2)
        Px = position[0]
        Py = position[1]
        Dx = position2[0]
        Dy = position2[1]
        Dist = sqrt((Dx-Px)**2+(Dy-Py)**2)
        return (Dist)

