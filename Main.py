import numpy as np

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

class Etat:
    def __init__(self,name):
        self.n = name
        
    def action(self):
        print(self.n)
        
from Map import Map

## VARIABLES GLOBALES

global MAP
MAP = Map(np.array(mappy))

from Animal import *