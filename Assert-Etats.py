# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/xababafr/Documents/Projet-Informatique')
import numpy as np
from Animal import *
from Map import *
from AStar import *
from Etat import *

mappy2 = [
    [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]],
    [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]],
    [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]],
    [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()]],
    [[0,Rien()],[0,Rien()],[0,Rien()],[0,Rien()],[1,Rien()],[0,Rien()]],
    [[0,Rien()],[0,Rien()],[1,Rien()],[1,Rien()],[1,Rien()],[0,Rien()]]
]

class Ecosysteme:
    def __init__(self,MAP,LIVING,CORPSES):
        self.MAP = np.array(mappy2)
        self.LIVING = []
        self.CORPSES = []
        