import numpy as np
from abc import ABCMeta , abstractmethod

# on mettra ces deux imports dans le futur fichier "final"

class Animal():
    """
        Classe décrivant un animal dont le comportement
        est defini dans plusieurs autres classes comportement
    """
       
    def __init__(self,faim,soif,vision,vitesse,vie,position,rang,etat):
        """
            La position est un tuple (x,y) ( = position dans la matrice)
            Le rang est la position de l'animal dans la liste d'animaux
            Le comportement est une instance d'une des classes de comportement
            
        """
        
        # J'ai retiré le paramètre self.proie. En fait, il faudra bien faire un comportement diffèrent
        # pour herbivore et carnivore. Effectivement, le lapin recherche sa "proie" dans la premiere case
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
        
    # à surcharger
    @abstractmethod
    def is_herbivore(self):
        pass
        
    # à surcharger
    @abstractmethod
    def is_predateur(self):
        pass
     
    # à surcharger
    @abstractmethod
    def a_faim(self):
        pass
    
    # à surcharger 
    @abstractmethod   
    def a_soif(self):
        pass

    # Création de décorateur pour la faim et la soif, qui ne peuvent exeder 24 ni être en dessous de 0
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

    # De même, on vérifie que la position ne dépasse jamais les limites de la map
    # Deux solutions : les bords de la map sont des murs, ou
    # la map est un globe, et une extrémite mène a une autre.
    # Pour le moment, on choisi l'option des murs

    @property
    def position(self):
        return self.position

    ## On suppose l'exisence d'un attribut dim dans MAP, qui est la dimension de l'array numpy
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

    # Enfin, je met l'état actuel en lecture seule, on a pas trop envie que ce paramètre soit bidouillé
    @property 
    def etat(self):
        # Suppose la surcharge de __str__ dans chaque état
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
        
        # Si on doit mourir
        if (self.faim == 0 or self.soif == 0 or self.vie == 0):
            self.mourir()
        else:
            (self.etat).action()
            
    def mourir(self):
        """
            MAP est l'objet global représentant la carte des animaux
            LIVING est la liste des animaux vivants
        """
        MAP.suppression(self.position) # Créer une méthode suppression dans MAP
        # Comme on supprime un élèment de LIVING, le rang de tous ceux derriere celui de l'animal supprimé diminue de 1
        for a in LIVING[self.rang+1:]:
            a.rang -= 1
        del LIVING[self.rang]
        
    def manger(self,quantite):
        # Pour le manger des predateurs, il faudra surcharger la méthode
        # car on a dit que lorsque qu'un prédateur mange, il remplit sa barre d'appétit
        self.appetit += quantite
        
    def boire(self,quantite):
        self.soif += quantite
        
    def deplacer(self,position2):
        # La position est un tuple(x2,y2)
        MAP.deplacer(self.position,position2) # Créer une méthode deplacer dans MAP
        self.position = position2
        
    def detecter_eau(self):
        """
            Fonction qui renvoie False s'il n'y a pas d'eau dans le voisinage, et 
            qui renvoie la position (x,y) de la case d'eau la + proche si elle                    existe
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinage(self.position,self.vision)
        taille = len(V)
        # L'eau la plus proche de l'animal trouvée actuellement
        eau_trouvee = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                # Si c'est de l'eau (on manipule un array numpy)
                if V[i,j][0] == 1:
                    # Si celle-ci est plus proche de l'animal que l'ancienne eau
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        eau_trouvee = (i,j)
                        distance = distance_locale
        return eau_trouvee


    def detecter_herbivore(self):
        """
            Fonction qui renvoie False s'il n'y a pas d'autres herbivores dans le voisinage, et 
            qui renvoi la position (x,y) de la case de l'herbivore le + proche si il est visible
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinage(self.position,self.vision)
        taille = len(V)
        # L'herbivore le plus proche de l'animal trouvé actuellement
        herbivore_trouve = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                ## De même, je suppose l'existence d'une méthode is_herbivore
                # Si c'est un prédateur
                if (V[i,j][1]).is_herbivore():
                    # Si celui-ci est plus proche de l'animal que l'ancien herbivore
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        herbivore_trouve = (i,j)
                        distance = distance_locale
        return herbivore_trouve


    def detecter_predateur(self):
        """
            Fonction qui renvoie False s'il n'y a pas de prédateur dans le voisinnage, et 
            qui renvoi la position (x,y) de la case du prédateur le + proche si il est visible
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = MAP.voisinage(self.position,self.vision)
        taille = len(V)
        # Prédateur le plus proche de l'animal trouvé actuellement
        predateur_trouve = False
        distance = MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                ## Ici, je suppose que dans la deuxième case de chaque position, il y a un objet possédant une
                ## méthode is_predateur renvoyant un booleen : à moi de définir ça pour chaque animal, et
                ## aussi de définir une classe Rien qui aura cette méthode, pour que l'on puisse mettre une
                ## instance de cette classe dans les cases où il n'y a pas d'animaux
                # Si c'est un prédateur
                if (not (V[i,j][1]).is_herbivore()):
                    # Si cette distance est plus petite que l'ancienne
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        predateur_trouve = (i,j)
                        distance = distance_locale
        return predateur_trouve
        

    def deplacements_possibles(self):
        """
            Check toutes les cases autour de l'animal, et renvoi la position de celles qui ne sont pas de l'eau, 
            donc celles sur lesquelles il peut se déplacer
            Pour une première approximation, on dira que l'on peux même marcher sur l'eau (juste des petites mares)
        """
        # V est un tableau n x n, où n est la vision de l'animal
        V=MAP.voisinage(self.position,self.vision)
        # Les déplacements possibles seront inscrits dans une liste déplacement_possibles
        deplacement_possible = []
        taille = len(V)
        position_eau = []
        # On check toutes les cases de V
        for i in range (taille):
            for j in range (taille):
                if V[0] == 1:
                    position_eau = position_eau.append[i,j]
                else :
                    deplacement_possible = deplacement_possible.append[i,j]
        return deplacement_possible
            


class Herbivore(Animal):
    
<<<<<<< HEAD
    # on dit que une itération représente 1H, et donc 1J = 24 tours
    # l'etat est une instance de Normal_herbivore, dont on passe en argument l'animal ayant le comportement concerne (le constructeur de chaque etat prends en parametre l'objet animal concerne par le comportement)
    # le comportement a ainsi acces a toutes les methodes et attributs de l'animal, ce qui lui permet de prendre des decisions
=======
    # On dit qu'une itération représente 1H, et donc 1J = 24 tours
    # L'état est une instance de Normal_herbivore, dont on passe en argument l'animal ayant le comportement concerné
    # Le comportement a ainsi accés a toutes les méthodes et attributs de l'animal, ce qui lui permet de prendre des decisions
>>>>>>> origin/master
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,3,1,120,position,rang,Herbivore_normal(self))
        
    # à surcharger
    def is_herbivore(self):
        return True
    
    def is_predateur(self):
        reurn False
        
    
    # Pour faim et soif, je met une limite assez haute, car on ne veux pas qu'ils bougent trop
    # Les herbivores étant en général assez statiques
    # L'idée est qu'ils restent en groupe pour manger
    # Un prédateur débarquent, ils fuient tous, donc leur faim et soif commence à passer en dessous de 24
    # et donc quand ils ont fini de fuir et survivre, ils vont vite trouver un nouveau spot
    def a_faim(self):
        return (self.faim < 18)
        
    def a_soif(self):
        return (self.soif < 18)
    
    # Avoir peur c'est comme détecter un prédateur    
    # def a_peur(self): 
        





       
class Solitaire(Animal):
    # Le prédateur solitaire se déplace vite et à une grande vision, mais a une durée de vie plus faible que les herbivores
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,6,3,72,position,rang,Solitaire_normal(self))
        
    # est un prédateur
    def is_herbivore(self):
        return False
        
    def is_predateur(self):
        return True
    
    # Quand un prédateur se nourrit, on estime qu'il a assez mangé pour toute la journée : la faim repasse a 24
    # Comme on a défini un setter sur la faim, on peut simplement le nourrir de 24

    def manger(self):
        self.faim += 24

    # Pour augmenter leur mobilité, on va aussi dire qu'ils n'ont besoin de boire que deux fois dans la journée

    def boire(self):
        self.faim += 12

    # Essayons la faim à 8 : le solitaire a normalement suffisamment de ressources pour trouver une proie
    def a_faim(self):
        return (self.faim < 8)
        
    # Boire redonne 12, donc en comptant le temps de déplacement vers de l'eau, 
    # commencer à en chercher à partir de 15 semble raisonnable
    def a_soif(self):
        return (self.soif < 15)





class Meute(Animal):
    # Le prédateur en Meute se deplace vite et à une vision moyenne, mais a une durée de vie plus faible que les herbivores
    # Il ne faut pas leur donner une vue trop forte, sinon, il vont raser des troupeaux d'herbivores tout le temps
    def __init__(self,faim,soif,position,rang,etat):
        super.__init__(24,24,4,2,96,position,rang,Meute_normal(self))
        
    # est un prédateur
    def is_herbivore(self):
        return False
        
    def is_predateur(self):
        return True
        
    
    # Quand un prédateur se nourrit, on estime qu'il a assez mangé pour toute la journée : la faim repasse a 24
    # comme on a défini un setter sur la faim, on peut simplement le nourrir de 24

    def manger(self):
        self.faim += 24

    # Pour augmenter leur mobilité, on va aussi dire qu'ils n'ont besoin de boire que deux fois dans la journée

    def boire(self):
        self.soif += 12

    # Essayons la faim à 12 : la meute a besoin d'un tout petit peu plus de temps que le solitaire pour trouver une proie
    # à cause de sa mobilité et de sa vision moins grande
    def a_faim(self):
        return (self.faim < 12)
        
    # Boire redonne 12, donc en comptant le temps de déplacement vers de l'eau, 
    # commencer à en chercher à partir de 18 semble raisonnable
    # Je met 18 ainsi, l'animal va "recharger" sa soif un peu avant d'avoir faim et de commencer sa traque d'animal : ainsi
    # il peux faire sa traque entière sans descendre trop bas dans la soif
    def a_soif(self):
        return (self.soif < 18)


class Rien():
    
    def is_herbivore(self):
        return False
    
    def is_predateur(self):
        return False
        
    
    
        

#lapin = Animal(1,2,3,4,5,6,7,8)
#mouton = Animal(2,1,4,3,5,7,6,8)
#carotte = Animal(3,1,5,3,3,7,3,8)
#M = [[1,2,lapin],[3,carotte,4],[mouton,5,6]]
#L = [lapin,carotte,mouton]
