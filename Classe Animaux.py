from random import random

class Animal(object):
    # Super-classe Animal contenant les caractéristiques communes aux différents type d'animaux
   
    def __init__(self,abscisse,ordonnee,faim,soif,vie,vitesse,vision,fertilite):
        self.__x=abscisse
        self.__y=ordonnee
        self.__faim=faim
        self.__soif=soif
        self.__vie=vie
        self.__vision=vision
        self.__fertilite=fertilite
        
    def mort(self): # Le suffixe M indique qu'un animal est mort
        vie=0
        if designation=='Herb':
            if vie > 200:   # Vie d'un Herbivore = 200
                designation=designation+'M'
            else:
                vie=vie+1
        if designation=='PredaSo':
            if vie > 125:   # Vie d'un Predateur_solo = 125
                designation=designation+'M'
            else:
                vie=vie+1
        if designation=='PredaMe':
            if vie > 100:   # Vie d'un Predateur_meute = 100
                designation=designation+'M'
            else:
                vie=vie+1
        if designation=='Charog':
            if vie > 150:   # Vie d'un Charognard = 150
                designation=designation+'M'
            else:
                vie=vie+1
        
        
    def reproduction(self,fertilite):
        
    def mouvement(self,abscisse,ordonnee,vision):
        if designation='Herb':
        if designation='PredaSo':
        if designation='PredaMe':
        if designation='Charog'
        
        
        
    
    def faim(self):
        if faim > 72 and faim < 144:
            CHERCHER A MANGER
        if faim > 144: # On compte un tic tout les 10 minutes ==> 144*10 minutes dans une journée
            designation=designation+'M'
        
    
    def soif(self):
        if soif > 72 and soif < 144:
            CHERCHER A BOIRE
        if soif > 144:
            designation=designation+'M'
        
            
        
        
        
        
        
class Herbivore(Animal,designation='Herb'): # Symbole Herb sur la matrice
    #Création de la sous classe Herbivore
    def __init__(self,abscisse,ordonnee,faim,soif,vie,vitesse,vision):
        super().__init__(abscisse,ordonnee,faim,soif,vie,vitesse,vision)
        
        
class Predateur_solo(Animal,designation='PredaSo'): # Symbole PredaSo sur la matrice
     #Création de la sous classe Predateur_solitaire
    def __init__(self,abscisse,ordonnee,faim,soif,vie,vitesse,vision):
        super().__init__(abscisse,ordonnee,faim,soif,vie,vitesse,vision)
        
class Predateur_meute(Animal,designation='PredaMe'): # Symbole PredaMe sur la matrice
     #Création de la sous classe Predateur_meute
    def __init__(self,abscisse,ordonnee,faim,soif,vie,vitesse,vision):
        super().__init__(abscisse,ordonnee,faim,soif,vie,vitesse,vision)
        
class Charognard(Animal,designation='Charog'): #Symbole Charog sur la matrice
    #Création de la sous classe Charognard
    def __init__(self,abscisse,ordonnee,faim,soif,vie,vitesse,vision):
        super().__init__(abscisse,ordonnee,faim,soif,vie,vitesse,vision)