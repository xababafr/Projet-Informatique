class Animal():
    """
        Classe decrivant un animal, dont le comportement
        est defini dans plusieurs classes comportement
    """
       
    def __init__(self,faim,soif,vision,vitesse,vie,proie,position,rang,etat):
        """
            la position est un tuple (x,y) ( = position dans la matrice)
            le rang est la position de l'animal dans la liste d'animaux
            le comportement  un une instance d'une des classes de comportement
            
        """
        self.faim = faim
        self.soif = soif
        self.vision = vision
        self.vitesse = vitesse
        self.vie = vie
        self.proie = proie
        self.position = position
        self.rang = rang
        self.etat = etat
        
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
        for a in LIVING[rang+1:]:
            a.rang -= 1
        del LIVING[self.rang]
        
    def manger(self,quantite):
        #pour le manger des predateurs, il faudra surcharger la methode
        #car on a dit qu'un predacteur, quand il bouffait, remplissait sa barre d'appettit
        self.appetit += quantite
        
    def boire(self,quantite);
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
                # si c'est de l'eau
                if V[i,j][0] == 1:
                    # si celle-ci est plus proche de l'animal que l'ancienne
                    distance_locale = MAP.distance(self.position,(i,j))
                    if (distance_locale < distance):
                        eau_trouvee = (i,j)
                        distance = distance_locale
        return eau_trouvee
        
    def __str__(self):
        texte = 'faim : {} \nsoif : {} \nvision : {} \nvitesse : {} \nvie : {} \nproie : {} \nposition : {}\nrang : {}\netat : {} \n'.format(self.faim,self.soif,self.vision,self.vitesse,self.vie,self.proie,self.position,self.rang,self.etat)
        
        return(texte)
        


#class Herbivore(Animal):
    
    #def __init__(self,faim,soif,position,rang,etat):
        #super.__init__(faim,soif,3,1,)
        
       
    ## A IMPLEMENTER DANS HERBIVORE    
    # def detecter_predateur(self):
    #     # V est un tableau n x n, ou n est la vision de l'animal 
    #     V = MAP.voisinnage(self.position,self.vision)
    #     taille = len(V)
    #     for i in range(taille):
    #         for j in range(taille):
    #             # ligne a adapter en fonction du type de tableau numpy [int,int] ou [int,object]
    #             if V[i,j] == self.predateur:
    #                 return True
    #     return False
    
    ## a implementer dans herbivore, carnivore et tout : 
    # a_faim, a_soif, a_peur?! etc..;
        

#lapin = Animal(1,2,3,4,5,6,7,8)
#mouton = Animal(2,1,4,3,5,7,6,8)
#carotte = Animal(3,1,5,3,3,7,3,8)
#M = [[1,2,lapin],[3,carotte,4],[mouton,5,6]]
#L = [lapin,carotte,mouton]
