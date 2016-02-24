## TEST

import heapq
import numpy as np

# True
# True
# True
# True
# True
# False
# False
# False
# True
# True
# True
# False
# True
# True
# True
# False
# True
# True
# True
# False
# False
# True
# True
# False
# True
# False
# True
# True
# False
# True
# True
# False
# True
# True
# True
# True

mappy = [
    [[0,None],[0,None],[0,None],[0,None],[0,None],[1,None]],
    [[1,None],[1,None],[0,None],[0,None],[0,None],[1,None]],
    [[0,None],[0,None],[0,None],[1,None],[0,None],[0,None]],
    [[0,None],[1,None],[1,None],[0,None],[0,None],[1,None]],
    [[0,None],[1,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[1,None],[0,None],[0,None],[0,None],[0,None]]
]

mappy2 = [
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[0,None],[0,None]],
    [[0,None],[0,None],[0,None],[0,None],[1,None],[0,None]],
    [[0,None],[0,None],[1,None],[1,None],[1,None],[0,None]]
]

class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __gt__(self,cell):
        return self.f > cell.f
        
class AStar(object):
    def __init__(self,MAP,start,end):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = len(MAP)
        self.grid_width = len(MAP)
        self.init_grid(MAP,start,end)
        
    def init_grid(self,MAP,start,end):
        n = len(MAP)
        for x in range(n):
            for y in range(n):
                self.cells.append(Cell(x,y,(MAP[x,y][0] != 1)))
                
        self.start = self.get_cell(start[0], start[1])
        self.end = self.get_cell(end[0], end[1])

        
    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.
    
        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
        
    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.
    
        @param cell get adjacent cells for this cell
        @returns adjacent cells list 
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells
        
    def get_cell(self, x, y):
        """
        Returns a cell from the cells list
    
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]
        
    def get_path(self):
        cell = self.end
        path = []
        path.append((cell.x,cell.y))
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x,cell.y))
        return path
            
            
    def update_cell(self, adj, cell):
        """
        Update adjacent cell
    
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
        
    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        ## marche en python 2.7
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))
                        ## test en python 3.*
                        #self.opened.append((adj_cell.f, adj_cell))
        return False