import heapq
import numpy as np

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

		# ontravaillera toujours avec une grille carree
		self.dim = n
		
		##NON, VOIR EN DESSOUS
		#self.start = Cell(start[0],start[1],False)
		#self.end = Cell(end[0],end[1],False)

		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 1)
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
		return path

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

