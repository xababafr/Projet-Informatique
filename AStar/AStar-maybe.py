#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Node:
    "Un node est l'entité utilisé par l'algorithme A* pour trouver le chemin"
    
    def __init__(self,position=[],dis=0,vol=0,parent=[]):
        self.distance=dis
        self.vol_oiseau=vol
        self.pos_x=position[0]
        self.pos_y=position[1]
        self.parent=parent


#La map que l'on fournit est un double tableau.
#0 = case libre, 1 = case bloquee
#Par exemple : map=[[0,0,1],[1,0,1],[0,0,0]]
#Cela fait : 0 1 0
#            0 0 0   
#            1 1 0

class A_Star:
    "Algorithme de pathfinding"
    
    def __init__(self,debut_xy,fin,map,largeur,hauteur):
        self.liste_ouverte = []
        self.liste_fermee = []
        self.depart= Node(debut_xy,0,0,debut_xy) #node de départ
        self.fin=fin #c'est une position et pas un node
        self.niveau=map 
        self.largeur=largeur
        self.hauteur=hauteur
        
    def pathfinding(self):
        #On active le pathfinding par cette fonction
        self.ajouter_node_liste_ouverte(self.depart,0)
        self.initialisation()
        self.enlever_node_liste_ouverte(self.depart)
        self.ajouter_node_liste_fermee(self.depart, 0)
        
        booleen=1
        reussite=0
        
        #Si dès le départ il n'y a aucune possibilité, on ne cherche pas
        taille=len(self.liste_ouverte)
        if(taille>0):
            while(booleen):

                #Le node que l'on va etudier est "node_actuel".
                #La fonction "trouver_poids_min" renvoie une liste
                #composee d'un node, et de son poids
                node_actuel=self.trouver_poids_min()
                self.enlever_node_liste_ouverte(node_actuel[0])
                self.ajouter_node_liste_fermee(node_actuel[0],node_actuel[1])
                self.test_node_adjacent(node_actuel)
            
                if(len(self.liste_ouverte)==0):
                    booleen=0

                #On cherche si on a rajouter le node final dans la liste fermee
                test=self.chercher_node_liste_fermee_xy(self.fin[0],self.fin[1])
                if(test):
                    booleen=0
                    #reussite=1 signifie qu'il y a un chemin
                    reussite=1
                if(reussite):
                    node=self.get_node_arrive()
                    self.chemin=self.construire_chemin(node)
        return reussite
        
    def initialisation(self):
        #test du node a gauche
        if (self.depart.pos_x!=0):         
            if(self.niveau[self.depart.pos_x-1][self.depart.pos_y]!=1):
                #Si ce node existe, on le rajoute à la liste ouverte
                position_node=[self.depart.pos_x-1,self.depart.pos_y]
                parent=[self.depart.pos_x,self.depart.pos_y]
                vol_oiseau=self.calcul_vol_oiseau(self.depart.pos_x-1,self.depart.pos_y)    
                distance=10
                poids=vol_oiseau+distance
                node= Node(position_node,distance,vol_oiseau,parent)
                self.ajouter_node_liste_ouverte(node,poids)
                
        #test du node a droite
        if (self.depart.pos_x!=self.largeur-1):
            if(self.niveau[self.depart.pos_x+1][self.depart.pos_y]!=1):
                #Si ce node existe, on le rajoute à la liste ouverte
                position_node=[self.depart.pos_x+1,self.depart.pos_y]
                parent=[self.depart.pos_x,self.depart.pos_y]
                vol_oiseau=self.calcul_vol_oiseau(self.depart.pos_x+1,self.depart.pos_y)    
                distance=10
                poids=vol_oiseau+distance
                node= Node(position_node,distance,vol_oiseau,parent)
                self.ajouter_node_liste_ouverte(node,poids)
        
        #test du node en haut       
        if (self.depart.pos_y!=0):
            if(self.niveau[self.depart.pos_x][self.depart.pos_y-1]!=1):
                #Si ce node existe, on le rajoute à la liste ouverte
                position_node=[self.depart.pos_x,self.depart.pos_y-1]
                parent=[self.depart.pos_x,self.depart.pos_y]
                vol_oiseau=self.calcul_vol_oiseau(self.depart.pos_x,self.depart.pos_y-1)    
                distance=10
                poids=vol_oiseau+distance
                node= Node(position_node,distance,vol_oiseau,parent)
                self.ajouter_node_liste_ouverte(node,poids)
                
        #test du node en bas       
        if (self.depart.pos_y!=self.hauteur-1):
            if(self.niveau[self.depart.pos_x][self.depart.pos_y+1]!=1):
                #Si ce node existe, on le rajoute à la liste ouverte
                position_node=[self.depart.pos_x,self.depart.pos_y+1]
                parent=[self.depart.pos_x,self.depart.pos_y]
                vol_oiseau=self.calcul_vol_oiseau(self.depart.pos_x,self.depart.pos_y+1)    
                distance=10
                poids=vol_oiseau+distance
                node= Node(position_node,distance,vol_oiseau,parent)
                self.ajouter_node_liste_ouverte(node,poids)
                
    def test_node_adjacent(self,node_actuel):
        #Test node a gauche du node actuel
        if(node_actuel[0].pos_x!=0):
            if(self.niveau[node_actuel[0].pos_x-1][node_actuel[0].pos_y]!=1):
                test=self.chercher_node_liste_fermee_xy(node_actuel[0].pos_x-1,node_actuel[0].pos_y)
                #Si le node n'est pas dans la liste fermee
                if(test!=1):
                    bool=self.chercher_node_liste_ouverte_xy(node_actuel[0].pos_x-1,node_actuel[0].pos_y)
                    #Si le node adjacent n'est pas dans la liste ouverte, on le rajoute
                    if(bool==0):
                        distance=10+node_actuel[0].distance
                        vol=self.calcul_vol_oiseau(node_actuel[0].pos_x-1,node_actuel[0].pos_y)
                        poids=distance+vol
                        parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                        position=[node_actuel[0].pos_x-1,node_actuel[0].pos_y]
                        node= Node(position,distance,vol,parent) 
                        self.ajouter_node_liste_ouverte(node, poids)
                    else:
                        distance=node_actuel[0].distance+10
                        #La fonction "index_liste_ouverte" retrouve la position du node cherche
                        #dans la liste, et retourne sa position.
                        j=self.index_node_liste_ouverte(node_actuel[0].pos_x-1,node_actuel[0].pos_y)
                        #Si la distance du depart jusqu'a ce node en passant par node actuel est
                        #plus courte que la distance deja enregistre par ce node, on modifie le
                        #node parent et la distance.
                        if(distance<self.liste_ouverte[j][0].distance):
                            self.liste_ouverte[j][0].parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                            self.liste_ouverte[j][0].distance=node_actuel[0].distance+10
                            poids=self.liste_ouverte[j][0].distance+self.liste_ouverte[j].vol
                            self.liste_ouverte[j][1]=poids

                    
        #Test node a droite du node actuel
        if(node_actuel[0].pos_x!=self.largeur-1):
            if(self.niveau[node_actuel[0].pos_x+1][node_actuel[0].pos_y]!=1):
                test=self.chercher_node_liste_fermee_xy(node_actuel[0].pos_x+1,node_actuel[0].pos_y)
                #Si le node n'est pas dans la liste fermee
                if(test!=1):
                    bool=self.chercher_node_liste_ouverte_xy(node_actuel[0].pos_x+1,node_actuel[0].pos_y)
                    #Si le node adjacent n'est pas dans la liste ouverte, on le rajoute
                    if(bool==0):
                        distance=10+node_actuel[0].distance
                        vol=self.calcul_vol_oiseau(node_actuel[0].pos_x+1,node_actuel[0].pos_y)
                        poids=distance+vol
                        parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                        position=[node_actuel[0].pos_x+1,node_actuel[0].pos_y]
                        node= Node(position,distance,vol,parent) 
                        self.ajouter_node_liste_ouverte(node, poids)
                    else:
                        distance=node_actuel[0].distance+10
                        #La fonction "index_liste_ouverte" retrouve la position du node cherche
                        #dans la liste, et retourne sa position.
                        j=self.index_node_liste_ouverte(node_actuel[0].pos_x+1,node_actuel[0].pos_y)
                        #Si la distance du depart jusqu'a ce node en passant par node actuel est
                        #plus courte que la distance deja enregistre par ce node, on modifie le
                        #node parent et la distance.
                        if(distance<self.liste_ouverte[j][0].distance):
                            self.liste_ouverte[j][0].parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                            self.liste_ouverte[j][0].distance=node_actuel[0].distance+10
                            poids=self.liste_ouverte[j][0].distance+self.liste_ouverte[j].vol
                            self.liste_ouverte[j][1]=poids       
                            
        
        #test node en haut du node actuel
        if(node_actuel[0].pos_y!=0):
            if(self.niveau[node_actuel[0].pos_x][node_actuel[0].pos_y-1]!=1):
                test=self.chercher_node_liste_fermee_xy(node_actuel[0].pos_x,node_actuel[0].pos_y-1)
                #Si le node n'est pas dans la liste fermee
                if(test!=1):
                    bool=self.chercher_node_liste_ouverte_xy(node_actuel[0].pos_x,node_actuel[0].pos_y-1)
                    #si le node adjacent n'est pas dans la liste ouverte, on le rajoute
                    if(bool==0):
                        distance=10+node_actuel[0].distance
                        vol=self.calcul_vol_oiseau(node_actuel[0].pos_x,node_actuel[0].pos_y-1)
                        poids=distance+vol
                        parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                        position=[node_actuel[0].pos_x,node_actuel[0].pos_y-1]
                        node= Node(position,distance,vol,parent) 
                        self.ajouter_node_liste_ouverte(node, poids)
                    else:
                        distance=node_actuel[0].distance+10
                        #La fonction "index_liste_ouverte" retrouve la position du node cherche
                        #dans la liste, et retourne sa position.
                        j=self.index_node_liste_ouverte(node_actuel[0].pos_x,node_actuel[0].pos_y-1)
                        #Si la distance du depart jusqu'a ce node en passant par node actuel est
                        #plus courte que la distance deja enregistre par ce node, on modifie le
                        #node parent et la distance.
                        if(distance<self.liste_ouverte[j][0].distance):
                            self.liste_ouverte[j][0].parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                            self.liste_ouverte[j][0].distance=node_actuel[0].distance+10
                            poids=self.liste_ouverte[j][0].distance+self.liste_ouverte[j].vol
                            self.liste_ouverte[j][1]=poids 
                            
                            
        #test node en bas du node actuel
        if(node_actuel[0].pos_y!=self.hauteur-1):
            if(self.niveau[node_actuel[0].pos_x][node_actuel[0].pos_y+1]!=1):
                test=self.chercher_node_liste_fermee_xy(node_actuel[0].pos_x,node_actuel[0].pos_y+1)
                #Si le node n'est pas dans la liste fermee
                if(test!=1):
                    bool=self.chercher_node_liste_ouverte_xy(node_actuel[0].pos_x,node_actuel[0].pos_y+1)
                    #si le node adjacent n'est pas dans la liste ouverte, on le rajoute
                    if(bool==0):
                        distance=10+node_actuel[0].distance
                        vol=self.calcul_vol_oiseau(node_actuel[0].pos_x,node_actuel[0].pos_y+1)
                        poids=distance+vol
                        parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                        position=[node_actuel[0].pos_x,node_actuel[0].pos_y+1]
                        node= Node(position,distance,vol,parent) 
                        self.ajouter_node_liste_ouverte(node, poids)
                    else:
                        distance=node_actuel[0].distance+10
                        #La fonction "index_liste_ouverte" retrouve la position du node cherche
                        #dans la liste, et retourne sa position.
                        j=self.index_node_liste_ouverte(node_actuel[0].pos_x,node_actuel[0].pos_y+1)
                        #Si la distance du depart jusqu'a ce node en passant par node actuel est
                        #plus courte que la distance deja enregistre par ce node, on modifie le
                        #node parent et la distance.
                        if(distance<self.liste_ouverte[j][0].distance):
                            self.liste_ouverte[j][0].parent=[node_actuel[0].pos_x,node_actuel[0].pos_y]
                            self.liste_ouverte[j][0].distance=node_actuel[0].distance+10
                            poids=self.liste_ouverte[j][0].distance+self.liste_ouverte[j].vol
                            self.liste_ouverte[j][1]=poids 
                
    def construire_chemin(self,arrive):
        #On commence par mettre la position finale et on remonte par les parents
        chemin=[self.fin]
        chemin.append(arrive.parent)
        continuer=1
        i=1
        
        while(continuer):
            if(chemin[i][0]==self.depart.pos_x and chemin[i][1]==self.depart.pos_y):
                    continuer=0
            else:
                node=self.get_node_liste_fermee(chemin[i])
                chemin.append(node.parent)
                i=i+1
                
        chemin.reverse()
        #On supprime la position de depart
        del chemin[0]
        return chemin    
        
    def trouver_poids_min(self):
        min=10000
        valeur=0
        node=self.liste_ouverte[0]
        for iterateur in self.liste_ouverte:
            valeur = iterateur[1]
            if(valeur<min):
                min=valeur
                node=iterateur
        node_valeur=[node[0],min]
        return node_valeur  
            
    def calcul_vol_oiseau(self,x,y):
        abscisse=self.fin[0]-x
        ordonnee=self.fin[1]-y
        vol=abscisse+ordonnee
        return vol
        
    def ajouter_node_liste_ouverte(self,node,valeur):
        self.liste_ouverte.append([node,valeur])
        
    def enlever_node_liste_ouverte(self,node):
        i=0
        for iterateur in self.liste_ouverte:
            if(iterateur[0].pos_x==node.pos_x and iterateur[0].pos_y==node.pos_y):
                del self.liste_ouverte[i]
              
            i=i+1
            
    def chercher_node_liste_ouverte_xy(self,x,y):
        booleen=0
        for iterateur in self.liste_ouverte:
            if(iterateur[0].pos_x==x and iterateur[0].pos_y==y):
                booleen=1
        return booleen
    
    def index_node_liste_ouverte(self,x,y):
        i=0
        index=0
        for iterateur in self.liste_ouverte:
            if(iterateur[0].pos_x==x and iterateur[0].pos_y==y):
                index=i
            i=i+1
        return index
        
    def ajouter_node_liste_fermee(self,node,valeur):
        self.liste_fermee.append([node,valeur])
        
    def chercher_node_liste_fermee(self,node):
        booleen=0
        for iterateur in self.liste_fermee:
            if(iterateur[0].pos_x==node.pos_x and iterateur[0].pos_y==node.pos_y):
                booleen=1
        return booleen
    
    def chercher_node_liste_fermee_xy(self,x,y):
        booleen=0
        for iterateur in self.liste_fermee:
            if(iterateur[0].pos_x==x and iterateur[0].pos_y==y):
                booleen=1
        return booleen
    
    def get_node_liste_fermee(self,coordonnee):
        node=0
        for iterateur in self.liste_fermee:
            if(iterateur[0].pos_x==coordonnee[0] and iterateur[0].pos_y==coordonnee[1]):
                node=iterateur[0] 
        return node 
    
    def get_node_arrive(self):
        node=0
        for iterateur in self.liste_fermee:
            if(iterateur[0].pos_x==self.fin[0] and iterateur[0].pos_y==self.fin[1]):
                node=iterateur[0]
        return node 
    
    def get_chemin(self):
        return self.chemin
