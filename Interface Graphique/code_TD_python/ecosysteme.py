from random import randint
import sys
import time

def sign(x):
    return int(x>0) - int(x<0)

class Insecte():
    xmax=100
    ymax=100
    def __init__(self, abscisse, ordonnee, capacite=10):
        self.x = abscisse
        self.y = ordonnee
        self._max = capacite
        self._etat = randint(capacite//2, capacite)

    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, abscisse):
        if abscisse>self.xmax:
            self.__x = self.xmax
        elif abscisse<0:
            self.__x = 0
        else:
            self.__x = abscisse

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, ordonnee):
        if ordonnee>self.ymax:
            self.__y = self.ymax
        elif ordonnee<0:
            self.__y = 0
        else:
            self.__y = ordonnee

    def __str__(self):
        return "%c : position (%i, %i) etat %i/%i"%(self.car(), self.x, self.y, self._etat, self._max)
    
    def car(self):
        return 'I'
    
    def manger(self):
        self._etat -= 1
        if abs(self.x)<=2 and abs(self.y)<=2:
            self._etat = self._max
            print("Je mange")
        if self._etat <= 0:
            print("Je meurs de faim")

    def bouger(self):
        self.x += randint(0, self.xmax//5)
        self.y += randint(0, self.ymax//5)

    def unTour(self):
        self.manger()
        self.bouger()


class Fourmi(Insecte):
    def __init__(self, abscisse, ordonnee):
        super().__init__(abscisse, ordonnee, 10)

    def bouger(self):
        if self._etat>=4:
            if randint(0,2):
                self.x += randint(0, self.xmax//3)
            else:
                self.y += randint(0, self.ymax//3)
        else:
            self.x -= self.xmax//10
            self.y -= self.ymax//10
        
    def car(self):
        return 'F'

class Cigale(Insecte):
    def __init__(self, abscisse, ordonnee):
        super().__init__(abscisse, ordonnee, 12)

    def bouger(self):
        action = randint(0,2)
        if action==1:
            print("Je danse.")
        elif action==2:
            print("Je chante.")
        elif self._etat>=4:
            if randint(0,2):
                self.x += randint(0, self.xmax//2)
            else:
                self.y += randint(0, self.ymax//2)
        else:
            self.x -= self.xmax//20
            self.y -= self.ymax//20

    def car(self):
        return 'C'

class Ecosysteme(list):
    def __init__(self, nbins,nbt,xmax,ymax):
        Insecte.xmax=xmax
        Insecte.ymax=ymax        
        for i in range(nbins):
            if randint(0, 1)==0:
                self.append(Fourmi(randint(0,xmax), randint(0, ymax)))
            else:
                self.append(Cigale(randint(0,xmax), randint(0,ymax)))
                
        self.nbtour =  nbt  
    
    def __str__(self):
        pos = {}
        for ins in self:
            pos[(ins.x, ins.y)]=ins.car()
        s = ""
        for j in range(Insecte.xmax, 0, -1):
            for i in range(0, Insecte.ymax):
                if (i, j) in pos:
                    s += pos[(i,j)]
                elif abs(i)<=2 and abs(j)<=2:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s
    
    def unTour(self):
        for ins in self:  # fonctionne car Ecosysteme descend de list
            ins.unTour()
            #print(ins)
       
    def simuler (self):
        for t in range(self.nbtour):
            print("### Tour %i ###"%(t))
            self.unTour()
            print(self)
            time.sleep(0.5)

if __name__ == "__main__":
    nbins = 50
    nbtour = 10
    ecosys = Ecosysteme(nbins,nbtour,100,100)
    print(ecosys)
    ecosys.simuler()
