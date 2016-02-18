import heapq

mappy2 = [
	[[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
	[[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
	[[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
	[[0,None],[0,None],[0,None],[0,None],[0,None],[0,None]],
	[[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
	[[0,None],[0,None],[1,None],[1,None],[1,None],[0,None]]
]

class Cell():
	def __init__(self, x, y, obstacle):
		self.x = x
		self.y = y
		self.obstacle = obstacle
		self.parent = None
		self.G = 0
		self.H = 0
		self.F = 0
		
	## en copiant/collant directement le code du mec
	## son code marche pas non plus en 3.*
	## mais en 2.7, si, donc visiblement, python ne sait plus comparer deux tuples
	## par rapport aleur premier element en 3.*, donc il faut lui expliquer avec __gt__
	## ici, c'est pourtant ce que j'ai fait, donc il doit aussi y avoir unprobleme avec
	## ma traduction du probleme a notre configuration
	## mais le sien marche apres ma modification!! (pas tt a fait pareil mais meme veracite il me semble)

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
		self.start = Cell(start[0],start[1],False)
		self.end = Cell(end[0],end[1],False)

		for x in range(n):
			for y in range(n):
				value = (MAP[x,y][0] == 1)
				self.cells.append(Cell(x,y,value))

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
		while cell.parent != self.start or cell.parent != None or cell != None:
			path.append((cell.x,cell.y))
			cell = cell.parent

	def set_voisin(self, parent, voisin):
		# on appelle cette fonction pour calculer les g, h et f d'une cellule, en connaissant sa cellule parente
		voisin.G = parent.G + 10
		voisin.H = self.heuristique(voisin)
		voisin.F = voisin.G + voisin.H
		voisin.parent = parent


	def find_patch(self):
		heapq.heappush(self.L_ouverte, (self.start.F, self.start))
		while len(self.L_ouverte):
			F,cell = heapq.heappop(self.L_ouverte)
			print('Cell : '+str((cell.x,cell.y))+', F : '+str(F))
			self.L_fermee.add(cell) #on l'ajoute si elle est pas deja dedans (d'ou l'utilisation d'un set())

			#si on est arrive au bout
			if cell is self.end:
				print('OK!')
				return True

			voisins = self.get_voisins(cell)
			for voisin in voisins:
				t = '    Voisin : '+str((voisin.x,voisin.y))+'   '
				if (not voisin.obstacle) and not(voisin in self.L_fermee):
					t += 'cond1   '
					if (voisin.F, voisin) in self.L_ouverte:
						t += 'cond2   '
						# si la cellule voisine est egalement dans la liste ouverte
						# on regarde si le chemin est plus interessant en passant par la cellule actuelle
						if voisin.G > cell.G + 10:
							t += 'cond 3   '
							self.set_voisin(cell,voisin)
					else: #cas classique
						t += 'cond4   '
						self.set_voisin(cell,voisin)
						
						## le probleme est peut etre avec cettte implementation des files prioritaires
						
						heapq.heappush(self.L_ouverte, (voisin.F, voisin))
				print(t)
		return False

