# -*- coding: utf-8 -*-

import heapq
import numpy as np
import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
from Animal import *


## le pathfinding ne marche pas deux fois d'affilees :
# il faut creer un nouvel objet a chaque fois

class Cell():
	def __init__(self, x, y, obstacle):
		self.x = x
		self.y = y
		self.obstacle = obstacle
		self.parent = None
		self.G = 0
		self.H = 0
		self.F = 0


	def __gt__(self,cell):
		return self.F > cell.F

class AStar():
	def __init__(self,MAP,start,end):
		self.L_ouverte = []
		# on cree une file de priorite
		heapq.heapify(self.L_ouverte)

		# on utilise un set() pour eviter d'avoir a gerer les repetitions
		self.L_fermee = set()

		# la liste des differentes cellules, qui sont ou non des obstacles ( = de l'eau)
		# j'ecris du code qui transforme la map en une liste de cells correspondant
		self.cells = []
		n = len(MAP)

		# on travaillera toujours avec une grille carree
		self.dim = n
		
		self.init_cells(n,MAP,start,end)
		
		##NON, VOIR EN DESSOUS
		#self.start = Cell(start[0],start[1],False)
		#self.end = Cell(end[0],end[1],False)
		"""
		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 3)
				self.cells.append(Cell(x,y,value))
				
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])
		"""

	def init_cells(self,n,MAP,start,end):
		
		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 3)
				self.cells.append(Cell(x,y,value))
				
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])

	def get_cell(self,x,y):
		return self.cells[x * self.dim + y]

	def heuristique(self,cell):
		return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

	def get_voisins(self,cell):
		voisins = []
		if cell.x < self.dim-1:
			voisins.append(self.get_cell(cell.x+1, cell.y))
		if cell.y > 0:
			voisins.append(self.get_cell(cell.x, cell.y-1))
		if cell.x > 0:
			voisins.append(self.get_cell(cell.x-1, cell.y))
		if cell.y < self.dim-1:
			voisins.append(self.get_cell(cell.x, cell.y+1))
		return voisins

	def get_path(self):
		cell = self.end
		path = []
		path.append((cell.x,cell.y))
		while cell.parent is not self.start:
			cell = cell.parent
			path.append((cell.x,cell.y))
		return (path[::-1])

	def set_voisin(self, parent, voisin):
		# on appelle cette fonction pour calculer les g, h et f d'une cellule, en connaissant sa cellule parente
		voisin.G = parent.G + 10
		voisin.H = self.heuristique(voisin)
		voisin.F = voisin.G + voisin.H
		voisin.parent = parent


	def find_path(self):
		heapq.heappush(self.L_ouverte, (self.start.F, self.start))
		while len(self.L_ouverte):
			F,cell = heapq.heappop(self.L_ouverte)
			self.L_fermee.add(cell) #on l'ajoute si elle est pas deja dedans (d'ou l'utilisation d'un set())

			#si on est arrive au bout
			if cell is self.end:
				return self.get_path()

			voisins = self.get_voisins(cell)
			for voisin in voisins:
				if (not voisin.obstacle) and not(voisin in self.L_fermee):
					if (voisin.F, voisin) in self.L_ouverte:
						# si la cellule voisine est egalement dans la liste ouverte
						# on regarde si le chemin est plus interessant en passant par la cellule actuelle
						if voisin.G > cell.G + 10:
							self.set_voisin(cell,voisin)
					else: #cas classique
						self.set_voisin(cell,voisin)
						
						## le probleme est peut etre avec cettte implementation des files prioritaires
						
						heapq.heappush(self.L_ouverte, (voisin.F, voisin))
		return False


class PathFinderH(AStar):
	
	#def __init__(self,MAP,start,end):
		#super.__init__(MAP,start,end)
	
	# le pathfinder de l'herbivore considère tous les autres animaux comme des barrières
	# car s'il marche sur leur cases, il les suppriment
	def init_cells(self,n,MAP,start,end):
		
		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 3 or isinstance(MAP[x,y][1],Animal))
				self.cells.append(Cell(x,y,value))
				
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])

class PathFinderS(AStar):
	
	#def __init__(self,MAP,start,end):
		#super.__init__(MAP,start,end)
	
	# le pathfinder du solitaire considère les autres solitaires comme des barrières
	# car s'il marche sur leur cases, il les suppriment
	def init_cells(self,n,MAP,start,end):
		
		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 3 or isinstance(MAP[x,y][1],Solitaire and Mort))
				self.cells.append(Cell(x,y,value))
				
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])
		
class PathFinderC(AStar):
	
	#def __init__(self,MAP,start,end):
		#super.__init__(MAP,start,end)
	
	# le pathfinder du charognard considère les autres animaux comme des barrières
	# car s'il marche sur leur cases, il les suppriment
	def init_cells(self,n,MAP,start,end):
		
		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 3 or isinstance(MAP[x,y][1],Solitaire and Herbivore and Charognard))
				self.cells.append(Cell(x,y,value))
				
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])


if __name__ == "__main__":
		
	class Rien():
		def __init__(self):
			pass
		

	mappy = np.array([
		[[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[3,Rien()]],
		[[3,Rien()],[3,Rien()],[0,Rien()],[1,Rien()],[0,Rien()],[3,Rien()]],
		[[0,Rien()],[0,Rien()],[0,Rien()],[3,Rien()],[0,Rien()],[0,Rien()]], 
		[[0,Rien()],[3,Rien()],[3,Rien()],[0,Rien()],[1,Rien()],[3,Rien()]],
		[[0,Rien()],[3,Rien()],[0,Rien()],[0,Rien()],[3,Rien()],[0,Rien()]],
		[[0,Rien()],[3,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()]]
	])
	
	start,end = (0,0) , (5,5)
	
	pathfinder = AStar(mappy,start,end)
	path = pathfinder.find_path()
	
	def check_path(path):
		for t in path:
			if (mappy[t[0],t[1]][0] == 3):
				return False
		return True
		
	assert check_path(path), "Erreur : pathfinder"
	print("Ok : pathfinder")