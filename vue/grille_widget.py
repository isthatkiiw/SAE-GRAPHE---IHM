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

                # les cases fixes ne sont pas cliquables
                if case.fixe:
                    bouton.setEnabled(False)
                    bouton.setStyleSheet("font-weight: bold; background-color: #d0d0d0;")
                else:
                    bouton.clicked.connect(self._on_clic)
                    bouton.setStyleSheet("background-color: white;")

                self.layout_grille.addWidget(bouton, l, c)
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)

    def _on_clic(self):
        bouton = self.sender()  # recupere le bouton qui a ete clique
        self.controleur.selectionner_case(bouton.ligne, bouton.colonne)
