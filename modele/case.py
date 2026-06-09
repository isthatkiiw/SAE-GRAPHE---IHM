# Represente une seule case de la grille
class Case:

    def __init__(self, ligne, colonne, valeur=0, fixe=False):
        self.ligne = ligne      # numero de ligne (commence a 0)
        self.colonne = colonne  # numero de colonne (commence a 0)
        self.valeur = valeur    # chiffre dans la case (0 = vide)
        self.fixe = fixe        # True si le chiffre est donne au depart (non modifiable)
