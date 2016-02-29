import sys
sys.path.append(os.getcwd())
import numpy as np
from Animal import *
from Map import Map

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
        

## VARIABLES GLOBALES

global MAP
MAP = Map(np.array(mappy))