# -*- coding: utf-8 -*-
import sys
from ecosysteme import *
from PyQt4 import QtCore, QtGui, uic


class EcosysUI(QtGui.QMainWindow): #Est ce que 'QtGui.QMainWindow' désigne la fenêtre principal de l'interface graphique
    def __init__(self, nb_tours, nb_predateur, nb_charognard, nb_herbivore, *args): #A quoi sert le '*args' ???
        self.nb_tours = nb_tours
        self.nb_predateur = nb_predateur
        self.nb_charognard = nb_charognard
        self.nb_herbivore = nb_herbivore        
        
        # on appelle le constructeur de la super classe
        QtGui.QMainWindow.__init__(self, *args)
        
        # et on charge l'interface graphique
        self.ui = uic.loadUi('EcosysHIM.ui', self)
        
        # pour l'instant on n'a pas d'écosystème
        self.ecosysteme = None
        self.generer()
#         # on charge l'image de fond
#         palette= QtGui.QPalette()
#         pixmap = QtGui.QPixmap("arrierPlan.png")
#         palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(pixmap))
#         self.setPalette(palette)
#         self.painter = QtGui.QPainter()
     
        self.ui.conteneur.paintEvent = self.mise_a_jour_ui
        self.ui.bouton_tour.clicked.connect(self.tour)
        self.ui.bouton_generer.clicked.connect(self.generer)
        self.ui.bouton_simuler.clicked.connect(self.simuler)
         
    def tour(self):
        if  self.ecosysteme.nbtours > 0:
            self.ecosysteme.unTour()
            self.conteneur.update()
            self.ecosysteme.nbtours -=1
        else:
            QtGui.QMessageBox.question(self,'Attention !','Le nombre de tours est épuisé', QtGui.QMessageBox.Ok)
        print(self.ecosysteme)
     
    def generer(self):
        self.ecosyteme=Ecosysteme(self.nb_predateur, self.nb_charognard, self.nb_herbivore,self.nb_tours,self.ui.conteneur.width(),self.ui.conteneur.height())
        print(self.ecosysteme)
        pass 
    
    def simuler(self):
        pass    
    
    def mise_a_jour_ui(self, *args):
        self.painter.begin(self.conteneur)
        qp = self.painter      
        for i in range (0,mappy.shape[0]):
            for j in range (0,mappy.shape[1]):
#  Il faudra appeler les images herbe, eau, sol, roche
                if mappy[i][0] == 0:
                    img = QtGui.QImage('herbe.png')
                    qp.drawImage(i,j,img)
                if mappy[i][0] == 1:
                    img = QtGui.QImage('eau.png')
                    qp.drawImage(i,j,img)
                if mappy[i][0] == 2:
                    img = QtGui.QImage('sol.png')
                    qp.drawImage(i,j,img)
                if mappy[i][0] == 3:
                    img = QtGui.QImage('roche.png')
                    qp.drawImage(i,j,img)
        for k in self.LIVING:
            ##print(ins.__class__.__name__)
            img = QtGui.QImage(self.LIVING.__class__.__name__+".png")
            qp.drawImage(self.LIVING[k].x,self.LIVING[k].y,img)
        qp.end()
        