# -*- coding: utf-8 -*-

## de la meme maniere qu'au final j'ai du passer ecosysteme en
## attribut de Animal(), il faudra ptet pour la meme raison
## le passer en argument à ahcaque action() pour le faire 
## transiter du main vers les autres fichiers

## penser à revérifier le décorateur de la position

## un animal peux potentiellement etre bodyblock et donc ne pas pouvoir bouger : pr l'istant
## ce cas n'est pas pris en compte
## en fait si, dans ce cas là, je fais un deplacement aléatoire (je suis trop fort) (Your name is God ;) )

"""le probleme de liste index out of range sur tigre.un_tour() : 

quand je fais (x+i-v, .. ) si v est trop grand, on passe en 
negatif, du oup l'appel à la fonction position_correcte() 
balance que des 0. Donc en fait faut pas faire x+i-v, mais :
v2 = min(v distance_a_un_bord) puis (x+i-v2)
"""

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
		
		# les herbivores doivent éviter de collisionner les autres animaux
		# les solitaires doivent éviter de colllisionner leurs semblables
		# donc ils evitent tous les solitaires et les herbivores evitetn aussi leur semblables
		for i in range(len(deplacement_proximite)):
			x,y = deplacement_proximite[i][0],deplacement_proximite[i][1]
			if isinstance(animal.ecosysteme.MAP.MAP[x,y][1],Solitaire):
				dep.remove(deplacement_proximite[i])
			if isinstance(animal,Herbivore):
				if isinstance(animal.ecosysteme.MAP.MAP[x,y][1],Herbivore):
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
		
## Solitaire		
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
				
					astar = PathFinderS(animal.get_voisinnage(),pos,eau_trouvee)
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
				# si on est sur la case où se trouve de l'herbe
				if self.chasse_reussie:
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
			
## Terminé			
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
			
## Charognard		
## Terminé
class Charognard_normal(Etat):
	def action(self,animal):
		print("NORMAL")
		
		# transitions
		if animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Charognard_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Charognard_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Charognard_faim_soif())
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
class Charognard_soif(Etat):
	
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
					# suivant dans un etat Charognard_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
						# on sort du for v in range..
					break

				else: # si chemin à trouver il y a bien
				
					astar = PathFinderS(animal.get_voisinnage(),pos,eau_trouvee)
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
			animal.changer_etat(Charognard_faim())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Charognard_normal())
			animal.etat.action(animal)
		# s'il a faim et soif
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Charognard_faim_soif())
			animal.etat.action(animal)
		
		else:
			
			self.apres_transition(animal)

## Terminé
class Charognard_faim(Etat):
	
	def __init__(self):
		self.chasse_reussie = False
	
	def apres_transition(self,animal):
		
		for v in range(animal.vitesse):
			# il faut à chaque tour rechercher le mort et refaire le pathfinder,
			# car se deplacer aleatoirement peut positionner l'animal de maniere plus favorable
			mort_trouve = animal.detecter_mort()
			
			if not mort_trouve:
				# si on est sur la case où se trouve le mort
				if self.chasse_reussie:
					print("miammiam")
					animal.faim += 100 # le setter s'assure que la faim sera au maximum et correcte
					# il faut s'assurer que le pathfinder ne soit jamais appelé, il renverrait sinon
					# une erreur vu que depart = arrivée
					# maintenant que l'animal n'a plus faim, on le fais bouger aléatoirement le nombre
					# de fois qu'il lui reste (3 mvmts / tour) puis il passera à l'appel de un_tour()
					# suivant dans un etat Charognard_normal() !
					
					for k in range(2-v):
						animal.deplacer(self.deplacement_aleatoire(animal))
					# et on sort du for v in...
					break
				else:
					print("not mort trouve")
					animal.deplacer(self.deplacement_aleatoire(animal))
			else:
				pos = self.global_to_local(animal,animal.position) # position locale de l'animal = (v,v)
				print("ok mort trouve : "+str(mort_trouve)+" pos locale animal : "+str(pos))
				# on se dirige vers le mort avec le pathfinder
				# la map est la vision de l'animal, le depart sa position, l'arrivee est le mort trouve
				
				
				astar = PathFinderS(animal.get_voisinnage(),pos,mort_trouve)
				chemin = astar.find_path()
				if (not chemin): # s'il n'y a pas de chemin 
					print("not chemin")
					animal.deplacer(self.deplacement_aleatoire(animal)) 
				else:
					print("ok chemin")
					# s'il y en a un, on se deplace d'une case dans la bonne direction
					# la methode deplacer demande la position absolue, et non relative
					
					# quand on se deplace sur l'animal, on le supprime : du coup
					# detecter_mort ne renvoi + rien, et par conséquent c'est
					# comme si l'animal ne l'avait pas mangé
					# remédions à ce problème
					if chemin[0] == mort_trouvee:
						self.chasse_reussie = True
					animal.deplacer(self.local_to_global(animal,chemin[0]))
	
	
	def action(self,animal):
		print("FAIM")
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Charognard_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Charognard_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == True:
			animal.changer_etat(Charognard_faim_soif())
			animal.etat.action(animal)
				
		else:
			self.apres_transition(animal)

