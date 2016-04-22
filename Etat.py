# -*- coding: utf-8 -*-

import numpy as np
#from abc import ABCMeta , abstractmethod
from random import randint
import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
from Animal import *
from AStar import *

# classe abstraite
class Etat():

	#def __init__(self,animal):
		# on conserve une instance de l'animal concerne
		#animal = animal

	def action(self,animal):
		pass
		
	# si (x,y) est la position de l'animal, v sa vision, et (i,j)
	# la position locale, la position globale sera (x+i-v,y+j-v)
	def local_to_global(self,animal,pos):
		i,j = pos[0],pos[1]
		x,y = animal.position
		v = animal.vision
		return (x+i-v,y+j-v)
		
	# autant ecrire la réciproque
	# je recupere (x+i-v,y+j-v), et je veux (i,j)
	def global_to_local(self,animal,pos):
		p1,p2 = pos[0],pos[1]
		x,y = animal.position
		v = animal.vision
		return (p1-x+v,p2-y+v)
		
	def deplacement_aleatoire(self,animal):
		
		position = animal.position
		case_disponible = animal.deplacements_possibles()
		deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
		
		dep = deplacement_proximite.copy()
		
# quand les herbivores sont en deplacement aléatoire, ils n'ont pas faim, ou viennent
# juste de la rassasier. Donc meme les carnivores évitent les herbivores, ça ne les 
# intéressent pas. Donc ici, les animaux se considèrent les uns les autres commes obstacles

		for i in range(len(deplacement_proximite)):
			x,y = deplacement_proximite[i][0],deplacement_proximite[i][1]
			if isinstance(animal.ecosysteme.MAP.MAP[x,y][1],Animal):
				dep.remove(deplacement_proximite[i])

		
		"""# uniquement les cases voisines, deplacement en diagonale interdit, comme pour le pathfinder
		deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1)]"""
		deplacement_proximite2 = dep.copy()
		# On cherche toutes les cases disponibles à proximité	
		for k in range(len(deplacement_proximite)):
			if (deplacement_proximite[k] not in case_disponible):
				deplacement_proximite2.remove(deplacement_proximite[k])
		pos_future = deplacement_proximite2[randint(0,len(deplacement_proximite2))-1]
		print('deplacer de '+str(position)+' à '+str(pos_future))
		return(pos_future)
		

		
## Terminé
class Solitaire_normal(Etat):
	def action(self,animal):
		print("NORMAL")
		
		# transitions
		if animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Solitaire_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Solitaire_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Solitaire_faim_soif())
			animal.etat.action(animal)
		else:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
	# On supprime toutes les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for v in range(animal.vitesse):
				animal.deplacer(self.deplacement_aleatoire(animal))
				
	# position est un tuple (i,j)
	

