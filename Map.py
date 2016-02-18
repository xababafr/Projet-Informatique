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

#Créer une méthode ""suppressioné""
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

class Map:

    def __init__(self, M):
        self.M = M
        self.dim = len(M)
        
    # je suppose pr le moment qu'un n'y a qu'un animal par case
    def deplacer(self,x,y,x2,y2):
        self.M[x2][y2][1] = self.M[x][y][1]
        self.M[x][y][1] = 0
        
    def infos(self,x,y):
        return self.M[x][y] # ou alors pk pas surcharger __getitem__()
        
    # sol = 0
    # herbe = 1
    # eau = 2
    def afficher(self):
        fenetre = Tk()
        for x in range(self.dim):
            for y in range(self.dim):
                P = self.infos(x,y)
                # s'il n'y a pas d'animal , on affiche ce qu'il y a par terre
                if P[0] == 0:
                    case = Canvas(fenetre,width=10,height=10,background='brown')
                elif P[0] == 1:
                    case = Canvas(fenetre,width=10,height=10,background='green')
                else:
                    case = Canvas(fenetre,width=10,height=10,background='blue')
                if type(P[1]) == Herbivore:
                    case.create_line(0,0,10,10)
                elif type(P[1]) == Meute: #predateur en meute
                    case.create_rectangle(2,2,8,8)
                else: #preateur solitaire
                    case.create_text(0,0,text='S')
                case.pack(padx=10*x,pady=10*y)
        fenetre.mainloop()
        
    
        
class Animal:
    def __init__(self,n):
        self.n = n
