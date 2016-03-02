# -*- coding: utf-8 -*-

import numpy as np
from abc import ABCMeta , abstractmethod
from random import randint

# classe abstraite
class Etat(metaclass=ABCMeta):

	def __init__(self,animal):
		# on conserve une instance de l'animal concerne
		self.animal = animal

	@abstractmethod
	def action(self):
		pass




## commencons par l'automate du solitaire, le plus facile a coder

class Solitaire_normal(Etat):

	def action(self):
		# en premiere approximation, pas besoin de se deplacer case par case
		# vu que l'on peux marcher sur toutes les cases
		# etats : normal, faim, chasse, soif

		#possibles transitions d'etat
		if self.animal.a_faim():
			self.animal.changer_etat(Solitaire_faim)
		#elif...
		else:
			# sinon, on fais le comportement classique de cet etat
			V = ecosysteme.MAP.voisinnage(self.animal.position,self.animal.vision)
			n = len(V)
			x,y,v = self.animal.position[0],self.animal.position[1],self.animal.vision
			numero = np.random.randint(0,n*n)
			c = 0
			destination = (0,0)
			for i in range(n):
				for j in range(n):
					if c == numero:
						# la position a laquelle on se trouve est (x+i-v,y+j-v)
						# en effet, le tableau V part des coordonnees (0,0), alors qu'en fait on est autour du point (x,y)
						# on commence donc par ajouter x et y a i et j
						# mais le point (x,y) n'est pas en haut a gauche du tableau, mais en plein milieu, donc decale
						# a a position (+v,+v), d'ou le fait que l'on retranche v a chaque coordonnee
						destination = (x+i-v,y+j-v)

						# on peux alors sortir de la double boucle, on a trouve la case que l'on voulait
						break;break;
					c += 1

			ecosysteme.MAP.deplacer_animal((x,y),destination)




class TypeAnimal_etatActuel:
	def action():
		# 1er bloc
		
		if ( conditions_pour_changer_d-etat ):
			self.animal.changer_etat( nouvel_etat )
		if (une_autre_cond ):
			self.animal.changer_etat( un_autre_etat )
		#etc...
		
		
		# 2eme bloc
		# si on a pas changé d'etat, on fais les actions relatives a celui-ci
		
class Solitaire_normal(Etat):
	def action(self):
		if self.animal.a_faim == True:
			self.animal.changer_etat(Solitaire_faim)
		elif self.animal.a_soif == True:
			self.animal.changer_etat(Solitaire_soif)
		elif:
	# Se deplacer aléatoirement
			case_disponible = self.animal.deplacements_possibles
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
	# position est un tuple (i,j)
	
				
			
class Solitaire_faim(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		herbivore_trouve = self.animal.detecter_herbivore
	# herbivore_trouve = False si aucun d'herbivore n'est détecté
	# herbivore_trouve = (i,j) si un herbivore est trouvé dans le voisinage
		if herbivore_trouve == None:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
	# position est un tuple (i,j)
			if self.animal.detecter_herbivore != None:
				position = self.animal.position
	# Solitaire lance la chasse : Pathfinder
				position _herbivore = self.animal.detecter_herbivore
	*************************
		else :
	# Solitaire lance la chasse : Pathfinder
			position_herbivore = self.animal.detecter_herbivore 
	*************************
		
class Solitaire_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = None si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
		if eau_trouve == None:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
	# position est un tuple (i,j)
			if self.animal.detecter_eau != None:
	# Solitaire se dirige vers la case d'eau : Pathfinder
				position_eau = self.animal.detecter_eau
	***************************
		else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
			position_eau = self.animal.detecter_eau
	***************************

#
# Troupeau = problème : il faudrait que tous le troupeau MANGE en même temps et BOIT en même 
#

class Herbivore_normal(Etat):
	def action(self):
		if self.animal.a_faim == True:
			self.animal.changer_etat(Solitaire_faim)
		elif self.animal.a_soif == True:
			self.animal.changer_etat(Solitaire_soif)
			
class Herbivore_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = None si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
		if eau_trouve == None:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
	# position est un tuple (i,j)
			if self.animal.detecter_eau != None:
	# Solitaire se dirige vers la case d'eau : Pathfinder
				position_eau = self.animal.detecter_eau
	***************************
		else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
			position_eau = self.animal.detecter_eau
	***************************
			

#
# Meute = problème il faudrait que toute la meute BOIVENT en même temps et MANGE en même temps
#

class Meute_normal(Etat):
	def action(self):
		if self.animal.a_faim == True:
			self.animal.changer_etat(Solitaire_faim)
		elif self.animal.a_soif == True:
			self.animal.changer_etat(Solitaire_soif)
			
class Meute_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = None si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
		if eau_trouve == None:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
	# position est un tuple (i,j)
			if self.animal.detecter_eau != None:
	# Solitaire se dirige vers la case d'eau : Pathfinder
				position_eau = self.animal.detecter_eau
	***************************
		else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
			position_eau = self.animal.detecter_eau
	***************************
					