# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
import numpy as np
from Animal import *
from Map import *

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
        

class Ecosysteme:
    def __init__(self,MAP,LIVING):
        self.MAP = MAP
        self.LIVING = LIVING
        

## VARIABLES GLOBALES

global MAP
MAP = Map(np.array(mappy))