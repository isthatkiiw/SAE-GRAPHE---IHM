from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

# Fenetre principale du jeu
class FenetrePrincipale(QMainWindow):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Neonaure")
        self._creer_menu_fichier()
        self._creer_menu_jeu()
        self._creer_menu_aide()
        self.statusBar().showMessage("Bienvenue dans Neonaure !")
        self.label_chrono = QLabel("00:00")                         # label du chronometre, affiche en permanence a droite de la barre de statut
        self.statusBar().addPermanentWidget(self.label_chrono)
        self.secondes = 0                                           # nombre de secondes depuis le debut de la partie
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tic)

    def _creer_menu_fichier(self):
        barre = self.menuBar()
        menu_fichier = barre.addMenu("Fichier")

        action_ouvrir = QAction("Ouvrir", self)
        action_ouvrir.setShortcut("Ctrl+O")
        action_ouvrir.triggered.connect(self.ouvrir)
        menu_fichier.addAction(action_ouvrir)

        action_sauvegarder = QAction("Sauvegarder", self)
        action_sauvegarder.setShortcut("Ctrl+S")
        action_sauvegarder.triggered.connect(self.sauvegarder)
        menu_fichier.addAction(action_sauvegarder)

        menu_fichier.addSeparator()

        action_quitter = QAction("Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)
    
    def _creer_menu_jeu(self):
        barre = self.menuBar()
        menu_jeu = barre.addMenu("Jeu")

        action_annuler = QAction("Annuler", self)
        action_annuler.setShortcut("Ctrl+Z")
        action_annuler.triggered.connect(self.controleur.annuler)
        menu_jeu.addAction(action_annuler)

        menu_jeu.addSeparator()

        action_verifier = QAction("Verifier", self)
        action_verifier.triggered.connect(self.controleur.verifier)
        menu_jeu.addAction(action_verifier)

        action_recommencer = QAction("Recommencer", self)
        action_recommencer.triggered.connect(self.controleur.recommencer)
        menu_jeu.addAction(action_recommencer)

        action_indice = QAction("Indice", self)
        action_indice.setShortcut("Ctrl+I")
        action_indice.triggered.connect(self.controleur.indice)
        menu_jeu.addAction(action_indice)

        action_resoudre = QAction("Resoudre", self)
        action_resoudre.triggered.connect(self.controleur.resoudre)
        menu_jeu.addAction(action_resoudre)

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
            "Ctrl+I  →  Indice (place un chiffre correct)\n"
            "Ctrl+Q  →  Quitter\n"
            "\n"
            "1 a 9  →  Poser le chiffre dans la case selectionnee\n"
            "Suppr ou Retour arriere  →  Effacer le chiffre de la case")

    def afficher_credits(self):
        QMessageBox.information(self, "Credits",
            "Neonaure — BUT1 Informatique\n\n"
            "Kyliane \n"
            "Kassim  \n"
            "Kevin   ")

    def keyPressEvent(self, event):
        # quand on appuie sur une touche du clavier
        texte = event.text()
        # on verifie que la touche est bien un chiffre de 1 a 9
        # c'est le controleur qui refusera un chiffre trop grand pour le motif
        if texte != "" and texte in "123456789":
            chiffre = int(texte)
            self.controleur.selectionner_chiffre(chiffre)
        # touche suppr ou retour arriere : effacer le chiffre de la case selectionnee
        elif event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.controleur.effacer_case()

    def _texte_chrono(self):
        # convertit le nombre de secondes en minutes et secondes
        minutes = self.secondes // 60
        secondes = self.secondes % 60
        return f"{minutes:02d}:{secondes:02d}"

    def demarrer_chrono(self):
        # remet le chrono a zero et le lance
        self.secondes = 0
        self.label_chrono.setText("00:00")
        self.timer.start(1000)

    def _tic(self):
        # appele automatiquement chaque seconde par le QTimer
        self.secondes += 1
        self.label_chrono.setText(self._texte_chrono())

    def arreter_chrono(self):
        # stoppe le chrono (a la victoire ou quand la grille est resolue)
        self.timer.stop()

    def afficher_victoire(self):
        # fenetre de victoire affichant le temps realise
        QMessageBox.information(self, "Victoire !",
            f"Bravo ! Vous avez resolu la grille en {self._texte_chrono()}.")

    def ouvrir(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.charger_grille(chemin)

    def sauvegarder(self):
        chemin, _ = QFileDialog.getSaveFileName(self, "Sauvegarder la grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.sauvegarder_grille(chemin)