## Terminé		
class Solitaire_soif(Etat):
	
	def apres_transition(self,animal):
		for v in range(animal.vitesse):
			# il faut à chaque tour rechercher de l'eau et refaire le pathfinder,
			# car se deplacer aleatoirement peut positionner l'animal de maniere plus favorable
			eau_trouvee = animal.detecter_eau()
			
			if not eau_trouvee:
				print("not eau trouvee")
				animal.deplacer(self.deplacement_aleatoire(animal))
			else:
				pos = self.global_to_local(animal,animal.position) # position locale de l'animal = (v,v)
				print("ok eau trouvee : "+str(eau_trouvee)+" pos locale animal : "+str(pos))
				# on se dirige vers l'eau avec le pathfinder
				# la map est la vision de l'animal, le depart sa position, l'arrivee est l'eau trouvee
				
				# si on est sur la case où se trouve de l'eau
				if eau_trouvee == pos:
					print("glouglou")
					animal.soif += 100 # le setter s'assure que la soif sera au maximum et correcte
					# il faut s'assurer que le pathfinder ne soit jamais appelé, il renverrait sinon
					# une erreur vu que depart = arrivée
					# maintenant que l'animal n'a plus soif, on le fais bouger aléatoirement le nombre
					# de fois qu'il lui reste (3 mvmts / tour) puis il passera à l'appel de un_tour()
					# suivant dans un etat Solitaire_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
						# on sort du for v in range..
					break

				else: # si chemin à trouver il y a bien
				
					## ICI, on prends le pathfinder de l'herbivore : le tigre n'a pas faim!
					astar = PathFinderH(animal.get_voisinnage(),pos,eau_trouvee)
					chemin = astar.find_path()
					if (not chemin): # s'il n'y a pas de chemin 
						print("not chemin")
						animal.deplacer(self.deplacement_aleatoire(animal)) 
					else:
						print("ok chemin")
						# s'il y en a un, on se deplace d'une case dans la bonne direction
						# la methode deplacer demande la position absolue, et non relative
						animal.deplacer(self.local_to_global(animal,chemin[0]))
						# si ce deplacement l'a amené là ou il voulait se retrouver
						"""if animal.position == self.local_to_global(animal,eau_trouvee):
							print("glouglou")
							animal.boire(100) # le setter s'assure que la soif sera au maximum et correcte"""
					
				# note : pas besoin de gerer la mort de soif pendant la "traque", celle-ci
				# est gérée automatiquement dans l'appel de un_tour()
	
	def action(self,animal):
		print("SOIF")
		
		# transitions
		if animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Solitaire_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Solitaire_normal())
			animal.etat.action(animal)
		# s'il a faim et soif
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Solitaire_faim_soif())
			animal.etat.action(animal)
		
		else:
			
			self.apres_transition(animal)

			
				
## Terminé			
class Solitaire_faim(Etat):
	
	def __init__(self):
		self.chasse_reussie = False
	
	def apres_transition(self,animal):
		
		for v in range(animal.vitesse):
			# il faut à chaque tour rechercher de l'eau et refaire le pathfinder,
			# car se deplacer aleatoirement peut positionner l'animal de maniere plus favorable
			herbivore_trouvee = animal.detecter_herbivore()
			
			if not herbivore_trouvee:
				# si on est sur la case où se trouve de l'herbivore
				if self.chasse_reussie:
					
					## ici, il faut buter l'animal en le supprimant du living
					L = animal.ecosysteme.LIVING
					for ani in L:
						# animal = le predateur, ani = on parcours la liste living
						if ani.position == animal.position and isinstance(ani, Herbivore): 
							ani.mourir(False)
					# l'herbivore a déjà disparu de la carte => 2eme param de mourir = False
					
					print("miammiam")
					animal.faim += 100 # le setter s'assure que la faim sera au maximum et correcte
					# il faut s'assurer que le pathfinder ne soit jamais appelé, il renverrait sinon
					# une erreur vu que depart = arrivée
					# maintenant que l'animal n'a plus faim, on le fais bouger aléatoirement le nombre
					# de fois qu'il lui reste (3 mvmts / tour) puis il passera à l'appel de un_tour()
					# suivant dans un etat Solitaire_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
					# et on sort du for v in...
					break
				else:
					print("not herbivore trouvee")
					animal.deplacer(self.deplacement_aleatoire(animal))
			else:
				pos = self.global_to_local(animal,animal.position) # position locale de l'animal = (v,v)
				print("ok herbivore trouvee : "+str(herbivore_trouvee)+" pos locale animal : "+str(pos))
				# on se dirige vers l'herbivore avec le pathfinder
				# la map est la vision de l'animal, le depart sa position, l'arrivee est l'herbivore trouvee
				
				
				astar = PathFinderS(animal.get_voisinnage(),pos,herbivore_trouvee)
				chemin = astar.find_path()
				if (not chemin): # s'il n'y a pas de chemin 
					print("not chemin")
					animal.deplacer(self.deplacement_aleatoire(animal)) 
				else:
					print("ok chemin")
					# s'il y en a un, on se deplace d'une case dans la bonne direction
					# la methode deplacer demande la position absolue, et non relative
					
					# quand on se deplace sur l'animal, on le supprime : du coup
					# detecter_herbivore ne renvoi + rien, et par conséquent c'est
					# comme si l'animal ne l'avait pas mangé
					#remédions à ce problème
					if chemin[0] == herbivore_trouvee:
						self.chasse_reussie = True
					animal.deplacer(self.local_to_global(animal,chemin[0]))
	
	
	def action(self,animal):
		print("FAIM")
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Solitaire_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Solitaire_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Solitaire_faim_soif())
			animal.etat.action(animal)
				
		else:
			
			self.apres_transition(animal)
			
			
