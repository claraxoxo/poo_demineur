import numpy as np
from case import CaseMinee, CaseNumerotee, CaseVide
from etatcase import EtatCase


class Grille():

    def __init__(self, size, nb_mines_initiales):
        """ Initialisation de la grille, placement des mines, des cases numérotées et vides.

        Args:
            size (int[2]): nb lignes et colonnes de la grille
            nb_mines_initiales (int): nb mines au début de la partie
        """

        # initialisation grille vide
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
                
                # si la case parcourue est une mine, on passe à la case suivante
                if [a,b] in coord_mine:
                    continue

                # sinon, on récupère les coord de toutes ses cases voisines
                liste_voisins = self.get_voisins(a, b)

                # initialisation compteur de mines sur les cases voisines 
                compte_mines = 0
                for couple in liste_voisins:
                    if couple in coord_mine:
                        compte_mines +=1

                # si aucune mine dans les cases voisines, c'est une case vide
                if compte_mines == 0 :
                    self.cases[a, b] = CaseVide(EtatCase.cachee, a, b)
                # sinon, c'est une case numérotée
                else:
                    self.cases[a, b] = CaseNumerotee(EtatCase.cachee, a, b, compte_mines)

    def __str__(self):
        """ Affiche la grille du démineur avec des symboles différents en fonction de la case et de son état.

            str: retourne le string représentant la grille
        """

        strings = []
        
        # boucle sur les lignes
        for x in range(self.l):
            
            # création string vide pour une ligne
            string = " "

            # boucle sur les colonnes
            for y in range(self.c):

                case = self.cases[x,y]

                # ajout d'un symbole en fonction de la case et de son état
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
            
            # ajout barre dernière colonne
            string += "|"       
            
            # ajout du string de la ligne au string de la grille
            strings.append(string)
        
        # joint toutes les strings de ligne avec un retour à la ligne entre chaque
        return "\n".join(strings)
    
    def get_voisins(self, a, b):
        """ Calcule les coord des 8 voisins d'une case.

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
        """ Dévoile toutes les cases voisines d'une case vide, si ce sont des cases numérotées ou vides.

        Args:
            case (Case): case dont on veut dévoiler les voisins
        """

        coord_voisins_case_vide = self.get_voisins(case.l, case.c)

        # pour chaque coord de case voisine
        for coord in coord_voisins_case_vide:

            x,y = coord[0], coord[1]
            # récupère l'objet Case de la case voisine
            case_voisine = self.trouver_case(x,y)[0]

            # si la case voisine est déjà dévoilée, on ne fait rien, on passe à la case suivante
            if case_voisine.etat == EtatCase.devoilee:
                continue

            # si la case voisine est marquée, on ne fait rien, on passe à la case suivante
            elif case_voisine.etat == EtatCase.marquee:
                continue

            # si la case voisine est cachée
            elif case_voisine.etat == EtatCase.cachee:
                
                # si elle est minée, on ne le dévoile pas, on passe à la case suivante
                if isinstance(case_voisine, CaseMinee):
                    continue 
                
                # si elle est numérotée, on la dévoile
                elif isinstance(case_voisine, CaseNumerotee):
                    case_voisine.changer_etat(EtatCase.devoilee)
                
                # si elle est vide, on la dévoile et on rappelle la méthode sur cette nouvelle case vide dévoilée
                elif isinstance(case_voisine, CaseVide):
                    case_voisine.changer_etat(EtatCase.devoilee)
                    self.devoiler_voisins(case_voisine)

    def trouver_case(self, l, c):
        """ Retourne la case correspondant à la ligne l et colonne c.

        Args:
            l (int): num de ligne de la case
            c (int): num de colonne de la case

        Returns:
            tuple(Case, bool): renvoie un objet Case et un True si la case est bien trouvée, renvoie
            un 0 et un False si la case n'a pas été trouvée
        """
        if (0<=l<self.l) and (0<=c<self.c):
            return self.cases[l,c], True
        else:
            print("Coordonnées de cases invalides. Refaites votre demande.")
            return 0, False

    def marquer_case(self, case):
        """ Marque la case.

        Args:
            case (Case): case à marquer

        Returns:
            bool: True si marquage réussi, False sinon
        """
        marquage_reussi = case.marquer()

        return marquage_reussi

    def decouvrir_case(self, case):
        """ Découvre une case.

        Args:
            case (Case): case à découvrir

        Returns:
            tuple(bool): decouverte_réussie (True si découverte réussie, False sinon) et 
            etat_partie (True si pas de mine découverte), False si partie perdue 
            à cause de mine découverte)
        """
        
        decouverte_reussie, etat_partie = case.decouvrir()

        if isinstance(case, CaseVide) and decouverte_reussie:
            self.devoiler_voisins(case)
        
        return decouverte_reussie, etat_partie

    def demarquer_case(self, case):
        """ Enlève la marque d'une case.

        Args:
            case (Case): case dont on veut enlever la marque

        Returns:
            bool: True si démarquage réussi, False sinon
        """

        demarquage_reussi = case.demarquer()
        
        return demarquage_reussi
    
    def verifier_victoire(self):
        """ Vérifie si la partie est gagnée. 
        2 conditions à vérifier pour savoir si la partie est gagnée :
            - si toutes les mines ont été marquées,
            - si toutes les cases vides et numérotées ont été découvertes
        Partie gagnée si l'une ou l'autre de ces conditions a été remplie.

        Returns:
            bool: True si partie gagnée, False sinon
        """

        cases_minees_marquees = True
        cases_autres_devoilees = True

        # parcours de la grille
        for a in range(self.l):
            for b in range(self.c):

                case = self.trouver_case(a,b)[0]

                # si au moins une des mines n'est pas marquée, partie pas encore gagnée
                if isinstance(case, CaseMinee) and case.etat != EtatCase.marquee:
                    cases_minees_marquees = False
                
                # si au moins une des cases numérotées ou vides pas découvertes, partie pas encore gagnée
                elif not isinstance(case, CaseMinee) and case.etat != EtatCase.devoilee:
                    cases_autres_devoilees = False

        condition = cases_autres_devoilees or cases_minees_marquees

        return condition 



            


