import numpy as np
from abc import ABCMeta , abstractmethod

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
	        V = MAP.voisinnage(self.animal.position,self.animal.vision)
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

	        	MAP.deplacer_animal((x,y),destination)





