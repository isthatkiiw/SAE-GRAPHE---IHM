from modele.grille import Grille

# chargement de la grille depuis le fichier JSON
grille = Grille()
grille.charger("Grille/grille1.json")

print(f"Grille {grille.nb_lignes}x{grille.nb_colonnes}")
print()

# affichage de la grille ligne par ligne
for l in range(grille.nb_lignes):
    ligne = ""
    for c in range(grille.nb_colonnes):
        valeur = grille.cases[l][c].valeur
        if valeur == 0:
            ligne += ". "
        else:
            ligne += str(valeur) + " "
    print(ligne)

print()

# affichage des motifs
for i, motif in enumerate(grille.motifs):
    print(f"Motif {i + 1} (taille {motif.taille()}) :", end=" ")
    for case in motif.cases:
        print(f"({case.ligne},{case.colonne})={case.valeur}", end=" ")
    print()