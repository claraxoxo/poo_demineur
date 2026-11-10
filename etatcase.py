from enum import Enum

class EtatCase(Enum):
    """ Représente les différents états possibles d'une case de la grille.

    Attributes:
        cachee (str): case pas encore découverte
        devoilee (str): case découverte
        marquee (str): case marquée comme potentiellement minée
    """
    cachee = 'cachee'
    devoilee = 'devoilee'
    marquee = 'marquee'