from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton

# Widget qui affiche la grille de jeu sous forme de boutons
class GrilleWidget(QWidget):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.boutons = []  # tableau 2D de boutons, un par case
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0)
        self.setLayout(self.layout_grille)

    def _trouver_motif(self, grille, l, c):
        # renvoie le motif auquel appartient la case (l, c)
        for motif in grille.motifs:
            if grille.cases[l][c] in motif.cases:
                return motif
        return None

    def _construire_bordures(self, grille, l, c):
        # trait epais (3px) si la case voisine est dans un autre motif ou si c'est le bord de la grille
        motif_actuel = self._trouver_motif(grille, l, c)

        if l == 0 or self._trouver_motif(grille, l - 1, c) != motif_actuel:
            haut = 3
        else:
            haut = 1

        if l == grille.nb_lignes - 1 or self._trouver_motif(grille, l + 1, c) != motif_actuel:
            bas = 3
        else:
            bas = 1

        if c == 0 or self._trouver_motif(grille, l, c - 1) != motif_actuel:
            gauche = 3
        else:
            gauche = 1

        if c == grille.nb_colonnes - 1 or self._trouver_motif(grille, l, c + 1) != motif_actuel:
            droite = 3
        else:
            droite = 1

        return (f"border-top: {haut}px solid black;"
                f"border-bottom: {bas}px solid black;"
                f"border-left: {gauche}px solid black;"
                f"border-right: {droite}px solid black;")

    def afficher_grille(self, grille):
        # supprimer les boutons de l'affichage precedent
        for ligne_boutons in self.boutons:
            for bouton in ligne_boutons:
                self.layout_grille.removeWidget(bouton)
                bouton.deleteLater()
        self.boutons = []

        # creer un bouton pour chaque case de la grille
        for l in range(grille.nb_lignes):
            ligne_boutons = []
            for c in range(grille.nb_colonnes):
                case = grille.cases[l][c]
                bouton = QPushButton()
                bouton.setFixedSize(60, 60)
                bouton.ligne = l
                bouton.colonne = c

                if case.valeur != 0:
                    bouton.setText(str(case.valeur))
                else:
                    bouton.setText("")

                bordures = self._construire_bordures(grille, l, c)

                # les cases fixes ne sont pas cliquables
                if case.fixe:
                    bouton.setEnabled(False)
                    bouton.setStyleSheet(f"font-weight: bold; font-size: 18px; background-color: #b8d4e8; {bordures}")
                else:
                    bouton.clicked.connect(self._on_clic)
                    bouton.setStyleSheet(f"font-size: 18px; background-color: #fef9e7; {bordures}")

                self.layout_grille.addWidget(bouton, l, c)
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)

    def _on_clic(self):
        bouton = self.sender()  # recupere le bouton qui a ete clique
        self.controleur.selectionner_case(bouton.ligne, bouton.colonne)
