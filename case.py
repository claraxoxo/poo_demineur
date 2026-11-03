import numpy as np
from etatcase import EtatCase

class Case():

    def __init__(self, state, ligne, colonne):
        self.etat = state
        self.l = ligne
        self.c = colonne

    def marquer(self):
        """ Marque une case.

        Returns:
            bool: si le marquage est réalisé ou non
        """

        if self.etat == EtatCase.marquee:

            print('Cette case est déjà marquée. \n Faites une autre action.')
            return False

        elif self.etat == EtatCase.devoilee:
            print('Cette case est déjà dévoilée. \n Faites une autre action.')
            return False
        
        else:
            self.changer_etat(EtatCase.marquee)
            return True

    def changer_etat(self, e):
        """ Change l'état d'une case.

        Args:
            e (EtatCase): état d'une case, compris dans l'énumération de EtatCase
        """

        self.etat = e



class CaseMinee(Case):
    pass

class CaseNumerotee(Case):
    
    def __init__(self, state, ligne, colonne, numero):
        super().__init__(state, ligne, colonne)
        self.num = numero

class CaseVide(Case):
    pass