## Terminé			
class Charognard_faim_soif(Etat):
	def action(self,animal):
		
		print("FAIM SOIF, ",end='')
		
		# transitions
		if animal.a_faim() == False and animal.a_soif() == True:
			animal.changer_etat(Charognard_soif())
			animal.etat.action(animal)
		elif animal.a_faim() == False and animal.a_soif() == False:
			animal.changer_etat(Charognard_normal())
			animal.etat.action(animal)
		elif animal.a_faim() == True and animal.a_soif() == False:
			animal.changer_etat(Charognard_faim())
			animal.etat.action(animal)
		else:
			
			if animal.faim < animal.soif:
				etat = Solitaire_faim()
				print("faim")
			else:
				etat = Solitaire_soif()
				print("soif")
			etat.apres_transition(animal)	
			
## Herbivore
## Terminé
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
				
## Terminé
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
					
## Terminé
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

## Terminé														
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
	
	
	"""ecosysteme = Ecosysteme(np.array(mappy),[])
	lapin = Herbivore(ecosysteme,(3,3),ecosysteme.get_rang(),Herbivore_normal())
	ecosysteme.add_animal(lapin)
	lapin2 = Herbivore(ecosysteme,(3,5),ecosysteme.get_rang(),Herbivore_normal())
	ecosysteme.add_animal(lapin2)
	tigre = Solitaire(ecosysteme,(3,5),ecosysteme.get_rang(),Solitaire_normal())
	ecosysteme.add_animal(tigre)
	tigre2 = Solitaire(ecosysteme,(3,3),ecosysteme.get_rang(),Solitaire_normal())
	ecosysteme.add_animal(tigre2)"""

