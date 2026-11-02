import numpy as np

class Case():

    def __init__(self, state, ligne, colonne):
        self.etat = state
        self.l = ligne
        self.c = colonne


class CaseMinee(Case):
    pass

class CaseNumerotee(Case):
    
    def __init__(self, state, ligne, colonne, numero):
        super().__init__(state, ligne, colonne)
        self.num = numero

class CaseVide(Case):
    pass