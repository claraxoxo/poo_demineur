import numpy as np
from grille import Grille
from etatcase import EtatCase
from case import Case, CaseMinee, CaseNumerotee, CaseVide

class Partie():

    def __init__(self):

        self.nb_mines_initiales = None
        self.nb_mines_restantes = None
        self.taille_grille = None

    def lancer_jeu(self):

        rejouer = True

        while rejouer:
            self.jouer()
            rejouer = self.rejouer()

        print(" Goodbye ")

    def jouer(self):
        
        
        self.choisir_difficulte()
        self.grille = Grille(self.taille_grille, self.nb_mines_initiales)
        self.afficher_mines()

        question = '__________________________________________________________________ \n' \
        'Que voulez vous faire ? Au choix, vous pouvez : \n' \
        ' \n' \
        '- Découvrir une case => taper "découvrir x,y" \n' \
        '- Marquer une case => taper "marquer x,y" \n' \
        "- Retirer la marque d'une case => \"démarquer x,y\" \n" 
        ' \n ' \
        'avec x le numéro de ligne et y le numéro de colonne \n' \
        'ATTENTION la numérotation des lignes et colonnes commence par 0 \n' \
        ' \n ' \
        '__________________________________________________________________ \n'


        i = 1
        
        victoire = False
        etat_partie = True

        while not victoire and etat_partie: 
            print('__________________________________________________________________ ')
            print(f'Coup n°{i} ')
            print('\n')
            print(self.grille)
            print('\n')
            print(f'Nb de mines restantes à marquer : {self.nb_mines_restantes}')
            print('\n')
            
            reponse = input(question)

            fonction = reponse.split(" ")[0]
            if fonction not in ('marquer', 'découvrir', 'démarquer'):
                print('Réponse invalide. Réécrivez votre choix.')
                continue

            try:
                coord = reponse.split(" ")[1]
                x = int(coord.split(',')[0])
                y = int(coord.split(',')[1])

            except (IndexError, ValueError):
                print("Réponse invalide. Réécrivez votre choix.")
                continue

            if fonction == 'marquer':
                case_trouvee = self.marquer_case(x,y)
  
            elif fonction == 'découvrir':
                etat_partie, case_trouvee = self.decouvrir_case(x,y) 

            elif fonction == 'démarquer':
                case_trouvee = self.demarquer_case(x,y)

            if not case_trouvee:
                continue
 
            
            victoire = self.grille.verifier_victoire()
            i += 1

        if victoire:
            print('Bravo !!!!!! Vous avez gagné ')
        else:
            print('... Vous avez perdu...') 
        

        return None
    

    def choisir_difficulte(self):

        string = 'Il y a 3 niveaux de difficulté : \n' \
        '1) Facile : grille 8x8 cases, 10% de mines \n' \
        '2) Moyen : grille 10x10, 15% de mines \n' \
        '3) Difficile : grille 12x12, 20% de mines \n' \
        '______________________________________________________________________ \n' \
        'Choississez le niveau de difficulté en tapant son numéro : 1, 2 ou 3 \n' \
        '_______________________________________________________________________ \n'

        etat_reponse = False
        

        while not etat_reponse:

            reponse = input(string)

            try:
                niveau = int(reponse)

            except ValueError:
                print("Réponse invalide. Réécrivez votre choix. \n ________________________________________________")
                continue

            if niveau == 1:
                self.nb_mines_initiales = 6
                self.taille_grille = [8,8]
                etat_reponse = True

            elif niveau == 2:
                self.nb_mines_initiales = 15
                self.taille_grille = [10,10]
                etat_reponse = True
        
            elif niveau == 3:
                self.nb_mines_initiales = 29
                self.taille_grille = [12,12]
                etat_reponse = True

            else:
                print("Le numéro de difficulté est invalide. Réécrivez votre choix.")
                continue

        self.nb_mines_restantes = self.nb_mines_initiales

    def rejouer(self):

        reponse = input("Voulez-vous rejouer ? (oui/non) : ")

        while reponse not in ("oui", "non"):
            print("Réponse invalide.")
            reponse = input("Voulez-vous rejouer ? (oui/non) : ")

        return reponse == "oui"


    def marquer_case(self, l, c):
        
        case, case_trouvee = self.grille.trouver_case(l,c)
        if case_trouvee:
            reussite_marquage = self.grille.marquer_case(case)
            if reussite_marquage:
                self.nb_mines_restantes -= 1
            return True
        else:
            return False
        
    def demarquer_case(self, l, c):

        case, case_trouvee = self.grille.trouver_case(l,c)
        if case_trouvee:
            reussite_demarquage = self.grille.demarquer_case(case)
            if reussite_demarquage:
                self.nb_mines_restantes += 1
            return True
        else:
            return False



    def decouvrir_case(self, l, c):
        
        case, case_trouvee = self.grille.trouver_case(l,c)
        if case_trouvee:
            _, etat_partie = self.grille.decouvrir_case(case)
            return etat_partie, True
        else:
            return True, False
        
    def afficher_mines(self):

        for a in range(self.grille.l):
            for b in range(self.grille.c):

                if isinstance(self.grille.cases[a,b], CaseMinee):
                    print(f"Mine en ({a}, {b})")
        
    
        