## Terminé
"""class Solitaire_faim_soif(Etat):
	
	def action(self,animal):
		print("FAIM SOIF")
		case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = animal.position
	# position est un tuple (i,j)
		herbivore_trouve = animal.detecter_herbivore
		eau_trouve = animal.detecter_eau
	# herbivore_trouve = False si aucun d'herbivore n'est détecté ; eau_trouve = False si aucune case d'eau n'est détectée
	# herbivore_trouve = (i,j) si un herbivore est trouvé dans le voisinage ; eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
	# On compare les paramètre faim et soif pour savoir à qui donner la priorité ; Si égalité, on donne la priorité à la soif
		if animal.faim < animal.soif :
			if herbivore_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
				deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
				for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
					for k in range(len(deplacement_proximité)):
						if deplacement_proximite[k] not in case_disponible:
							deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
					animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
					position = animal.position
					case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
					if animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
						position_herbivore = animal.detecter_herbivore
						while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
							traque = AStar(mappy,position,position_herbivore)
							if animal.faim == 0:
								self.MAP.suppression(position)
								animal.mourir() 
							if animal.soif == 0:
								self.MAP.suppression(position)
								animal.mourir() 
						animal.manger(100) # on remplit la barre d'appétit
						position = animal.position
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if animal.faim == 0:
					self.MAP.suppression(position)
					animal.mourir() 
				if animal.soif == 0:
					self.MAP.suppression(position)
					animal.mourir() 
			else: # animal.detecter_herbivore != False:
	# Solitaire lance la chasse : Pathfinder
				position_herbivore = animal.detecter_herbivore
				while position != position_herbivore: # tant que le Solitaire n'est pas sur l'Herbivore
					traque = AStar(mappy,position,position_herbivore)
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir() 
					if animal.soif == 0:
						self.MAP.suppression(position)
						animal.mourir() 
				animal.manger(100) # on remplit la barre d'appétit
				position = animal.position
		else:
			if eau_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
				deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
				for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
					for k in range(len(deplacement_proximité)):
						if deplacement_proximite[i] not in case_disponible:
							deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
					animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
					position = animal.position
					case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
					if animal.detecter_eau != False:
	# Solitaire se dirige vers la case d'eau : Pathfinder
						position_eau = animal.detecter_eau
						while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
							traque = AStar(mappy,position,position_eau)
							if animal.faim == 0:
								self.MAP.suppression(position)
								animal.mourir() 
							if animal.soif == 0:
								self.MAP.suppression(position)
								animal.mourir() 
						animal.boire(100) # on remplit la barre de soif
						position = animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if animal.soif == 0:
					self.MAP.suppression(position)
					animal.mourir() 
				if animal.faim == 0:
					self.MAP.suppression(position)
					animal.mourir()
			else :
	# Solitaire se dirige vers la case d'eau : Pathfinder
				position_eau = animal.detecter_eau
				while position != position_eau: # tant que le Solitaire n'est pas sur l'eau
					traque = AStar(mappy,position,position_eau)
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir() 
					if animal.soif == 0:
						self.MAP.suppression(position)
						animal.mourir() 
				animal.boire(100) # on remplit la barre de soif
				position = animal.position"""
		
#
# Troupeau = problème : il faudrait que tous le troupeau MANGE en même temps et BOIT en même 
#

#
# Inclure un truc pour que les Herbivore reste en eux et se cherche
#

