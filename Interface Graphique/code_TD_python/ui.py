# -*- coding: utf-8 -*-
import sys
from ecosysteme import *
from PyQt4 import QtCore, QtGui, uic

class InsectesUI(QtGui.QMainWindow):
    def __init__(self, nb_tours, nb_ins, *args):
        self.nb_tours = nb_tours
        self.nb_ins = nb_ins
        
        # on appelle le constructeur de la super classe
        QtGui.QMainWindow.__init__(self, *args)
        
        # et on charge l'interface graphique
        self.ui = uic.loadUi('interface.ui', self)
        
        # pour l'instant on n'a pas d'écosystème
        self.ecosys = None
        self.un_generer()
        # on charge l'image de fond
        palette= QtGui.QPalette()
        pixmap = QtGui.QPixmap("arrierPlan.png")
        palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(pixmap))
        self.setPalette(palette)
        self.painter = QtGui.QPainter()
        
        
        self.ui.conteneur.paintEvent = self.mise_a_jour_ui
        
        self.ui.bouton_pas.clicked.connect(self.un_pas)
        self.ui.bouton_gen.clicked.connect(self.un_generer)
        self.ui.bouton_sim.clicked.connect(self.un_simuler)
        

            
    def un_pas(self):
        if  self.ecosys.nbtour > 0:
            self.ecosys.unTour()
            self.conteneur.update()
            self.ecosys.nbtour -=1
        else:
            QtGui.QMessageBox.question(self,'Attention !','Le nombre de tours est épuisé', QtGui.QMessageBox.Ok)
        print(self.ecosys)
            
    def un_generer(self):
        self.ecosys=Ecosysteme(self.nb_ins,self.nb_tours,self.ui.conteneur.width(),self.ui.conteneur.height())
        print(self.ecosys)
        pass
    
    def un_simuler(self):
        pass
    
    def mise_a_jour_ui(self, *args):
        self.painter.begin(self.conteneur)
        qp = self.painter      
        for ins in self.ecosys:
            ##print(ins.__class__.__name__)
            img = QtGui.QImage(ins.__class__.__name__+".png")
            qp.drawImage(ins.x,ins.y,img)
        qp.end()
            #if ins.car() == 'F':
             #   qp.setPen(QtCore.Qt.red)
              #  qp.drawRect(ins.x,ins.y,10,10)  #x,y,largeur,hauteur
            #else :    
             #   qp.setPen(QtCore.Qt.green)
              #  qp.drawRect(ins.x,ins.y,10,10)
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = InsectesUI(3, 20)
    window.show()
    sys.exit(app.exec_())
    