class Solitaire_faim_soif(Etat):
	def action(self,animal):
		
		print("FAIM SOIF, ",end='')
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Solitaire_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Solitaire_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Solitaire_faim())
			animal.etat.action(animal)
		else:
			
			if animal.faim < animal.soif:
				etat = Solitaire_faim()
				print("faim")
			else:
				etat = Solitaire_soif()
				print("soif")
			etat.apres_transition(animal)
		


class Herbivore_normal(Etat):
	def action(self,animal,faire_transitions = True):
		print("NORMAL")
		
		# transitions
		if animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Herbivore_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Herbivore_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Herbivore_faim_soif())
			animal.etat.action(animal)
		else:

			for v in range(animal.vitesse):
				animal.deplacer(self.deplacement_aleatoire(animal))
				
			
class Herbivore_soif(Etat):
	
	def apres_transition(self,animal):
		for v in range(animal.vitesse):
			# il faut à chaque tour rechercher de l'eau et refaire le pathfinder,
			# car se deplacer aleatoirement peut positionner l'animal de maniere plus favorable
			eau_trouvee = animal.detecter_eau()
			
			if not eau_trouvee:
				print("not eau trouvee")
				animal.deplacer(self.deplacement_aleatoire(animal))
			else:
				pos = self.global_to_local(animal,animal.position) # position locale de l'animal = (v,v)
				print("ok eau trouvee : "+str(eau_trouvee)+" pos locale animal : "+str(pos))
				# on se dirige vers l'eau avec le pathfinder
				# la map est la vision de l'animal, le depart sa position, l'arrivee est l'eau trouvee
				
				# si on est sur la case où se trouve de l'eau
				if eau_trouvee == pos:
					print("glouglou")
					animal.soif += 100 # le setter s'assure que la soif sera au maximum et correcte
					# il faut s'assurer que le pathfinder ne soit jamais appelé, il renverrait sinon
					# une erreur vu que depart = arrivée
					# maintenant que l'animal n'a plus soif, on le fais bouger aléatoirement le nombre
					# de fois qu'il lui reste (3 mvmts / tour) puis il passera à l'appel de un_tour()
					# suivant dans un etat Solitaire_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
						# on sort du for v in range..
					break

				else: # si chemin à trouver il y a bien
				
					astar = PathFinderH(animal.get_voisinnage(),pos,eau_trouvee)
					chemin = astar.find_path()
					if (not chemin): # s'il n'y a pas de chemin 
						print("not chemin")
						animal.deplacer(self.deplacement_aleatoire(animal)) 
					else:
						print("ok chemin")
						# s'il y en a un, on se deplace d'une case dans la bonne direction
						# la methode deplacer demande la position absolue, et non relative
						animal.deplacer(self.local_to_global(animal,chemin[0]))
						# si ce deplacement l'a amené là ou il voulait se retrouver
						"""if animal.position == self.local_to_global(animal,eau_trouvee):
							print("glouglou")
							animal.boire(100) # le setter s'assure que la soif sera au maximum et correcte"""
					
				# note : pas besoin de gerer la mort de soif pendant la "traque", celle-ci
				# est gérée automatiquement dans l'appel de un_tour()
	
	def action(self,animal):
		print("SOIF")
		
		# transitions
		if animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Herbivore_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Herbivore_normal())
			animal.etat.action(animal)
		# s'il a faim et soif
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Herbivore_faim_soif())
			animal.etat.action(animal)
		
		else:
			
			self.apres_transition(animal)
					

