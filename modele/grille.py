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

    def charger(self, chemin_json):
        import json

        with open(chemin_json, "r") as f:
            donnees = json.load(f)

        # trouver les dimensions de la grille a partir des cases du JSON
        toutes_les_cases = []
        for cases_motif in donnees.values():
            toutes_les_cases.extend(cases_motif)

        self.nb_lignes = max(c[0] for c in toutes_les_cases) + 1
        self.nb_colonnes = max(c[1] for c in toutes_les_cases) + 1

        # creer le tableau 2D vide
        self.cases = []
        for l in range(self.nb_lignes):
            ligne = []
            for c in range(self.nb_colonnes):
                ligne.append(Case(l, c))
            self.cases.append(ligne)

        # remplir les cases et construire les motifs
        self.motifs = []
        for cases_motif in donnees.values():
            motif = Motif()
            for (l, c, valeur) in cases_motif:
                # si la valeur est non nulle, la case est fixe (donnee au depart)
                fixe = valeur != 0
                case = Case(l, c, valeur, fixe)
                self.cases[l][c] = case
                motif.cases.append(case)
            self.motifs.append(motif)
