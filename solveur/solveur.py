# Solveur de grille Neonaure par backtracking
class Solveur:

    def resoudre(self, grille):
        # parcourir toutes les cases pour trouver la premiere case vide
        for l in range(grille.nb_lignes):
            for c in range(grille.nb_colonnes):
                case = grille.cases[l][c]
                if case.valeur == 0:
                    # trouver le motif de cette case pour connaitre les valeurs possibles
                    motif = None
                    for m in grille.motifs:
                        if case in m.cases:
                            motif = m
                            break
                    # essayer chaque valeur de 1 a la taille du motif
                    for valeur in range(1, motif.taille() + 1):
                        if grille.placement_valide(l, c, valeur):
                            case.valeur = valeur
                            if self.resoudre(grille):
                                return True
                            # echec : on annule et on essaie la valeur suivante
                            case.valeur = 0
                    # aucune valeur ne fonctionne : on remonte
                    return False
        # aucune case vide : la grille est resolue
        return True