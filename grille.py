import numpy as np
from case import Case, CaseMinee, CaseNumerotee, CaseVide
from etatcase import EtatCase


class Grille():

    def __init__(self, size, nb_mines_initiales):
        """Initialise la grille, placement des mines et des cases numérotées et vides.

        Args:
            size (list[2]): nb lignes et colonnes de la grille
            nb_mines_initiales (int): nb mines au début de la partie
        """
        self.l = size[0]
        self.c = size[1]

        self.cases = np.empty((self.l, self.c), dtype=object)

        # placement des cases mines
        coord_mine = []
        mines_placees = 0
        while mines_placees < nb_mines_initiales:

            ligne, colonne = np.random.randint(0, self.l), np.random.randint(0, self.c)
            if [ligne, colonne] not in coord_mine:
                coord_mine.append([ligne, colonne])
                self.cases[ligne, colonne] = CaseMinee(EtatCase.cachee, ligne, colonne)
                mines_placees += 1

        # placement des cases restantes : numérotées ou vides
        for a in range(self.l):
            for b in range(self.c):
                
                if [a,b] in coord_mine:
                    continue
                liste_voisins = self.get_voisins(a, b)

                compte_mines = 0
                for couple in liste_voisins:
                    if couple in coord_mine:
                        compte_mines +=1

                if compte_mines == 0 :
                    self.cases[a, b] = CaseVide(EtatCase.cachee, a, b)
                else:
                    self.cases[a, b] = CaseNumerotee(EtatCase.cachee, a, b, compte_mines)

    def __str__(self):
        """ Affiche la grille du démineur avec des symboles différents en fonction de la case et de son état.

            str: retourne le string représentant la grille
        """

        strings = []
        for x in range(self.l):

            string = " "
            for y in range(self.c):

                case = self.cases[x,y]

                if case.etat == EtatCase.cachee:
                    string += '|O'
                
                elif case.etat == EtatCase.devoilee and isinstance(case, CaseMinee):
                    string += '|X'
                
                elif case.etat == EtatCase.devoilee and isinstance(case, CaseVide):
                    string += '| '

                elif case.etat == EtatCase.devoilee and isinstance(case, CaseNumerotee):
                    string += '|' + str(case.num)

                elif case.etat == EtatCase.marquee:
                    string += '|M'
            
            string += "|"       
            
            strings.append(string)
            
        return "\n".join(strings)

    
    def get_voisins(self, a, b):
        """Calcule les coord des 8 voisins d'une case.

        Args:
            a (int): num de la ligne
            b (int): num de la colonne

        Returns:
            list: liste des coord des voisin dont la taille peut varier entre 3 et 8 voisins
        """
        
        coord_voisins = [
            [a - 1, b - 1],
            [a - 1, b],
            [a - 1, b + 1],
            [a, b - 1],
            [a, b + 1],
            [a + 1, b - 1],
            [a + 1, b],
            [a + 1, b + 1]
        ]

        coord_valides = []
        for couple in coord_voisins :

            if (0 <= couple[0] < self.l) and (0 <= couple[1] < self.c):
                coord_valides.append(couple)

        return coord_valides
    
    def devoiler_voisins(self, case):

        coord_voisins_case_vide = self.get_voisins(case.l, case.c)
        for coord in coord_voisins_case_vide:

            x,y = coord[0], coord[1]
            case_voisine = self.trouver_case(x,y)

            if case_voisine.etat == EtatCase.devoilee:
                continue
            elif case_voisine.etat == EtatCase.marquee:
                continue
            elif case_voisine.etat == EtatCase.cachee:

                if isinstance(case_voisine, CaseMinee):
                    continue 

                elif isinstance(case_voisine, CaseNumerotee):
                    case_voisine.changer_etat(EtatCase.devoilee)
                
                elif isinstance(case_voisine, CaseVide):
                    case_voisine.changer_etat(EtatCase.devoilee)
                    self.devoiler_voisins(case_voisine)

        


    def trouver_case(self, l, c):
        """ Retourne la case correspondant à la ligne l et colonne c.

        Args:
            l (int): num de ligne de la case
            c (int): num de colonne de la case

        Returns:
            Case: case cherchée
        """
        if (0<=l<self.l) and (0<=c<self.c):
            return self.cases[l,c], True
        else:
            print("Coordonnées de cases invalides.")
            return 0, False

    def marquer_case(self, case):
        """ Marque la case.

        Args:
            case (Case): case à marquer
        """

        marquage_reussi = case.marquer()

        return marquage_reussi

    def decouvrir_case(self, case):
        
        decouverte_reussie, etat_partie = case.decouvrir()

        if isinstance(case, CaseVide) and decouverte_reussie:

            self.devoiler_voisins(case)
        
        return decouverte_reussie, etat_partie
            
            


