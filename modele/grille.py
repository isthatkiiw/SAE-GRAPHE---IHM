from modele.case import Case
from modele.motif import Motif
import json

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

        with open(chemin_json, "r") as f:
            donnees = json.load(f)

        # trouver les dimensions de la grille a partir des cases du JSON
        toutes_les_cases = []
        for cases_motif in donnees.values():
            toutes_les_cases.extend(cases_motif)

        # le JSON est au format [colonne, ligne, valeur]
        self.nb_lignes = max(c[1] for c in toutes_les_cases) + 1
        self.nb_colonnes = max(c[0] for c in toutes_les_cases) + 1

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
            for (col, lig, valeur) in cases_motif:
                # si la valeur est non nulle, la case est fixe (donnee au depart)
                fixe = valeur != 0
                case = Case(lig, col, valeur, fixe)
                self.cases[lig][col] = case
                motif.cases.append(case)
            self.motifs.append(motif)
    
    def voisins(self, case):
        # renvoie la liste des cases voisines
        resultat = []
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                l = case.ligne + dl
                c = case.colonne + dc
                # on ignore la case elle-meme et les cases hors de la grille
                if (dl != 0 or dc != 0) and (0 <= l < self.nb_lignes) and (0 <= c < self.nb_colonnes):
                    resultat.append(self.cases[l][c])
        return resultat
    
    def placement_valide(self, ligne, colonne, valeur):
        case = self.cases[ligne][colonne]

        # trouver le motif auquel appartient cette case
        motif_case = None
        for motif in self.motifs:
            if case in motif.cases:
                motif_case = motif
                break

        # la valeur doit etre entre 1 et la taille du motif
        if valeur < 1 or valeur > motif_case.taille():
            return False

        # la valeur ne doit pas deja etre presente dans le motif
        for c in motif_case.cases:
            if c != case and c.valeur == valeur:
                return False

        # la valeur ne doit pas etre identique a celle d'un voisin
        for voisin in self.voisins(case):
            if voisin.valeur == valeur:
                return False

        return True
    
    def sauvegarder(self, chemin_json):

        donnees = {}
        # reconstruire le meme format que le JSON d'origine
        for i, motif in enumerate(self.motifs):
            nom_motif = "motif" + str(i + 1)
            cases_motif = []
            for case in motif.cases:
                cases_motif.append([case.colonne, case.ligne, case.valeur])
            donnees[nom_motif] = cases_motif

        with open(chemin_json, "w") as f:
            json.dump(donnees, f)

    def est_resolue(self):
        # verifier que toutes les cases sont remplies et que toutes les regles sont respectees
        for l in range(self.nb_lignes):
            for c in range(self.nb_colonnes):
                case = self.cases[l][c]
                # une case vide = pas resolue
                if case.valeur == 0:
                    return False
                # la valeur posee doit etre valide
                if not self.placement_valide(l, c, case.valeur):
                    return False
        return True
