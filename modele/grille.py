from modele.case import Case
from modele.motif import Motif

# Represente la grille de jeu complete
class Grille:

    def __init__(self):
        self.nb_lignes = 0
        self.nb_colonnes = 0
        # tableau 2D de Cases, accessible via self.cases[ligne][colonne]
        self.cases = []
        # liste de tous les motifs de la grille
        self.motifs = []