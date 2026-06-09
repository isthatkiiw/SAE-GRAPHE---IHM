# Represente un motif de la grille, compose de plusieurs cases
class Motif:

    def __init__(self):
        self.cases = []  # liste des cases qui forment ce motif

    def taille(self):
        # renvoie N, le nombre de cases dans le motif
        return len(self.cases)