## Autres
"""class Herbivore_normal(Etat):
	def action(self,animal):
		if animal.a_faim == True and animal.a_soif == False:
			animal.changer_etat(Herbivore_faim)
		elif animal.a_faim == False and animal.a_soif == True:
			animal.changer_etat(Herbivore_soif)
		elif animal.a_faim == True and animal.a_soif == True:
			animal.changer_etat(Herbivore_faim_soif)
		else:
	# Se deplacer aléatoirement
			case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime toutes les cases de proximité indisponible
	# Solitaire se déplace aléatoirement sur une distance de "vitesse" case
			for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
				for k in range(len(deplacement_proximité)):
					if deplacement_proximite[k] not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
				animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
				position = animal.position
				case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)

## Terminé			
class Herbivore_faim(Etat):
	def action(self,animal):
		case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
		position = animal.position
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
					for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
						for k in range(len(deplacement_proximité)):
							if deplacement_proximite[k] not in case_disponible:
								deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
								animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
								position = animal.position
								case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
						for k in case_disponible:
							if mappy[case_disponible[k]][0] == 1:
								nourriture = nourriture + case_disponible[k]
								if len(nourriture) != 0:
	# on cherche la case d'herbe la plus proche
									nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k])]
									for k in nourriture_distance:
										nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
									traque = AStar(mappy,position,nourriture_proche)
									if animal.faim == 0:
										self.MAP.suppression(position)
										animal.mourir()
									animal.deplacer(nourriture_proche)		
									animal.manger(5) # on augmente la faim de 5 
									position = animal.position
	# on cherche la case d'herbe la plus proche
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir()
				else:
					nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k])]
					for k in nourriture_distance:
						nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
					traque = AStar(mappy,position,nourriture_proche)
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir()
				animal.deplacer(nourriture_proche)		
				animal.manger(5) # on augmente la faim de 5 
				position = animal.position
				
				
## Terminé			
class Herbivore_soif(Etat):
	def action(self,animal):
		case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = animal.position
	# position est un tuple (i,j)
		eau_trouve = animal.detecter_eau
	# eau_trouve = False si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage	
		if eau_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Herbivore se déplace aléatoirement sur une distance de "vitesse" case
			for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
				for k in range(len(deplacement_proximité)):
					if deplacement_proximite[i] not in case_disponible:
						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
				animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
				position = animal.position
				case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
				if animal.detecter_eau != False:
	# Herbivore se dirige vers la case d'eau : Pathfinder
					position_eau = animal.detecter_eau
					while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
						traque = AStar(mappy,position,position_eau)
					animal.boire(100) # on remplit la barre de soif
					position = animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
			if animal.soif == 0:
				self.MAP.suppression(position)
				animal.mourir() 
		else :
	# Herbivore se dirige vers la case d'eau : Pathfinder
			position_eau = animal.detecter_eau
			while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
				traque = AStar(mappy,position,position_eau)
			animal.boire(100) # on remplit la barre de soif
			position = animal.position

## Terminé
class Herbivore_faim_soif(Etat):
	def action(self,animal):
		case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles
		position = animal.position
	# position est un tuple (i,j)
		eau_trouve = animal.detecter_eau
	# eau_trouve = False si aucune case d'eau n'est détectée
	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
	# On compare les paramètre faim et soif pour savoir à qui donner la priorité ; Si égalité, on donne la priorité à la soif
		if animal.faim < animal.soif :
			case_disponible = animal.deplacements_possibles()
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
			position = animal.position
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
					for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
						for k in range(len(deplacement_proximité)):
							if deplacement_proximite[k] not in case_disponible:
								deplacement_proximite.remove(deplacement_proximite[k])
	# On deplace l'animal
								animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
								position = animal.position
								case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
						for k in case_disponible:
							if mappy[case_disponible[k]][0] == 1:
								nourriture = nourriture + case_disponible[k]
								if len(nourriture) != 0:
	# on cherche la case d'herbe la plus proche
									nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k])]
									for k in nourriture_distance:
										nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
									traque = AStar(mappy,position,nourriture_proche)
									if animal.faim == 0:
										self.MAP.suppression(position)
										animal.mourir()
									animal.deplacer(nourriture_proche)		
									animal.manger(5) # on augmente la faim de 5 
									position = animal.position
	# on cherche la case d'herbe la plus proche
	# si la faim arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir()
				else:
					nourriture_distance = nourriture_distance+[self.MAP.distance(position,nourriture[k])]
					for k in nourriture_distance:
						nourriture_proche = min(nourriture_distance[k])
	# nourriture_proche est la case d'herbe la plus proche
					traque = AStar(mappy,position,nourriture_proche)
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir()
				animal.deplacer(nourriture_proche)		
				animal.manger(5) # on augmente la faim de 5 
				position = animal.position
		else:
			if eau_trouve == False:
	# Se deplacer aléatoirement
	# case_disponible est une liste des cases disponibles dans la vision de l'animal
				deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
	# On supprime tout les cases de proximité indisponible
	# Herbivore se déplace aléatoirement sur une distance de "vitesse" case
				for k in range(animal.vitesse):
	# On cherche toutes les cases disponibles à proximité	
					for k in range(len(deplacement_proximité)):
						if deplacement_proximite[i] not in case_disponible:
							deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
					animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))])
					position = animal.position
					case_disponible = animal.deplacements_possibles()
	# position est un tuple (i,j)
					if animal.detecter_eau != False:
	# Herbivore se dirige vers la case d'eau : Pathfinder
						position_eau = animal.detecter_eau
						while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
							traque = AStar(mappy,position,position_eau)
							if animal.faim == 0:
								self.MAP.suppression(position)
								animal.mourir() 
							if animal.soif == 0:
								self.MAP.suppression(position)
								animal.mourir()
						animal.boire(100) # on remplit la barre de soif
						position = animal.position
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
				if animal.soif == 0:
					self.MAP.suppression(position)
					animal.mourir() 
				if animal.faim == 0:
					self.MAP.suppression(position)
					animal.mourir()
			else :
	# Herbivore se dirige vers la case d'eau : Pathfinder
				position_eau = animal.detecter_eau
				while position != position_eau: # tant que le Herbivore n'est pas sur l'eau
					traque = AStar(mappy,position,position_eau)
					if animal.faim == 0:
						self.MAP.suppression(position)
						animal.mourir() 
					if animal.soif == 0:
						self.MAP.suppression(position)
						animal.mourir()
				animal.boire(100) # on remplit la barre de soif
				position = animal.position
"""




