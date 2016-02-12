import numpy as np
from abc import ABCMeta , abstractmethod

# on mettra ces deux imports dans le futur fichier "final"

class Animal():
    """
        Classe decrivant un animal, dont le comportement
        est defini dans plusieurs classes comportement
    """
       
    def __init__(self,faim,soif,vision,vitesse,vie,position,rang,etat):
        """
            la position est un tuple (x,y) ( = position dans la matrice)
            le rang est la position de l'animal dans la liste d'animaux
            le comportement  un une instance d'une des classes de comportement
            
        """
        
        # j'ai retiré le parametre self.proie, en fait,  il faudra bien faire un comportement diffenrent
        # pour herbivore et carnivore.. Effectivement, le lapin recherche sa "proie" dans la premiere case
        # d'une position de la MAP (herbe), tandis que le carnivore la recherche dans la seconde case.
        # un algo différent dera donc a implementer
        
        self.faim = faim
        self.soif = soif
        self.vision = vision
        self.vitesse = vitesse
        self.vie = vie
        self.position = position
        self.rang = rang
        self.etat = etat
        
    # a surcharger
    @abstractmethod
    def is_herbivore(self):
        pass
        
    # a surcharger
    @abstractmethod
    def is_predateur(self):
        pass
     
    # a surcharger
    @abstractmethod
    def a_faim(self):
        pass
    
    # a surcharger 
    @abstractmethod   
    def a_soif(self):
        pass

    # creation de decorateur pour la faim et la soif, qui ne peuvent exeder 24 ni etre en dessous de 0
    # on fais donc le getter et le setter
    @property
    def faim(self):
        return self.faim

    @faim.setter
    def faim(self,f):
        self.faim += f
        if self.faim > 24:
            self.faim = 24
        if self.faim < 0:
            self.faim = 0

    @property
    def soif(self):
        return self.soif

    @soif.setter
    def soif(self,s):
        self.soif += s
        if self.soif > 24:
            self.soif = 24
        if self.soif < 0:
            self.soif = 0

    # de meme, on verifie que la position ne sort jamais de la map
    # deux solutions : les bords de la map sont des murs, ou
    # la map est uune un globe, et une extremite teleporte a une autre
    # pour le moment, on fais les murs

    @property
    def position(self):
        return self.position

    ## suppose l'exisence d'une attibut dim dans map, qui est la dimension de l'array numpy
    @position.setter
    def position(self,p):
        x,y = p[0],p[1]
        if x < 0:
            x = 0
        if x > MAP.dim:
            x = MAP.dim
        if y < 0:
            y = 0
        if y > MAP.dim:
            y = MAP.dim
        self.position = (x,y)

    # enfin, je met l'etat actuel en lecture seule, on a pas trop envie que ce parametre soit bidouille
    @property 
    def etat(self):
        # suppose la surcharge de __str__ dans chaque etat
        return(str(self.etat))

    def __str__(self):
        texte = 'faim : {} \nsoif : {} \nvision : {} \nvitesse : {} \nvie : {} \nposition : {}\nrang : {}\netat : {} \n'.format(self.faim,self.soif,self.vision,self.vitesse,self.vie,self.position,self.rang,self.etat)
        
        return(texte)
        
    def changer_etat(self,etat):
        self.etat = etat
        
    def un_tour(self):
        self.vie -= 1
        self.faim -= 1
        self.soif -= 1
        
        #si on doit mourir
        if (self.faim == 0 or self.soif == 0 or self.vie == 0):
            self.mourir()
        else:
            (self.etat).action()
            
    def mourir(self):
        """
            MAP est l'objet global representant la carte des animaux
            LIVING est la liste des animaux vivants
        """
        MAP.suppression(self.position)
        # comme on supprime un element de LIVING, le rang de tous ceux derriere l'animal supprime diminue de 1
        for a in LIVING[self.rang+1:]:
            a.rang -= 1
        del LIVING[self.rang]
        
    def manger(self,quantite):
        #pour le manger des predateurs, il faudra surcharger la methode
        #car on a dit qu'un predacteur, quand il bouffait, remplissait sa barre d'appettit
        self.appetit += quantite
        
    def boire(self,quantite):
        self.soif += quantite
        
    def deplacer(self,position2):
        #position est un tuple(x2,y2)
        MAP.deplacer(self.position,position2)
        self.position = position2
        
    def detecter_eau(self):
        """
            fonction qui renvoi False s'il n'y a pas d'eau dans le voisinnage, et 
            qui renvoi la position (x,y) de la case d'eau la + proche si elle existe
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinnage(self.position,self.vision)
        taille = len(V)
        # l'eau la plus proche de l'animal trouvee actuellement
        eau_trouvee = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                # si c'est de l'eau (on manipule un array numpy)
                if V[i,j][0] == 1:
                    # si celle-ci est plus proche de l'animal que l'ancienne
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        eau_trouvee = (i,j)
                        distance = distance_locale
        return eau_trouvee


    def detecter_herbivore(self):
        """
            fonction qui renvoi False s'il n'y a pas d'autres herbivoores dans le voisinnage, et 
            qui renvoi la position (x,y) de la case de l'herbivore le + proche si il est visible
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinnage(self.position,self.vision)
        taille = len(V)
        # l'eau la plus proche de l'animal trouvee actuellement
        herbivore_trouve = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                ## de meme, je suppose l'existence d'une methode is_herbivore
                # si c'est un predateur
                if (V[i,j][1]).is_herbivore():
                    # si celle-ci est plus proche de l'animal que l'ancienne
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        herbivore_trouve = (i,j)
                        distance = distance_locale
        return herbivore_trouve


    def detecter_predateur(self):
        """
            fonction qui renvoi False s'il n'y a pas de predateur dans le voisinnage, et 
            qui renvoi la position (x,y) de la case du predateur le + proche si il est visible
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinnage(self.position,self.vision)
        taille = len(V)
        # l'eau la plus proche de l'animal trouvee actuellement
        predateur_trouve = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                ## ici, je suppose que dans la deuxieme case de chaque positon, il y a un object possedant une
                ## methode is_predateur revoyant un booleen : a moi de definir ça pour chaque animal, et
                ## de aussi definir une classe Rien qui aura cette méthode, pour que l'on puisse mettre une
                ## instance de cette classe dans les cases où il n'y a pas d'animaux
                # si c'est un predateur
                if (not (V[i,j][1]).is_herbivore()):
                    # si celle-ci est plus proche de l'animal que l'ancienne
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        predateur_trouve = (i,j)
                        distance = distance_locale
        return predateur_trouve
        

    def deplacements_possibles(self):
        """
            checke toutes les cases autour de l'animal, et renvoi la position de celles qui ne sont pas de l'eau, 
            donc celles sur lesquelles il peux se deplacer
            Pour une premiere approximation, on dira que l'on peux meme marcher sur l'eau( juste des petites mares)
        """

        # a ecrire

        pass





class Herbivore(Animal):
    
    # on dit que une intération représente 1H, et donc 1J = 24 tours
    # l'etat es une instance de Normal_herbivore, dont on passe en argument l'animal ayant le comportement concerne
    # le comportement a ainsi acces a toutes les methodes et attribut de l'animal, ce qui lui permet de prendre des descisions
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,3,1,120,position,rang,Herbivore_normal(self))
        
    # a surcharger
    def is_herbivore(self):
        return True
        
    
    # pour faim et soif, je met une limite assez haute, car on veux pas qu'ils bougent trop
    # les herbivores etant en general assez statiques
    # l'idee est qu'ils restent en groupe pour manger
    # un predateur debarquent, ils fuient tous, donc leur faim et soif commence à passer en dessous de 24
    # et donc quand ils ont fini de fuir et survivre, ils vont vite trouver un nouveau spot
    def a_faim(self):
        return (self.faim < 18)
        
    def a_soif(self):
        return (self.soif < 18)
    
    # avoir peur c'est comme detecter un predateur    
    #def a_peur(self): 
        





       
class Solitaire(Animal):
    # le predateur solitaire se deplace vite et a une grande vision, mais a une durée de vie plus faible que les herbivores
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,6,3,72,position,rang,Solitaire_normal(self))
        
    # est une predateur
    def is_herbivore(self):
        return False
        
    
    # quand un predateur se nourrit, on estime qu'il a assez mange pour toute la journee : la faim repasse a 24
    # comme on a defini un setter sur la faim, on peut simplement le nourrir de 24

    def manger(self):
        self.faim += 24

    # pour augmenter leur mobilite, on va aussi dire qu'il n'ont besoin de boire que deux fois dans la journee

    def boire(self):
        self.faim += 12

    # essayons la faim a 8 : le solitaire a normalement suffisamment de ressources pour trouver une proie
    def a_faim(self):
        return (self.faim < 8)
        
    # boire redonne 12, donc en comptant le temps de deplacement a de l'eau, 
    # commencer a en chercher a partir de 15 semble raisonnable
    def a_soif(self):
        return (self.soif < 15)





class Meute(Animal):
    # le predateur en leute se deplace vite et a une vision moyenne, mais a une durée de vie plus faible que les herbivores
    # il ne faut pas leur donner une vue trop forte, sinon, il vont raser des troupeaux d'herbivores tout le temps
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,4,2,96,position,rang,Meute_normal(self))
        
    # est une predateur
    def is_herbivore(self):
        return False
        
    
    # quand un predateur se nourrit, on estime qu'il a assez mange pour toute la journee : la faim repasse a 24
    # comme on a defini un setter sur la faim, on peut simplement le nourrir de 24

    def manger(self):
        self.faim += 24

    # pour augmenter leur mobilite, on va aussi dire qu'il n'ont besoin de boire que deux fois dans la journee

    def boire(self):
        self.soif += 12

    # essayons la faim a 12 : la meute a besoin d'un tout petit peu plus de temps que le solitaire pour trouver une proie
    # a cause de sa mobilité et sa vision moins grande
    def a_faim(self):
        return (self.faim < 12)
        
    # boire redonne 12, donc en comptant le temps de deplacement a de l'eau, 
    # commencer a en chercher a partir de 18 semble raisonnable
    # je met 18 ainsi, l'animal va "recharger" sa soif un peu avant d'avoir faim et de commencer sa traque d'animal : ainsi
    # il peux faire sa traque entiere sans descendre trop bas dans la soif
    def a_soif(self):
        return (self.soif < 18)

        

#lapin = Animal(1,2,3,4,5,6,7,8)
#mouton = Animal(2,1,4,3,5,7,6,8)
#carotte = Animal(3,1,5,3,3,7,3,8)
#M = [[1,2,lapin],[3,carotte,4],[mouton,5,6]]
#L = [lapin,carotte,mouton]
