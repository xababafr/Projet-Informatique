# -*- coding: utf-8 -*-

#import numpy as np

import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
import numpy as np
from CustomList import *
from abc import ABCMeta , abstractmethod
#from Map import Map

# on mettra ces deux imports dans le futur fichier "final"

class Animal():
    """
        Classe decrivant un animal dont le comportement
        est defini dans plusieurs autres classes comportement
    """
       
    def __init__(self,ecosysteme,faim,soif,vision,vitesse,vie,position,rang,etat):
        """
            La position est un tuple (x,y) ( = position dans la matrice)
            Le rang est la position de l'animal dans la liste d'animaux
            Le comportement est une instance d'une des classes de comportement
        """
        
        # J'ai retire le parametre self.proie. En fait, il faudra bien faire un comportement different
        # pour herbivore et carnivore. Effectivement, le lapin recherche sa "proie" dans la premiere case
        # d'une position de la self.ecosysteme.MAP (herbe), tandis que le carnivore la recherche dans la seconde case.
        # un algo différent sera donc a implementer
        
        #self.ecosysteme.MAP = self.ecosysteme.MAP
        #self.LIVING = LIVING
        self.ecosysteme = ecosysteme
        self._faim = faim
        self._soif = soif
        self.vision = vision
        self.vitesse = vitesse
        self.vie = vie
        self._position = position
        self.rang = rang
        self.rang_naturel = rang+1
        self._etat = etat
        
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
        return self._faim

    @faim.setter
    def faim(self,f):
        self._faim = f
        if self._faim > 24:
            self._faim = 24
        if self._faim < 0:
            self._faim = 0

    @property
    def soif(self):
        return self._soif

    @soif.setter
    def soif(self,s):
        self._soif = s
        if self._soif > 24:
            self._soif = 24
        if self._soif < 0:
            self._soif = 0
            
    
    # modifie une position si celle-ci sort de la map
    def position_correcte(self,p):
        x,y = p[0],p[1]
        if x < 0:
            x = 0
        if x >= self.ecosysteme.MAP.dim:
            x = self.ecosysteme.MAP.dim-1
        if y < 0:
            y = 0
        if y >= self.ecosysteme.MAP.dim:
            y = self.ecosysteme.MAP.dim-1
        return (x,y)
        

    # De même, on vérifie que la position ne dépasse jamais les limites de la map
    # Deux solutions : les bords de la map sont des murs, ou
    # la map est un globe, et une extrémite mène a une autre.
    # Pour le moment, on choisi l'option des murs

    @property
    def position(self):
        return self._position

    ## On suppose l'exisence d'un attribut dim dans self.ecosysteme.MAP, qui est la dimension de l'array numpy
    @position.setter
    def position(self,p):
        self._position = self.position_correcte((p[0],p[1]))

    # Enfin, je met l'état actuel en lecture seule, on a pas trop envie que ce paramètre soit bidouillé
    @property 
    def etat(self):
        # Suppose la surcharge de __str__ dans chaque état
        return(self._etat)

    def __str__(self):
        texte = 'faim : {} \nsoif : {} \nvision : {} \nvitesse : {} \nvie : {} \nposition : {}\nrang : {}\netat : {} \n'.format(self.faim,self.soif,self.vision,self.vitesse,self.vie,self.position,self.rang,self.etat)
        
        return(texte)
        
    def changer_etat(self,etat):
        self._etat = etat
        
    def un_tour(self):
        self.vie -= 1
        self.faim -= 1
        self.soif -= 1
        # Si on doit mourir
        if (self.faim == 0 or self.soif == 0 or self.vie == 0):
            print("mort")
            self.mourir()
        else:
            (self.etat).action(self)
            
    def mourir(self):
        # supprime l'animal de living et map
        # les animaux faisant appel à un_tour() etant tous dans living, l'animal n'est
        # plus utilisé, et le ramsse-miette devrait le supprimer, vu que toutes ses references ont disparues
        # meme si ce n'est pas le cas, tant que l'animal est supprimé es deux, tout est ok
        
        """
            self.ecosysteme.MAP est l'objet global représentant la carte des animaux
            LIVING est la liste des animaux vivants
            CORPSES est la liste des cadavres
        """
        self.ecosysteme.MAP.conversion_mort(self.position) # Créer une méthode suppression dans self.ecosysteme.MAP
        # Comme on supprime un élèment de LIVING, le rang de tous ceux derriere celui de l'animal supprimé diminue de 1,à              condition de ne pas être le dernier animal de la liste, sinon, aucun rang ne change!
        if (self.rang != len(self.ecosysteme.LIVING)-1):
            for a in self.ecosysteme.LIVING[self.rang+1:]:
                a.rang -= 1
        del self.ecosysteme.LIVING[self.rang]
        self.ecosysteme.CORPSES.append(self)
        
    def decomposition(self):
        """
            Méthode permettant de supprimer un cadavre de la liste CORPSES et de la carte 
            Cet élément est définitivement éliminé
        """
         self.ecosysteme.MAP.suppression(self.position)
         # Comme on supprime un élèment de LIVING, le rang de tous ceux derriere celui de l'animal supprimé diminue de 1,à condition de ne pas être le dernier animal de la liste, sinon, aucun rang ne change!
        if (self.rang != len(self.ecosysteme.CORPSES)-1):
            for a in self.ecosysteme.CORPSES[self.rang+1:]:
                a.rang -= 1
        del self.ecosysteme.CORPSES[self.rang]
        
        
    def manger(self,quantite):
        # Pour le manger des predateurs, il faudra surcharger la méthode
        # car on a dit que lorsque qu'un prédateur mange, il remplit sa barre d'appétit
        self.faim += quantite
        
    def boire(self,quantite):
        self.soif += quantite
        
    def deplacer(self,position2):
        # La position est un tuple(x2,y2)
        self.ecosysteme.MAP.deplacer(self.position,position2) # Créer une méthode deplacer dans self.ecosysteme.MAP
        self.position = position2
        
        
    def get_voisinnage(self):
        return(self.ecosysteme.MAP.voisinnage(self.position,self.vision))
        
    def detecter_herbe(self):
        """
            Fonction qui renvoie False s'il n'y a pas d'herbe dans le voisinage, et 
            qui renvoie la position (x,y) de la case d'eau la + proche si elle existe
            elle renvoi la version locale(dans la voisinnage) de cette position
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        x,y,v = self.position[0], self.position[1],self.vision
        V = self.get_voisinnage()
        self.ecosysteme.MAP.visible_to_printable(V)
        taille = len(V)
        # L'eau la plus proche de l'animal trouvée actuellement
        herbe_trouvee = False
        distance = self.ecosysteme.MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                # Si c'est de l'herbe (on manipule un array numpy)
                if V[i,j][0] == 0:
                    # Si celle-ci est plus proche de l'animal que l'ancienne eau
                    distance_locale = self.ecosysteme.MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        herbe_trouvee = (i,j)
                        distance = distance_locale
        return herbe_trouvee
        
    def detecter_eau(self):
        """
            Fonction qui renvoie False s'il n'y a pas d'eau dans le voisinage, et 
            qui renvoie la position (x,y) de la case d'eau la + proche si elle existe
            elle renvoi la version locale(dans la voisinnage) de cette position
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        x,y,v = self.position[0], self.position[1],self.vision
        V = self.get_voisinnage()
        self.ecosysteme.MAP.visible_to_printable(V)
        taille = len(V)
        # L'eau la plus proche de l'animal trouvée actuellement
        eau_trouvee = False
        distance = self.ecosysteme.MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                # Si c'est de l'eau (on manipule un array numpy)
                if V[i,j][0] == 1:
                    # Si celle-ci est plus proche de l'animal que l'ancienne eau
                    distance_locale = self.ecosysteme.MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        #eau_trouvee = (i,j) ## TESSTTTTT
                        eau_trouvee = (i,j)
                        distance = distance_locale
        return eau_trouvee


    def detecter_herbivore(self):
        """
            Fonction qui renvoie False s'il n'y a pas d'herbivore dans le voisinage, et 
            qui renvoie la position (x,y) de la case de l'herbivore le + proche si elle existe
            elle renvoi la version locale(dans la voisinnage) de cette position
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        x,y,v = self.position[0], self.position[1],self.vision
        V = self.get_voisinnage()
        self.ecosysteme.MAP.visible_to_printable(V)
        taille = len(V)
        # L'herbivore le plus proche de l'animal trouvé actuellement
        herbivore_trouvee = False
        distance = self.ecosysteme.MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                # Si c'est de l'herbe (on manipule un array numpy)
                if (V[i,j][1].is_herbivore()):
                    # Si celle-ci est plus proche de l'animal que l'ancienne eau
                    distance_locale = self.ecosysteme.MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        herbivore_trouvee = (i,j)
                        distance = distance_locale
        return herbivore_trouvee


    def detecter_predateur(self):
        """
            Fonction qui renvoie False s'il n'y a pas de prédateur dans le voisinnage, et 
            qui renvoi la position locale (i,j) de la case du prédateur le + proche si il est visible
        """
        # V est un tableau n x n, ou n est la vision de l'animal 
        V = self.get_voisinnage()
        x,y,v = self.position[0],self.position[1],self.vision
        taille = len(V)
        # Prédateur le plus proche de l'animal trouvé actuellement
        predateur_trouve = False
        distance = self.ecosysteme.MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
                ## Ici, je suppose que dans la deuxième case de chaque position, il y a un objet possédant une
                ## méthode is_predateur renvoyant un booleen : à moi de définir ça pour chaque animal, et
                ## aussi de définir une classe Rien qui aura cette méthode, pour que l'on puisse mettre une
                ## instance de cette classe dans les cases où il n'y a pas d'animaux
                # Si c'est un prédateur
                if ((V[i,j][1]).is_predateur()):
                    # Si cette distance est plus petite que l'ancienne
                    distance_locale = self.ecosysteme.MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        predateur_trouve = (i,j)
                        distance = distance_locale
        return predateur_trouve
  
     
    def detecter_mort(self):
    """
        Fonction qui renvoie False s'il n'y a pas de cadavre dans le voisinage, et 
        qui renvoie la position (x,y) de la case du cadavre le + proche si elle existe
        elle renvoi la version locale(dans la voisinnage) de cette position
    """
    # V est un tableau n x n, ou n est la vision de l'animal 
    x,y,v = self.position[0], self.position[1],self.vision
    V = self.get_voisinnage()
    self.ecosysteme.MAP.visible_to_printable(V)
    taille = len(V)
    # Le cadavre le plus proche de l'animal trouvé actuellement
    mort_trouve = False
    distance = self.ecosysteme.MAP.distance_max()
    for i in range(taille):
        for j in range(taille):
            # on manipule un array numpy
            if (V[i,j][1].is_mort()):
                # Si le mort est plus proche de l'animal que l'ancien mort
                distance_locale = self.ecosysteme.MAP.distance(self.position,(i,j))
                if (distance_locale < distance):
                    mort_trouve = (i,j)
                    distance = distance_locale
    return mort_trouve
        
        
    """def distance_min_coins(self,position,vision):
        # on nous passe une position (x+i,y+j)
        # on veux retourner v2 et v3 tels que la position absolue
        # de la case soit donnée, càd on revoit (x+i-v2,y+j-v3) où
        # v2 = min(vision, distance_coin_x)
        # v3 = min(vision, distance_coin_y)
        
        xr,yr = position[0],position[1]
        
        distance_min_x = min(xr,(self.ecosysteme.MAP.dim-1-xr))
        distance_min_y = min(yr,(self.ecosysteme.MAP.dim-1-yr))
        
        v2,v3 = min(distance_min_x,vision), min(distance_min_y,vision)
        
        return(v2,v3)
    """
        

    def deplacements_possibles(self):
        """
            Check toutes les cases autour de l'animal, et renvoi la position de celles qui ne sont pas de la roche (3), 
            donc celles sur lesquelles il peut se déplacer
            Pour une première approximation, on dira que l'on peux marcher sur l'eau (juste des petites mares)
            cette fois-ci, on renvoi la position absolue
        """
        
        # V est un tableau n x n, où n est la vision de l'animal
        V=self.ecosysteme.MAP.voisinnage(self.position,self.vision)
        x,y,v = self.position[0],self.position[1],self.vision
        # Les déplacements possibles seront inscrits dans une liste déplacement_possibles
        deplacement_possible = []
        taille = len(V)
        position_roche = []
        # On check toutes les cases de V
        for i in range (taille):
            for j in range (taille):
                if V[i,j][0] == 3:
                    position_roche.append((x+i-v,y+j-v)) #inutile (et faux)
                else :
                    #v2,v3 = self.distance_min_coins((x+i,y+j),v)
                    deplacement_possible.append((x+i-v,y+j-v))
        return deplacement_possible
        
    def rester_ensemble_Herbivore(self,vision):
        """
            Fonction pour que les herbivores et les meutes se regroupent lorsqu'ils se croisent
        """
        # v est un tableau n x n, ou n est la vision de l'animal 
        x,y,v = self.position[0], self.position[1], self.vision
        voisinage = self.ecosysteme.MAP.voisinnage(self.position,self.vision)
        taille = len(voisinage)
        # taille contient un tableau numpy de la vision de l'animal
        deplacement_possible = []
        deplacement_possible_ideal = []
        position_ideale = ()
        distance_ideal = 2 # on laisse une case libre de distance entre l'animal et le copain : type pièce tour aux échecs
        # On cherche le copain
        position_copain = []
        copain = False
        for i in range(taille):
            for j in range(taille):
        # Si c'est un Herbivore (on manipule un array numpy)
                if voisinage[i,j][1] == Herbivore:
                    position_copain = position_copain.append(i,j)
        # L'animal suit le 1er animal rencontré, je n'ai pas eu d'autre idée
                    distance_animal_copain = self.MAP.distance(self.position,position_copain[0])
        # deplacement_possible contient la liste de toutes les positions situés dans le champ de vision de l'animal
                    for i in range(self.vision):
                        for j in range(self.vision):
                            deplacement_possible.append(i,j)
        # deplacement_possible_ideal contient la liste de toutes les positions situés à une distance de 2 du copain                    
                    for k in range(len(deplacement_possible)):
                        if self.MAP.distance(deplacement_possible[k],position_copain[0]) == 2:
                            deplacement_possible_ideal.append(deplacement_possible[k])
        # position_ideale contien la position la plus proche situé à une distance de 2 du copain
                    for l in range(len(deplacement_possible_ideale)):
                        position_ideale = min(self.MAP.distance(self.position, deplacement_possible_ideal[l]))
        # on retourne LA position_ideale; si il n'y a pas de copain, on renvoit False
                    return(position_ideale)
                else:
                    return False
    
## En construction    
## Création d'un compteur de bebe dans les caractéristiques des animaux
## Les animaux se reproduise aléatoirement lorsqu'il se rencontrent et qu'ils ne sont pas stressés : 0.4 H ** 0.9 C et S
    def reproduction_Herbivore(self,vision,vitesse,position):
        """
            Fonction permettant à nos animaux de se reproduire entre eux
        """
        # v est un tableau n x n, ou n est la vision de l'animal
        x,y,v = self.position[0], self.position[1], self.vision
        voisinage = self.ecosysteme.MAP.voisinnage(self.position,self.vision)
        taille = len(voisinnage)
        # taille contient un tableau numpy de la vision de l'animal
        position_partenaire = []
        partenaire = False
## Création d'un compteur de bebe dans les caractéristiques des animaux
        bebe = self.bebe
        # Aucun animal n'a un champ de vision superieur à 10
        distance = self.ecosysteme.MAP.distance_max()
        for i in range(taille):
            for j in range(taille):
        # Si c'est un Herbivore (on manipule un array numpy)
                if voisinage[i,j][1] == Herbivore:
                    position_partenaire = position_partenaire.append(i,j)
        # Pour se reproduire, les deux animaux n'ont pas besoin d'être l'un à coté de l'autre. 
                for k in range(position_partenaire):
                    if self.MAP.distance(self.position, position_partenaire[k]) < distance:
                        distance = self.MAP.distance(self.position, position_partenaire[k])
                        partenaire = self.position
        # Décrémenter les compteurs de bébé
        # Faire pop le nouvel animal à un emplacement vide 
                        
                    

class Herbivore(Animal):

    # on dit que une itération représente 1H, et donc 1J = 24 tours
    # l'etat est une instance de Normal_herbivore, dont on passe en argument l'animal ayant le comportement concerne (le constructeur de chaque etat prends en parametre l'objet animal concerne par le comportement)
    # le comportement a ainsi acces a toutes les methodes et attributs de l'animal, ce qui lui permet de prendre des decisions

    def __init__(self,ecosysteme,position,rang,etat):
        super().__init__(ecosysteme,24,24,1,1,120,position,rang,etat)  #faim,soif,vision,vitesse,vie
        
    # à surcharger
    def is_herbivore(self):
        return True
    
    def is_predateur(self):
        return False
        
    def is_charognard(self):
        return False
        
    def is_rien(self):
        return False
    
    def is_mort(self):
        return False
        
    def manger(self):
        self.faim += 24

    # Leur limite de soif étant haute, on peut considérer qu'ils récupèrent totalement après avoir bu.
    #Idem pour la faim

    def boire(self):
        self.faim += 24
    
    # Pour faim et soif, je met une limite assez haute, car on ne veux pas qu'ils bougent trop
    # Les herbivores étant en général assez statiques
    # L'idée est qu'ils restent en groupe pour manger
    # Un prédateur débarquent, ils fuient tous, donc leur faim et soif commence à passer en dessous de 24
    # et donc quand ils ont fini de fuir et survivre, ils vont vite trouver un nouveau spot
    def a_faim(self):
        return (self.faim < 18)
        
    def a_soif(self):
        return (self.soif < 20)
    
    # Avoir peur c'est comme détecter un prédateur    
    # def a_peur(self): 
        
       
class Solitaire(Animal):
    # Le prédateur solitaire se déplace vite et à une grande vision, mais a une durée de vie plus faible que les herbivores
    def __init__(self,ecosysteme,position,rang,etat):
        super().__init__(ecosysteme,24,24,3,3,72,position,rang,etat)
        
    # est un prédateur
    def is_herbivore(self):
        return False
        
    def is_predateur(self):
        return True
    
    def is_charognard(self):
        return False
    
    def is_rien(self):
        return False
    
    def is_mort(self):
        return False
    
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

class Charognard(Animal):
    # Le charognard se déplace vite et à une grande vision, mais a une durée de vie plus faible que les herbivores
    def __init__(self,ecosysteme,position,rang,etat):
        super().__init__(ecosysteme,24,24,3,3,72,position,rang,etat)
        
    # est un charogard
    def is_herbivore(self):
        return False
        
    def is_predateur(self):
        return False
        
    def is_charognard(self):
        return True
    
    def is_rien(self):
        return False
        
    def is_mort(self):
        return False
    
    # Quand un prédateur se nourrit, on estime qu'il a assez mangé pour toute la journée : la faim repasse a 24
    # Comme on a défini un setter sur la faim, on peut simplement le nourrir de 24

    def manger(self):
        self.faim += 24

    # Pour augmenter leur mobilité, on va aussi dire qu'ils n'ont besoin de boire que deux fois dans la journée

    def boire(self):
        self.faim += 12

    # Essayons la faim à 8 : le charognard a normalement suffisamment de ressources pour trouver une proie
    def a_faim(self):
        return (self.faim < 8)
        
    # Boire redonne 12, donc en comptant le temps de déplacement vers de l'eau, 
    # commencer à en chercher à partir de 15 semble raisonnable
    def a_soif(self):
        return (self.soif < 15)

class Rien():
    
    def __init__(self):
        self.rang_naturel = 0
    
    def is_herbivore(self):
        return False
    
    def is_predateur(self):
        return False
        
    def is_charognard(self):
        return False
   
    def is_rien(self):
       return True
       
    def is_mort(self):
        return False
        
## Idee gestion des mort
## Les morts sont des class aux même titre que les herbivores, les solitaires... Il faut alors retoucher la fonction initiale de Etat afin que seul les charognards puisse se déplacer sur les cases de cadavres (Si les cadavres se mettent à créer des labyrinthe infernaux, réduire leur durée de présence sur la carte)
## Les morts sont des caractéristiques de la carte comme l'herbe ou l'eau sur lesquelles seul les charognards peuvent se déplacer. Il faut donc encore retoucher la class Etat afin que les autres type d'animaux ne puissent se déplacer sur ces cases (idem caillou)
## Créer une méthode detecter_mort dans Animal
class Mort():
    def __init__(self,ecosysteme,position,rang,etat):
        super().__init__(ecosysteme,24,24,0,0,10,position,rang,etat) # Pour l'instant les cadavres ont une vie de 10
    
    def is_herbivore(self):
        return False
    
    def is_predateur(self):
        return False
        
    def is_charognard(self):
        return False
        
    def is_rien(self):
         return False
         
    def is_mort(self):
        return True
    
    
# class Meute(Animal):
#     # Le prédateur en Meute se deplace vite et à une vision moyenne, mais a une durée de vie plus faible que les herbivores
#     # Il ne faut pas leur donner une vue trop forte, sinon, il vont raser des troupeaux d'herbivores tout le temps
#     def __init__(self,ecosysteme,position,rang,etat):
#         super().__init__(ecosysteme,24,24,2,2,90,position,rang,etat)
#         
#     # est un prédateur
#     def is_herbivore(self):
#         return False
#         
#     def is_predateur(self):
#         return True
#         
#     def is_charognard(self):
#         return False
#     
#     # Quand un prédateur se nourrit, on estime qu'il a assez mangé pour toute la journée : la faim repasse a 24
#     # comme on a défini un setter sur la faim, on peut simplement le nourrir de 24
# 
#     def manger(self):
#         self.faim += 24
# 
#     # Pour augmenter leur mobilité, on va aussi dire qu'ils n'ont besoin de boire que deux fois dans la journée
# 
#     def boire(self):
#         self.soif += 12
# 
#     # Essayons la faim à 12 : la meute a besoin d'un tout petit peu plus de temps que le solitaire pour trouver une proie
#     # à cause de sa mobilité et de sa vision moins grande
#     def a_faim(self):
#         return (self.faim < 12)
#         
#     # Boire redonne 12, donc en comptant le temps de déplacement vers de l'eau, 
#     # commencer à en chercher à partir de 18 semble raisonnable
#     # Je met 18 ainsi, l'animal va "recharger" sa soif un peu avant d'avoir faim et de commencer sa traque d'animal : ainsi
#     # il peux faire sa traque entière sans descendre trop bas dans la soif
#     def a_soif(self):
#         return (self.soif < 18)
    
"""if __name__ == "__main__":
    
    # on a besoin d'une map pour tester les fonction de animal
    # on va donc creer un self.ecosysteme contenant une instance de Map()
    # on a aussi besoin d'objets etat,  ils peuvent etre vides pources tests, c'est suffisant
    
    from Map import *
    
    class EtatA():
        def __init__(self):
            pass
            
        def __str__(self):
            return("A")
            
            
    class EtatB():
        def __init__(self):
            pass
            
        def __str__(self):
            return("B")
       
            
    class Ecosysteme():
        def __init__(self,MAP,LIVING):
            self.MAP = MAP
            self.LIVING = LIVING
    
    lapin = Animal(12,15,2,1,480,(1,1),0,EtatA())
    loup = Animal(10,20,3,3,240,(3,3),1,EtatB())
    mouton = Animal(12,15,2,1,460,(5,5),2,EtatA())
    cheval = Animal(10,20,3,3,260,(2,5),3,EtatB())
    chevre = Herbivore((4,5),4,EtatA())
    lion = Solitaire((2,1),5,EtatA())
    
    mappy = np.array([
        [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()]],
        [[1,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()]], #lapin
        [[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()]], #cheval
        [[0,Rien()],[1,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[1,Rien()]], #loup
        [[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]], #chevre
        [[0,Rien()],[1,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()]] #mouton et lion
    ])
    
    
    ## pour la MAP, je n'ai pas trouvé d'autre solution que lui passer un objet Rien()
    ## pour faire ses manipulations, sinon il y a des erreurs... affaire à suivre
    rien = Rien()
    MAP = Map(mappy,rien)
    LIVING = [lapin,loup,mouton,cheval,chevre,lion]
    
    self.ecosysteme = Ecosysteme(MAP,LIVING)
    
    # on a initialisé toutes les variables / objets necessaires, on peut commencer les tests
    
    lapin.faim, lapin.soif, lapin.position = 35, -4, (-7,10)
    
    # les getter et setters ne sont pas appellés dans le constructeur de Animal, c'est vonlontaire
    # mais ça veut dire que lors de la création des animaux, on doit rentrer des infos valides
    
    assert (lapin.faim == 24 and lapin.soif == 0 and lapin.position == (0,5) and isinstance(lapin.etat,EtatA)), \
    "Erreur : getters et setters de faim, soif et position"
    print("Ok : getters et setters de faim, soif, position et etat")
    
    lapin.position = (1,1) # on le remet là où il etait
    
    loup.mourir()
    
    # on verifie que tout a bien été supprimé dans living
    # la fonction Map.suppression a déjà été vérifiée donc pas besoin de checker la carte également
    def check_mourir():
        if len(self.ecosysteme.LIVING) != 5:
            return False
        else:
            for i in range(5):
                if self.ecosysteme.LIVING[i].rang != i:
                    return False
        return True
    
    assert (check_mourir()), "Erreur : mourir"
    print("Ok : mourir")
    
    lapin.changer_etat(EtatB())
    
    assert (isinstance(lapin.etat,EtatB)), "Erreur : changer_etat"
    print("Ok : changer etat")
    
    # si mourir() esr OK, un_tour() aussi, donc on verif' pas
    # manger(), boire() sont trivialement correctes
    
    lapin.deplacer((2,2))
    
    assert(isinstance(self.ecosysteme.MAP.infos((1,1))[1],Rien) and isinstance(self.ecosysteme.MAP.infos((2,2))[1],Animal) and lapin.position == (2,2)), "Erreur : deplacer"
    print("Ok : deplacer")
    
    assert(mouton.detecter_eau() == (4,4) and mouton.detecter_herbivore() == (4,5) and lapin.detecter_predateur() == (2,1)), "Erreur : fonctions detecter_..."
    print("Ok : fonctions detecter_...")
    
    dpl = [(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(1, 1),(1, 2),(1, 3),(1, 4),(2, 0),(2, 1),(2, 2),(2, 4),(3, 0),(3, 3),(3, 4),(4, 0),(4, 2),(4, 3)]
    
    assert(lapin.deplacements_possibles() == dpl), "Erreur : deplacements possibles"
    print("Ok : deplacements possibles")"""

#lapin = Animal(1,2,3,4,5,6,7,8)
#mouton = Animal(2,1,4,3,5,7,6,8)
#carotte = Animal(3,1,5,3,3,7,3,8)
#M = [[1,2,lapin],[3,carotte,4],[mouton,5,6]]
#L = [lapin,carotte,mouton]
