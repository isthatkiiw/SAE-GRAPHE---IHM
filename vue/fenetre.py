from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
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
    
    def _creer_menu_jeu(self):
        barre = self.menuBar()
        menu_jeu = barre.addMenu("Jeu")

        action_verifier = QAction("Verifier", self)
        action_verifier.triggered.connect(self.controleur.verifier)
        menu_jeu.addAction(action_verifier)

        action_resoudre = QAction("Resoudre", self)
        action_resoudre.triggered.connect(self.controleur.resoudre)
        menu_jeu.addAction(action_resoudre)

        action_recommencer = QAction("Recommencer", self)
        action_recommencer.triggered.connect(self.controleur.recommencer)
        menu_jeu.addAction(action_recommencer)

    def _creer_menu_aide(self):
        barre = self.menuBar()
        menu_aide = barre.addMenu("Aide")

        action_regles = QAction("Regles", self)
        action_regles.triggered.connect(self.afficher_regles)
        menu_aide.addAction(action_regles)

        action_raccourcis = QAction("Raccourcis", self)
        action_raccourcis.triggered.connect(self.afficher_raccourcis)
        menu_aide.addAction(action_raccourcis)

        action_credits = QAction("Credits", self)
        action_credits.triggered.connect(self.afficher_credits)
        menu_aide.addAction(action_credits)

    def afficher_regles(self):
        QMessageBox.information(self, "Regles du jeu",
            "Neonaure — variante de Sudoku\n\n"
            "- Un chiffre par case\n"
            "- Chaque chiffre doit etre different de ses 8 voisins\n"
            "- Un motif de N cases doit contenir tous les chiffres de 1 a N")

    def afficher_raccourcis(self):
        QMessageBox.information(self, "Raccourcis clavier",
            "Ctrl+O  →  Ouvrir une grille\n"
            "Ctrl+S  →  Sauvegarder\n"
            "Ctrl+Z  →  Annuler le dernier coup\n"
            "Ctrl+Q  →  Quitter")

    def afficher_credits(self):
        QMessageBox.information(self, "Credits",
            "Neonaure — BUT1 Informatique\n\n"
            "Kyliane \n"
            "Kassim  \n"
            "Kevin   ")

    def ouvrir(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.charger_grille(chemin)

    def sauvegarder(self):
        chemin, _ = QFileDialog.getSaveFileName(self, "Sauvegarder la grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.sauvegarder_grille(chemin)