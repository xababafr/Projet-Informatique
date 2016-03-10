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

		
## Terminé
class Solitaire_normal(Etat):
	def action(self):
		if self.animal.a_faim == True and self.animal.a_soif == False:
			self.animal.changer_etat(Solitaire_faim)
		elif self.animal.a_faim == False and self.animal.a_soif == True:
			self.animal.changer_etat(Solitaire_soif)
		elif self.animal.a_faim == True and self.animal.a_soif == True:
			self.animal.changer_etat(Solitaire_faim_soif)
		else:
	# Se deplacer aléatoirement
			case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime toutes les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximite):
					if deplacement_proximite[k] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
	# position est un tuple (i,j)
	
				
## Terminé			
class Solitaire_faim(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		herbivore_trouve = self.animal.detecter_herbivore
	# herbivore_trouve = False si aucun d'herbivore n'est détecté
	# herbivore_trouve = (i,j) si un herbivore est trouvé dans le voisinage
		if herbivore_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[k] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
				case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
				if self.animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
					position_herbivore = self.animal.detecter_herbivore
					while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
						traque = AStar(mappy,position,position_herbivore)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
				self.animal.manger(100) # on remplit la barre d'appétit
				position = self.animal.position
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
			if self.animal.faim == 0:
				self.MAP.suppression(position)
				self.animal.mourir() 
		else: # self.animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
			position_herbivore = self.animal.detecter_herbivore
			while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
				traque = AStar(mappy,position,position_herbivore)
				if self.animal.faim == 0:
					self.MAP.suppression(position)
					self.animal.mourir() 
			self.animal.manger(100) # on remplit la barre d'appétit
			position = self.animal.position

## Terminé		
class Solitaire_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = False si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
		if eau_trouve == False:
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
				case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
				if self.animal.detecter_eau != False:
	# Solitaire se dirige vers la case d'eau : Pathfinder
					position_eau = self.animal.detecter_eau
					while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
						traque = AStar(mappy,position,position_eau)
						if self.animal.soif == 0:
							self.MAP.suppression(position)
							self.animal.mourir()
					self.animal.boire(100) # on remplit la barre de soif
					position = self.animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
			if self.animal.soif == 0:
				self.MAP.suppression(position)
				self.animal.mourir() 
		else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
			position_eau = self.animal.detecter_eau
			while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
				traque = AStar(mappy,position,position_eau)
				if self.animal.soif == 0:
					self.MAP.suppression(position)
					self.animal.mourir()
			self.animal.boire(100) # on remplit la barre de soif
			position = self.animal.position

## Terminé
class Solitaire_faim_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		herbivore_trouve = self.animal.detecter_herbivore and eau_trouve = self.animal.detecter_eau
	# herbivore_trouve = False si aucun d'herbivore n'est détecté ; eau_trouve = False si aucune case d'eau n'est détectée
	# herbivore_trouve = (i,j) si un herbivore est trouvé dans le voisinage ; eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
	# On compare les paramètre faim et soif pour savoir à qui donner la priorité ; Si égalité, on donne la priorité à la soif
		if self.animal.faim < self.animal.soif :
			if herbivore_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
				deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
				for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
					for k in range len(deplacement_proximité):
						if deplacement_proximite[k] is not in case_disponible:
							deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
					self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
					position = self.animal.position
					case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
					if self.animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
						position_herbivore = self.animal.detecter_herbivore
						while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
							traque = AStar(mappy,position,position_herbivore)
							if self.animal.faim == 0:
								self.MAP.suppression(position)
								self.animal.mourir() 
							if self.animal.soif == 0:
								self.MAP.suppression(position)
								self.animal.mourir() 
						self.animal.manger(100) # on remplit la barre d'appétit
						position = self.animal.position
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if self.animal.faim == 0:
					self.MAP.suppression(position)
					self.animal.mourir() 
				if self.animal.soif == 0:
					self.MAP.suppression(position)
					self.animal.mourir() 
			else: # self.animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
				position_herbivore = self.animal.detecter_herbivore
				while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
					traque = AStar(mappy,position,position_herbivore)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
					if self.animal.soif == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
				self.animal.manger(100) # on remplit la barre d'appétit
				position = self.animal.position
		else:
			if eau_trouve == False:
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
					case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
					if self.animal.detecter_eau != False:
	# Solitaire se dirige vers la case d'eau : Pathfinder
						position_eau = self.animal.detecter_eau
						while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
							traque = AStar(mappy,position,position_eau)
							if self.animal.faim == 0:
								self.MAP.suppression(position)
								self.animal.mourir() 
							if self.animal.soif == 0:
								self.MAP.suppression(position)
								self.animal.mourir() 
						self.animal.boire(100) # on remplit la barre de soif
						position = self.animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if self.animal.soif == 0:
					self.MAP.suppression(position)
					self.animal.mourir() 
				if self.animal.faim == 0:
					self.MAP.suppression(position)
					self.animal.mourir()
			else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
				position_eau = self.animal.detecter_eau
				while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
					traque = AStar(mappy,position,position_eau)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
					if self.animal.soif == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
				self.animal.boire(100) # on remplit la barre de soif
				position = self.animal.position
		
#
# Troupeau = problème : il faudrait que tous le troupeau MANGE en même temps et BOIT en même 
#

#
# Inclure un truc pour que les Herbivore reste en eux et se cherche
#

## Terminé
class Herbivore_normal(Etat):
	def action(self):
		if self.animal.a_faim == True and self.animal.a_soif == False:
			self.animal.changer_etat(Herbivore_faim)
		elif self.animal.a_faim == False and self.animal.a_soif == True:
			self.animal.changer_etat(Herbivore_soif)
		elif self.animal.a_faim == True and self.animal.a_soif == True:
			self.animal.changer_etat(Herbivore_faim_soif)
		elif:
	# Se deplacer aléatoirement
			case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime toutes les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[k] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
				case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)

