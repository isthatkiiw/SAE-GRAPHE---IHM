from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout

# Bouton d'une case : comme un bouton normal, mais detecte aussi le double clic
class BoutonCase(QPushButton):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur

    def mouseDoubleClickEvent(self, event):
        # double clic sur la case : on demande au controleur d'effacer son chiffre
        self.controleur.double_clic_case(self.ligne, self.colonne)

# Widget qui affiche la grille de jeu sous forme de boutons
class GrilleWidget(QWidget):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.boutons = []  # tableau 2D de boutons, un par case
        self.boutons_pave = []  # liste des boutons du pave de chiffres

        # disposition principale : grille a gauche, pave de chiffres a droite
        self.layout_principal = QHBoxLayout()
        self.setLayout(self.layout_principal)

        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0)

        self.layout_pave = QVBoxLayout()
        self.layout_pave.setSpacing(5)

        # la grille et le pave restent compacts et centres, meme en plein ecran
        colonne_grille = QVBoxLayout()
        colonne_grille.addStretch(1)
        colonne_grille.addLayout(self.layout_grille)
        colonne_grille.addStretch(1)

        colonne_pave = QVBoxLayout()
        colonne_pave.addStretch(1)
        colonne_pave.addLayout(self.layout_pave)
        colonne_pave.addStretch(1)

        self.layout_principal.addStretch(1)
        self.layout_principal.addLayout(colonne_grille)
        # petit espace fixe entre la grille et le pave
        self.layout_principal.addSpacing(40)
        self.layout_principal.addLayout(colonne_pave)
        self.layout_principal.addStretch(1)

    def afficher_pave(self, n_max):
        # supprimer les anciens boutons du pave
        while self.layout_pave.count():
            widget = self.layout_pave.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        self.boutons_pave = []

        # creer un bouton par chiffre de 1 a n_max
        for chiffre in range(1, n_max + 1):
            bouton = QPushButton(str(chiffre))
            bouton.setFixedSize(50, 50)
            bouton.setStyleSheet("font-size: 16px;")
            bouton.chiffre = chiffre
            bouton.clicked.connect(self._on_clic_pave)
            self.layout_pave.addWidget(bouton)
            self.boutons_pave.append(bouton)

    def afficher_selection_pave(self):
        # met en orange le bouton du pave correspondant au chiffre selectionne
        for bouton in self.boutons_pave:
            if bouton.chiffre == self.controleur.chiffre_selectionne:
                bouton.setStyleSheet("font-size: 16px; background-color: #f5a623;")
            else:
                bouton.setStyleSheet("font-size: 16px;")

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

        def couleur(epaisseur):
            return "black" if epaisseur == 3 else "#aaaaaa"

        return (f"border-top: {haut}px solid {couleur(haut)};"
                f"border-bottom: {bas}px solid {couleur(bas)};"
                f"border-left: {gauche}px solid {couleur(gauche)};"
                f"border-right: {droite}px solid {couleur(droite)};")

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
                bouton = BoutonCase(self.controleur)
                bouton.setFixedSize(60, 60)
                bouton.ligne = l
                bouton.colonne = c

                if case.valeur != 0:
                    bouton.setText(str(case.valeur))
                else:
                    bouton.setText("")

                bordures = self._construire_bordures(grille, l, c)
                case_selectionnee = self.controleur.case_selectionnee

                # les cases fixes ne sont pas cliquables
                if case.fixe:
                    bouton.setEnabled(False)
                    bouton.setStyleSheet(f"font-weight: bold; font-size: 18px; color: black; background-color: #b8d4e8; {bordures}")
                # le rouge de l'erreur passe avant l'orange de la selection
                elif case == self.controleur.case_erreur:
                    bouton.clicked.connect(self._on_clic)
                    bouton.setStyleSheet(f"font-size: 18px; color: black; background-color: #e74c3c; {bordures}")
                elif case == case_selectionnee:
                    bouton.clicked.connect(self._on_clic)
                    bouton.setStyleSheet(f"font-size: 18px; color: black; background-color: #f5a623; {bordures}")
                else:
                    bouton.clicked.connect(self._on_clic)
                    bouton.setStyleSheet(f"font-size: 18px; color: black; background-color: #fef9e7; {bordures}")

                self.layout_grille.addWidget(bouton, l, c)
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)

    def _on_clic(self):
        bouton = self.sender()  # recupere le bouton qui a ete clique
        self.controleur.selectionner_case(bouton.ligne, bouton.colonne)

    def _on_clic_pave(self):
        bouton = self.sender()  # recupere le bouton du pave qui a ete clique
        self.controleur.selectionner_chiffre(bouton.chiffre)
