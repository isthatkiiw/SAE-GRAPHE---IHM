from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

# Fenetre principale du jeu
class FenetrePrincipale(QMainWindow):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Neonaure")
        self._creer_menu_fichier()

    def _creer_menu_fichier(self):
        barre = self.menuBar()
        menu_fichier = barre.addMenu("Fichier")

        action_ouvrir = QAction("Ouvrir", self)
        action_ouvrir.triggered.connect(self.ouvrir)
        menu_fichier.addAction(action_ouvrir)

        action_sauvegarder = QAction("Sauvegarder", self)
        action_sauvegarder.triggered.connect(self.sauvegarder)
        menu_fichier.addAction(action_sauvegarder)

        menu_fichier.addSeparator()

        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)

    def ouvrir(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.charger_grille(chemin)

    def sauvegarder(self):
        chemin, _ = QFileDialog.getSaveFileName(self, "Sauvegarder la grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.sauvegarder_grille(chemin)