## Terminé			
class Herbivore_faim(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
		position = self.animal.position
	# position est un tuple (i,j)
		nourriture = []
	# nourriture est une liste qui contient toutes les cases contenant de l'herbe
		nourriture_distance = []
	# sol = 0
	# herbe = 1
	# eau = 2
		for k in case_disponible:
			if mappy[case_disponible[k]][0] == 1:
				nourriture = nourriture + case_disponible[k]
				if len(nourriture) == 0:
	# si pas d'herbe à proximité, on déplace l'animal
					deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
					for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
						for k in range len(deplacement_proximité):
							if deplacement_proximite[k] is not in case_disponible:
								deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
								self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
								position = self.animal.position
								case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
						for k in case_disponible:
							if mappy[case_disponible[k]][0] == 1:
								nourriture = nourriture + case_disponible[k]
								if len(nourriture) != 0:
	# on cherche la case d'herbe la plus proche
									nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k]]
									for k in nourriture_distance:
										nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
									traque = AStar(mappy,position,nourriture_proche)
									if self.animal.faim == 0:
										self.MAP.suppression(position)
										self.animal.mourir()
									self.animal.deplacer(nourriture_proche)		
									self.animal.manger(5) # on augmente la faim de 5 
									position = self.animal.position
	# on cherche la case d'herbe la plus proche
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir()
				else:
					nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k]]
					for k in nourriture_distance:
						nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
					traque = AStar(mappy,position,nourriture_proche)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir()
				self.animal.deplacer(nourriture_proche)		
				self.animal.manger(5) # on augmente la faim de 5 
				position = self.animal.position
				
				
## Terminé			
class Herbivore_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = False si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage	
		if eau_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Herbivore se déplace aléatoirement sur une distance de "vitesse" case
			for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
				for k in range len(deplacement_proximité):
					if deplacement_proximite[i] is not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
				position = self.animal.position
				case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
				if self.animal.detecter_eau != False:
	# Herbivore se dirige vers la case d'eau : Pathfinder
					position_eau = self.animal.detecter_eau
					while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
						traque = AStar(mappy,position,position_eau)
					self.animal.boire(100) # on remplit la barre de soif
					position = self.animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
			if self.animal.soif == 0:
				self.MAP.suppression(position)
				self.animal.mourir() 
		else :
	# Herbivore se dirige vers la case d'eau : Pathfinder
			position_eau = self.animal.detecter_eau
			while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
				traque = AStar(mappy,position,position_eau)
			self.animal.boire(100) # on remplit la barre de soif
			position = self.animal.position

