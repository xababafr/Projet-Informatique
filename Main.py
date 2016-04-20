# -*- coding: utf-8 -*-

"""

###########################################################################################################
COMMENT SE SERVIR DE NOTRE PROGRAMME : 

le main qui suit permet au correcteur de verifier le comptement de nos herbivores
et prédateurs (note :  les herbivores n'ont pour le moment ni comportement de meute,
ni comportement de fuite, mais cela ne saurait tarder)

Pour commencer, éxécutez le fichier Main.py, le main ci-dessous créé l'écosysteme 
(avec la map, la liste LIVING et la liste chainée CORPSES), et y ajoute deux animaux,
qui sont nommés tigre et lapin (notés respectivement 1 et 2 sur la map)

Pour afficher la carte : taper dans la console ecosysteme.MAP.visible_to_printable()

vous pouvez testez les différents comportements de ces animaux en ecrivant dans la console
animal.un_tour(), et en modifiant leurs attributs faim et soif à la main
Une fois sous "stress", (faim et/ou soif), les animaux détaillent leurs faits et gestes de
chaque tour, en printant leur voisinnage et les descisions qu'ils prennent;
dans l'etat normal, ils se contentent d'ecrire le déplacement aléatoire qu'ils font.

vous pouvez aussi ajouter d'autres animaux dans la carte, les instructions d'ajout etant : 
tigre = Solitaire(ecosysteme,(4,3),ecosysteme.get_rang(),Solitaire_normal())
ecosysteme.add_animal(tigre)

vous pouvez modifier les ressources ou la taille de la MAP(0 = herbe, 1 = eau, 2 = sol, 3 = roche)

Nous avons préférer donner un main qui ne fais pas tourner les animaux en boucle, mais qui détaille
précisement comment ils se comportent. Ainsi la première étape de ce projet sera validée plus facilement :
vous pouvez beaucoup plus aisément vous convaincre du fonctionnement du programme que si celui-ci se
contentait d'afficher une MAP qui évolue selon des règles à peine précisées.

PS : si ce main-ci bug, une version fonctionnelle se trouve dans le fichier Etat.py
###########################################################################################################

"""

import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
import numpy as np
from Animal import *
from Map import *
from AStar import *
from CustomList import *
from Etat import *

mappy = [
    [[2,Rien()],[2,Rien()],[1,Rien()]],
    [[3,Rien()],[3,Rien()],[3,Rien()]],
    [[3,Rien()],[3,Rien()],[3,Rien()]]
]

mappy2 = [
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()]],
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()]],
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()]],
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[0,Rien()],[0,Rien()]],
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[0,Rien()],[0,Rien()]],
    [[2,Rien()],[2,Rien()],[2,Rien()],[2,Rien()],[1,Rien()],[2,Rien()]]
]

class Ecosysteme:
    def __init__(self,MAP,LIVING,nbtours):
        self.MAP = Map(np.array(MAP),Rien())
        self.LIVING = LIVING
        self.CORPSES = CustomList()
        
    def add_animal(self,animal):
        self.LIVING.append(animal)
        self.MAP.add_animal(animal)
    
    # retourne le rang d'un animal qui viendrait a etre ajouté à la fin de LIVING
    def get_rang(self):
        return len(self.LIVING)
        
    def unTour(self):
        for i in LIVING: 
            LIVING[i].unTour()
            
    def simuler(self):
        for t in range(self.nbtours):
            print("### Tour %i ###"%(t))
            self.unTour()
            print(self)
            time.sleep(0.5)

# test Solitaire_normal
ecosysteme = Ecosysteme(np.array(mappy2),[])
tigre = Solitaire(ecosysteme,(4,3),ecosysteme.get_rang(),Solitaire_normal())
ecosysteme.add_animal(tigre)
lapin = Herbivore(ecosysteme,(8,5),ecosysteme.get_rang(),Herbivore_normal())
ecosysteme.add_animal(lapin)