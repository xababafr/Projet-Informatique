## representation d'une map
# C'est un tableau n x n, et chaque case de ce tableau
# est une liste [indice_sol,objet_animal]
# indice_sol = 0,1,2 = sol, eau, herbe (ou potentiellement des objets)
# (avec le polymorphisme c'est meme surement plus interessant d'avoir des objets)
# objet_animal = instance de la classe concernee

# L = [0,Animal()]
# type(L[1]) == Animal renvoi True donc easy de check le type d'un animal
# del(L[1]) fais que l'on obtient juste une liste de taille 1, donc
# il faudra après le del de animal (pour la mort) remplacer par 0
# quand on change un animal de position, je suis pas sur que changer une case en [x,0] et la nouvelle en [x,Animal]
# va conserver le meme animal, et non pas une "copie" ==> pointeurs?! (apres si c'est pas genant OSEF)
# creer une classe Rien qui permettrait le polymophisme?

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

#apparamment pas besoin de pointeurs
#peut etre plusieurs animaux par case

# ou alors si on se sert des refenrences?? en tout cas, il serait pratique d'avoir un objet case

#Créer une méthode ""suppression""
#Créer une méthode ""deplacer""
#Créer une méthode ""voisinage""
#Créer une méthode distance_max
#Créer une méthode ""distance""

## truc utile : 
# a = np.empty((50,50),dtype=object)
# a[3,2] = Case()
# voisinnage : a[2:5,1:4] !!!! pratique

# UN ARRAY NUMPY SERAIT + PRATIQUE

from tkinter import *
import numpy as np

class Map:

    def __init__(self, MAP):
        self.MAP = MAP
        self.dim = len(MAP)
        
    # je suppose pr le moment qu'un n'y a qu'un animal par case

        
    def infos(self,x,y):
        return self.MAP[x,y] # ou alors pk pas surcharger __getitem__()
        
    # sol = 0
    # herbe = 1
    # eau = 2
        
## Méthodes reliées à la Class Animal

def voisinage(self,position,vision):
    # position est un tuple(x,y)
    # vision est un int 
    Px = position[0]
    Py = position[1]
    V = np.MAP[Px-vision:Px+vision+1,Py-vision:Py+vision+1]
    return V
    
def deplacer(self,position,position2):
    # position est un tuple (x,y) 
    # position2 est un tuple (x2,y2)
    Px = position[0]
    Py = position[1]
    Dx = position2[0]
    Dy = position2[1]    
    MAP[Dx,Dy][1] = MAP[Px,Py][1]
    MAP[Px,Py][1] = Rien()
    
def suppression(self,position):
    # position est un tuple (x,y)
    Px = position[0]
    Py = position[1]
    MAP[Px,Py][1] = Rien()
    
def distance_max():
    xmin = 0
    ymin = 0
    xmax = len(MAP)
    ymax = len(MAP)
    Distmax = sqrt((xmax-xmin)**2+(ymax-ymin)**2)
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

