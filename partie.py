import numpy as np
from grille import Grille

class Partie():

    def __init__(self, mines_restantes):
        # niveau de difficulté diff : choisir nb mine et taille grille
        self.nb_mines_initiales = 4
        self.nb_mines_restantes = mines_restantes
        self.taille_grille = [10,10]

    def jouer(self):
        # demander le niveau de difficulté (input)
        self.grille = Grille(self.taille_grille)

    def marquer_case(self, l, c):
        
        case = self.grille.trouver_case(l,c)
        reussite_marquage = self.grille.marquer_case(case)

        if reussite_marquage:
            self.nb_mines_restantes -=1

    def decouvrir_case(self, l, c):
        
        case = self.grille.trouver_case(l,c)
        self.grille.decouvrir_case(case)
        


