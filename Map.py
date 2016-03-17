# -*- coding: utf-8 -*-

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

class Map:

    def __init__(self, MAP,rien):
        ## à voir
        #self.MAP = np.pad(MAP,3,mode='constant',constant_values=[1,-1])
        M = []
        
        # on créé la bordure de la map avec de l'eau
        
        l = len(MAP)+6
        for i in range(l):
            L = []
            for j in range(l):
                L.append([3,rien])
            M.append(L)
        M = np.array(M)
        
        M[3:l-3,3:l-3] = MAP
        
        self.MAP = M
        
        self.dim = len(MAP)+6
        self.rien = rien
        
    # je suppose pr le moment qu'un n'y a qu'un animal par case

        
    def infos(self,position):
        return self.MAP[position[0],position[1]] # ou alors pk pas surcharger __getitem__()
        
    # herbe = 0
    # eau = 1
    # sol = 2
    # cailou = 3
    
    """def coord_correcte(self,c):
        if c < 0:
            return 0
        elif c >= self.dim:
            return (self.dim-1)
        else:
            return c"""
        
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
        #self.MAP[Dx,Dy][1] , self.MAP[Px,Py][1] = self.MAP[Px,Py][1] , self.MAP[Dx,Dy][1]
        self.MAP[Dx,Dy][1] , self.MAP[Px,Py][1] = self.MAP[Px,Py][1] , self.rien
        
    # besoin d'assert celle-ci?
    def add_animal(self,animal):
        x,y = animal.position[0],animal.position[1]
        self.MAP[x,y][1] = animal
        
    def suppression(self,position):
        
        # position est un tuple (x,y)
        Px = position[0]
        Py = position[1]
        
        self.MAP[Px,Py][1] = self.rien
        
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
        
    def Map_to_visible(self,MAP):
        M = []
        for l in MAP:
            L = []
            for c in l:
                L.append([c[0],c[1].rang_naturel])
            M.append(L)
        return(M)
        
    # affiche une version "visible" de la map, juste 1 affichage primaire
    def visible_to_printable(self,MAP = []):
        print('')
        if MAP == []:
            MAP = self.MAP
        M = self.Map_to_visible(MAP)
        t = '*  '
        for i in range(len(M)):
            t += str(i%10) + ' '
        print(t)
        print('')
        c = 0
        for l in M:
            txt = str(c%10)+'  '
            for case in l:
                if case[1] != 0:
                    txt += str(case[1]) + ' '
                else:
                    #pourrait etre ecrit bien + facilement avec une liste
                    
                    L = ['#','@','-','+']
                    
                    txt += L[case[0]] + ' '
                    
            print(txt)
            c +=1


if __name__ == "__main__":
    
    # pour tester les differentes fonctions de la classe, on a besoin
    # d'une classe animal et d'une classe Rien, et d'une carte que l'on appelle mappy
    class Animal_vide:
        def __init__(self):
            self.rang_naturel = 1
            
    class Rien:
        def __init__(self):
            self.rang_naturel = 0
            
    animal = Animal_vide()
    
                    
    
    mappy = np.array([
        [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()]],
        [[1,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()]],
        [[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()]], # animal en (3,3)
        [[0,Rien()],[1,Rien()],[1,Rien()],[0,animal],[0,Rien()],[1,Rien()]],
        [[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]],
        [[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()]]
    ])
    
    m = Map(mappy,Rien())
    
    V = m.voisinnage((3,3),2)
    
    assert V.tolist() == m.MAP[1:6,1:6].tolist() , \
    "Erreur : voisinnage"
    print("Ok : voisinnage")
    
    m.deplacer((6,6),(5,5))
    
    assert (isinstance(m.MAP[6,6][1],Rien) and isinstance(m.MAP[5,5][1],Animal_vide)), \
    "Erreur : deplacer"
    print("Ok : deplacer")
    
    m.suppression((2,2))
    
    assert (isinstance(m.MAP[2,2][1],Rien)), \
    "Erreur : suppression"
    print("Ok : suppression")
    
    assert (m.distance((0,0),(1,1)) == sqrt(2)), \
    "Erreur : distance"
    print("Ok : distance")
    
    
    
    
    
    
    
    
    
    
    
    