## Autre
#
# Meute = problème il faudrait que toute la meute BOIVENT en même temps et MANGE en même temps
#

#class Meute_normal(Etat):
#	def action(self,animal):
#		if animal.a_faim == True and animal.a_soif == False:
#			animal.changer_etat(Meute_faim)
#		elif animal.a_faim == False and animal.a_soif == True:
#			animal.changer_etat(Meute_soif)
#		elif animal.a_faim == False and animal.a_soif == False:
#			animal.changer_etat(Meute_faim_soif)

#
# Inclure un truc pour que les meute reste entre eux et se cherche
#
			
#class Meute_soif(Etat):
#		def action(self,animal):
#		case_disponible = animal.deplacements_possibles()
#	# case_disponible est une liste des cases disponibles
#		position = animal.position
#	# position est un tuple (i,j)
#		eau_trouve = animal.detecter_eau
#	# eau_trouve = False si aucune case d'eau n'est détectée
#	# eau_trouve = (i,j) si une case d'eau est trouvée dans le voisinage
#		if eau_trouve == False:
#	# Se deplacer aléatoirement
#	# case_disponible est une liste des cases disponibles dans la vision de l'animal
#			deplacement_proximite = [(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]+1),(position[0],position[1]-1),(position[0]+1,position[1]+1), (position[0]+1,position[1]-1),(position[0]-1,position[1]-1), (position[0]-1,position[1]+1)]
#	# On supprime tout les cases de proximité indisponible
#	# Meute se déplace aléatoirement sur une distance de "vitesse" case
#			for k in range animal.vitesse:
#	# On cherche toutes les cases disponibles à proximité	
#				for k in range len(deplacement_proximité):
#					if deplacement_proximite[i] is not in case_disponible:
#						deplacement_proximite.remove(deplacement_proximite[i])
	# On deplace l'animal
#				animal.deplacer(deplacement_proximite[random.randint(0,len(deplacement_proximite))]
#				position = animal.position
	# position est un tuple (i,j)
	# si la soif arrive à 0, on fait mourir l'animal : suppression de MAP, suppression de LIVING
#			if animal.soif == 0:
#				self.MAP.suppression(position)
#				animal.mourir() 
#			if animal.detecter_eau != False:
#	# Meute se dirige vers la case d'eau : Pathfinder
#				position_eau = animal.detecter_eau
#				while position != position_eau: # tant que le Meute n'est pas sur l'eau
#					traque = AStar(mappy,position,position_eau)
#				animal.boire(100) # on remplit la barre de soif
#				position = animal.position
#		else :
	# Meute se dirige vers la case d'eau : Pathfinder
#			position_eau = animal.detecter_eau
#			while position != position_eau: # tant que le Meute n'est pas sur l'eau
#				traque = AStar(mappy,position,position_eau)
#			animal.boire(100) # on remplit la barre de soif
#			position = animal.position