class Herbivore_faim(Etat):
	
	def apres_transition(self,animal):
		
		for v in range(animal.vitesse):
			# il faut à chaque tour rechercher de l'eau et refaire le pathfinder,
			# car se deplacer aleatoirement peut positionner l'animal de maniere plus favorable
			herbe_trouvee = animal.detecter_herbe()
			
			if not herbe_trouvee:
				print("not herbe trouvee")
				animal.deplacer(self.deplacement_aleatoire(animal))
			else:
				pos = self.global_to_local(animal,animal.position) # position locale de l'animal = (v,v)
				print("ok herbe trouvee : "+str(herbe_trouvee)+" pos locale animal : "+str(pos))
				# on se dirige vers l'herbe avec le pathfinder
				# la map est la vision de l'animal, le depart sa position, l'arrivee est l'herbe trouvee
				
				# si on est sur la case où se trouve de l'herbe
				if herbe_trouvee == pos:
					print("miammiam")
					animal.faim += 100 # le setter s'assure que la faim sera au maximum et correcte
					# il faut s'assurer que le pathfinder ne soit jamais appelé, il renverrait sinon
					# une erreur vu que depart = arrivée
					# maintenant que l'animal n'a plus faim, on le fais bouger aléatoirement le nombre
					# de fois qu'il lui reste (3 mvmts / tour) puis il passera à l'appel de un_tour()
					# suivant dans un etat Solitaire_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
						# on sort du for v in range..
					break

				else: # si chemin à trouver il y a bien
				
					astar = PathFinderH(animal.get_voisinnage(),pos,herbe_trouvee)
					chemin = astar.find_path()
					if (not chemin): # s'il n'y a pas de chemin 
						print("not chemin")
						animal.deplacer(self.deplacement_aleatoire(animal)) 
					else:
						print("ok chemin")
						# s'il y en a un, on se deplace d'une case dans la bonne direction
						# la methode deplacer demande la position absolue, et non relative
						animal.deplacer(self.local_to_global(animal,chemin[0]))
	
	
	def action(self,animal):
		print("FAIM")
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Herbivore_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Herbivore_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Herbivore_faim_soif())
			animal.etat.action(animal)
				
		else:
			
			self.apres_transition(animal)

							
							
class Herbivore_faim_soif(Etat):
	def action(self,animal):
		
		print("FAIM SOIF, ",end='')
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Herbivore_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Herbivore_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Herbivore_faim())
			animal.etat.action(animal)
		else:
			
			if animal.faim < animal.soif:
				etat = Herbivore_faim()
				print("faim")
			else:
				etat = Herbivore_soif()
				print("soif")
			etat.apres_transition(animal)
			

##MAIN

"""

###########################################################################################################
COMMENT SE SERVIR DE NOTRE PROGRAMME : 

le main qui suit permet au correcteur de verifier le comptement de nos herbivores
et prédateurs (note :  les herbivores n'ont pour le moment ni comportement de meute,
ni comportement de fuite, mais cela ne saurait tarder)

Pour commencer, éxécutez le fichier Etat.py, le main ci-dessous créé l'écosysteme 
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
###########################################################################################################

"""

if __name__ == "__main__":
	
	import sys
	sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
	import numpy as np
	from Animal import *
	from Map import *
	from AStar import *
	from CustomList import *
	
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
		def __init__(self,MAP,LIVING):
			self.MAP = Map(np.array(MAP),Rien())
			self.LIVING = LIVING
			self.CORPSES = CustomList()
			
		def add_animal(self,animal):
			self.LIVING.append(animal)
			self.MAP.add_animal(animal)
		
		# retourne le rang d'un animal qui viendrait a etre ajouté à la fin de LIVING
		def get_rang(self):
			return len(self.LIVING)
	
	
	# test Solitaire_normal
	ecosysteme = Ecosysteme(np.array(mappy2),[])
	tigre = Solitaire(ecosysteme,(4,3),ecosysteme.get_rang(),Solitaire_normal())
	ecosysteme.add_animal(tigre)
	lapin = Herbivore(ecosysteme,(8,5),ecosysteme.get_rang(),Herbivore_normal())
	ecosysteme.add_animal(lapin)
	