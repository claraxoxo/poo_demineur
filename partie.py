import numpy as np
from grille import Grille

class Partie():

    def __init__(self):
        # niveau de difficulté diff : choisir nb mine et taille grille
        self.nb_mines_initiales = 4
        self.nb_mines_restantes = 4
        self.taille_grille = [10,10]

    def jouer(self):
        # demander le niveau de difficulté (input)

        self.grille = Grille(self.taille_grille, self.nb_mines_initiales)
        print(self.grille)

        etat_partie = True
        question = 'Que voulez vous faire ? Au choix, vous pouvez : \n' \
        '- Découvrir une case (écrire "découvrir x,y) \n' \
        '- Marquer une case (écrire "marquer x,y) \n' \
        'avec x le numéro de ligne et y le numéro de colonne \n' \
        'ATTENTION la numérotation des lignes et colonnes commence par 0'

        while self.nb_mines_restantes != 0 and etat_partie: 
            reponse = input(question)
            fonction = reponse.split(" ")[0]
            coord = reponse.split(" ")[1]
            x = int(coord.split(',')[0])
            y = int(coord.split(',')[1])

            if fonction == 'marquer':
                self.marquer_case(x,y)
  
            elif fonction == 'découvrir':
                decouverte_reussie, etat_partie = self.decouvrir_case(x,y)

            

            else:
                print("Votre demande n'est pas valide, refaites-la.")
            


    def marquer_case(self, l, c):
        
        case, case_trouvee = self.grille.trouver_case(l,c)
        if case_trouvee:
            reussite_marquage = self.grille.marquer_case(case)
            if reussite_marquage:
                self.nb_mines_restantes -=1

    def decouvrir_case(self, l, c):
        
        case, case_trouvee = self.grille.trouver_case(l,c)
        if case_trouvee:
            decouverte_reussie, etat_partie = self.grille.decouvrir_case(case)
            return decouverte_reussie, etat_partie
        else:
            decouverte_reussie, etat_partie = False, True
        


