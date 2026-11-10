from etatcase import EtatCase

class Case():
    """ Classe mère caractérisant tous les types de cases du démineur.
    """

    def __init__(self, state, ligne, colonne):
        """ Constructeur

        Args:
            state (EtatCase): élément de l'énumération EtatCase (dévoilée, marquée ou cachée)
            ligne (int): numéro de la ligne de la case
            colonne (int): numéro de la colonne de la case
        """
        self.etat = state
        self.l = ligne
        self.c = colonne

    def changer_etat(self, e):
        """ Change l'état d'une case.

        Args:
            e (EtatCase): état d'une case, compris dans l'énumération de EtatCase
        """

        self.etat = e

    def marquer(self):
        """ Marque une case.

        Returns:
            bool: si le marquage est réalisé ou non
        """

        if self.etat == EtatCase.marquee:
            print('Cette case est déjà marquée. \n Faites une autre action.')
            return False

        elif self.etat == EtatCase.devoilee:
            print('Cette case est déjà dévoilée, vous ne pouvez pas la marquer. \n Faites une autre action.')
            return False
        
        else:
            self.changer_etat(EtatCase.marquee)
            return True

    def decouvrir(self):
        """ Découvre une case.

        Returns:
            tuple(bool): renvoie 2 booléens, decouverte_reussie (True si la découverte a marché, False sinon) et etat_partie (True si partie pas perdue, 
            False sinon => découverte de bombe)
        """

        etat_partie = True

        if self.etat == EtatCase.marquee:
            print('Cette case est déjà marquée. \n Faites une autre action.')
            decouverte_reussie = False
            return decouverte_reussie, etat_partie

        elif self.etat == EtatCase.devoilee:
            print('Cette case est déjà dévoilée. \n Faites une autre action.')
            decouverte_reussie = False
            return decouverte_reussie, etat_partie
        
        else:
            self.changer_etat(EtatCase.devoilee)
            decouverte_reussie = True
            return decouverte_reussie, etat_partie
        
    def demarquer(self):
        """ Enlève la marque d'une case préalablement marquée.

        Returns:
            bool: renvoie 1 booléen (True si le démarquage a réussi et False sinon)
        """

        if self.etat == EtatCase.marquee:
            self.changer_etat(EtatCase.cachee)
            return True
        
        elif self.etat == EtatCase.devoilee:
            print('Cette case est déjà dévoilée, vous ne pouvez pas la démarquer. \n ' \
            'Faites une autre action.')
            return False
        
        else:
            print("Cette case n'est pas marquée, vous ne pouvez pas la démarquer. \n " \
            'Faites une autre action.')
            return False

class CaseMinee(Case):
    """ Classe de la case minée, classe fille de la classe Case.

    Args:
        Case (class): classe mère Case
    """
    
    def decouvrir(self):
        """ Découvre une case minée.

        Returns:
            tuple(bool): renvoie 2 booléens, decouverte_reussie (True si la découverte a marché, False sinon) et etat_partie (True si partie pas perdue, 
            False sinon => découverte de bombe)
        """
        
        decouverte_reussie, etat_partie = super().decouvrir()

        if decouverte_reussie:
            print("Vous avez découvert une bombe !!!! C'est fini....")
            etat_partie = False
        
        return decouverte_reussie, etat_partie 

class CaseNumerotee(Case):
    """ Classe de la case numérotée, classe fille de la classe Case.

    Args:
        Case (class): classe mère Case
    """
    
    def __init__(self, state, ligne, colonne, numero):
        """ Constructeur

        Args:
            state (EtatCase): élément de l'énumération EtatCase (dévoilée, marquée ou cachée)
            ligne (int): numéro de la ligne de la case
            colonne (int): numéro de la colonne de la case
            numero (int): nombre de mines dans les cases limitrophes (cases en diagonales comptent)
        """
        super().__init__(state, ligne, colonne)
        self.num = numero

class CaseVide(Case):
    """ Classe de la case vide, classe fille de la classe Case.

    Args:
        Case (class): classe mère Case
    """
    
    pass