## Terminé
class Herbivore_faim_soif(Etat):
	def action(self):
		case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = self.animal.position
	# position est un tuple (i,j)
		eau_trouve = self.animal.detecter_eau
	# eau_trouve = False si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
	# On compare les paramètre faim et soif pour savoir à qui donner la priorité ; Si égalité, on donne la priorité à la soif
		if self.animal.faim < self.animal.soif :
			case_disponible = self.animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			position = self.animal.position
	# position est un tuple (i,j)
			nourriture = []
	# nourriture est une liste qui contient toutes les cases contenant de l'herbe
			nourriture_distance = []
	# sol = 0
	# herbe = 1
	# eau = 2
			for k in case_disponible:
				if mappy[case_disponible[k]][0] == 1:
					nourriture = nourriture + case_disponible[k]
					if len(nourriture) == 0:
	# si pas d'herbe à proximité, on déplace l'animal
						deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
					for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
						for k in range len(deplacement_proximité):
							if deplacement_proximite[k] is not in case_disponible:
								deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
								self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
								position = self.animal.position
								case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
						for k in case_disponible:
							if mappy[case_disponible[k]][0] == 1:
								nourriture = nourriture + case_disponible[k]
								if len(nourriture) != 0:
	# on cherche la case d'herbe la plus proche
									nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k]]
									for k in nourriture_distance:
										nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
									traque = AStar(mappy,position,nourriture_proche)
									if self.animal.faim == 0:
										self.MAP.suppression(position)
										self.animal.mourir()
									self.animal.deplacer(nourriture_proche)		
									self.animal.manger(5) # on augmente la faim de 5 
									position = self.animal.position
	# on cherche la case d'herbe la plus proche
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir()
				else:
					nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k]]
					for k in nourriture_distance:
						nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
					traque = AStar(mappy,position,nourriture_proche)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir()
				self.animal.deplacer(nourriture_proche)		
				self.animal.manger(5) # on augmente la faim de 5 
				position = self.animal.position
		else:
			if eau_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
				deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Herbivore se déplace aléatoirement sur une distance de "vitesse" case
				for k in range self.animal.vitesse:
	# On cherche toutes les cases disponibles à proximité	
					for k in range len(deplacement_proximité):
						if deplacement_proximite[i] is not in case_disponible:
							deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
					self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
					position = self.animal.position
					case_disponible = self.animal.deplacements_possibles()
	# position est un tuple (i,j)
					if self.animal.detecter_eau != False:
	# Herbivore se dirige vers la case d'eau : Pathfinder
						position_eau = self.animal.detecter_eau
						while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
							traque = AStar(mappy,position,position_eau)
							if self.animal.faim == 0:
								self.MAP.suppression(position)
								self.animal.mourir() 
							if self.animal.soif == 0:
								self.MAP.suppression(position)
								self.animal.mourir()
						self.animal.boire(100) # on remplit la barre de soif
						position = self.animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if self.animal.soif == 0:
					self.MAP.suppression(position)
					self.animal.mourir() 
				if self.animal.faim == 0:
					self.MAP.suppression(position)
					self.animal.mourir()
			else :
	# Herbivore se dirige vers la case d'eau : Pathfinder
				position_eau = self.animal.detecter_eau
				while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
					traque = AStar(mappy,position,position_eau)
					if self.animal.faim == 0:
						self.MAP.suppression(position)
						self.animal.mourir() 
					if self.animal.soif == 0:
						self.MAP.suppression(position)
						self.animal.mourir()
				self.animal.boire(100) # on remplit la barre de soif
				position = self.animal.position



## EN CONSTRUCTION
#
# Meute = problème il faudrait que toute la meute BOIVENT en même temps et MANGE en même temps
#

#class Meute_normal(Etat):
#	def action(self):
#		if self.animal.a_faim == True and self.animal.a_soif == False:
#			self.animal.changer_etat(Meute_faim)
#		elif self.animal.a_faim == False and self.animal.a_soif == True:
#			self.animal.changer_etat(Meute_soif)
#		elif self.animal.a_faim == False and self.animal.a_soif == False:
#			self.animal.changer_etat(Meute_faim_soif)

#
# Inclure un truc pour que les meute reste entre eux et se cherche
#
			
#class Meute_soif(Etat):
#		def action(self):
#		case_disponible = self.animal.deplacements_possibles()
#	# case_disponible est une liste des cases disponibles
#		position = self.animal.position
#	# position est un tuple (i,j)
#		eau_trouve = self.animal.detecter_eau
#	# eau_trouve = False si aucune case d'eau n'est détectée
#	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
#		if eau_trouve == False:
#	# Se deplacer aléatoirement
#	# case_disponible est une liste des cases disponibles dans la vision de l'animal
#			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
#	# On supprime tout les cases de proximité indisponible
#	# Meute se déplace aléatoirement sur une distance de "vitesse" case
#			for k in range self.animal.vitesse:
#	# On cherche toutes les cases disponibles à proximité	
#				for k in range len(deplacement_proximité):
#					if deplacement_proximite[i] is not in case_disponible:
#						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
#				self.animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
#				position = self.animal.position
	# position est un tuple (i,j)
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
#			if self.animal.soif == 0:
#				self.MAP.suppression(position)
#				self.animal.mourir() 
#			if self.animal.detecter_eau != False:
#	# Meute se dirige vers la case d'eau : Pathfinder
#				position_eau = self.animal.detecter_eau
#				while position != position_eau: # tant que le Meute n'est pas sur l'eau
#					traque = AStar(mappy,position,position_eau)
#				self.animal.boire(100) # on remplit la barre de soif
#				position = self.animal.position
#		else :
	# Meute se dirige vers la case d'eau : Pathfinder
#			position_eau = self.animal.detecter_eau
#			while position != position_eau: # tant que le Meute n'est pas sur l'eau
#				traque = AStar(mappy,position,position_eau)
#			self.animal.boire(100) # on remplit la barre de soif
#			position = self.animal.position