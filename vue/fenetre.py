from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QStackedWidget, QInputDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

# Fenetre principale du jeu
class FenetrePrincipale(QMainWindow):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Neonaure")
        # actions de jeu, grisees tant qu'aucune grille n'est chargee
        self.actions_jeu = []
        self._creer_menu_fichier()
        self._creer_menu_jeu()
        self._creer_menu_aide()
        for action in self.actions_jeu:
            action.setEnabled(False)
            
        self.statusBar().showMessage("Bienvenue dans Neonaure !")
        self.label_indices = QLabel("") # compteur d'indices restants, vide en mode libre
        self.statusBar().addPermanentWidget(self.label_indices)
        self.label_chrono = QLabel("00:00") # label du chronometre, affiche en permanence a droite de la barre de statut
        self.statusBar().addPermanentWidget(self.label_chrono)
        self.secondes = 0 # nombre de secondes depuis le debut de la partie
        self.limite = 0  # temps maximum en secondes, 0 = pas de limite
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tic)
        # pile de pages : page 0 = menu d'accueil, page 1 = jeu
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

    def ajouter_pages(self, menu, jeu):
        self.pages.addWidget(menu)
        self.pages.addWidget(jeu)

    def afficher_menu(self):
        self.pages.setCurrentIndex(0)

    def afficher_jeu(self):
        self.pages.setCurrentIndex(1)

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
        self.actions_jeu.append(action_sauvegarder)

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
        action_recommencer.triggered.connect(self.confirmer_recommencer)
        menu_jeu.addAction(action_recommencer)

        action_indice = QAction("Indice", self)
        action_indice.setShortcut("Ctrl+I")
        action_indice.triggered.connect(self.controleur.indice)
        menu_jeu.addAction(action_indice)

        action_resoudre = QAction("Resoudre", self)
        action_resoudre.triggered.connect(self.confirmer_resoudre)
        menu_jeu.addAction(action_resoudre)

        menu_jeu.addSeparator()

        action_retour_menu = QAction("Retour au menu", self)
        action_retour_menu.triggered.connect(self.confirmer_retour_menu)
        menu_jeu.addAction(action_retour_menu)

        # toutes les actions du menu Jeu necessitent une grille chargee
        self.actions_jeu.extend([action_annuler, action_verifier, action_recommencer, action_indice, action_resoudre, action_retour_menu])

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
            "Suppr ou Retour arriere  →  Effacer le chiffre de la case\n"
            "Double clic sur une case  →  Effacer son chiffre")

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

    def demarrer_chrono(self, limite=0):
        # remet le chrono a zero et le lance (0 = pas de limite)
        self.secondes = 0
        self.limite = limite
        if limite > 0:
            minutes = limite // 60
            self.label_chrono.setText(f"{minutes:02d}:00")
        else:
            self.label_chrono.setText("00:00")
        self.timer.start(1000)

    def _tic(self):
        # appele automatiquement chaque seconde par le QTimer
        self.secondes += 1
        # avec une limite de temps, on affiche le temps restant a la place
        if self.limite > 0:
            restant = self.limite - self.secondes
            minutes = restant // 60
            secondes = restant % 60
            self.label_chrono.setText(f"{minutes:02d}:{secondes:02d}")
            if restant <= 0:
                self.timer.stop()
                self.controleur.temps_ecoule()
        else:
            self.label_chrono.setText(self._texte_chrono())

    def arreter_chrono(self):
        # stoppe le chrono (a la victoire ou quand la grille est resolue)
        self.timer.stop()

    def afficher_victoire(self):
        # fenetre de victoire affichant le temps realise
        QMessageBox.information(self, "Victoire !",
            f"Bravo ! Vous avez resolu la grille en {self._texte_chrono()}.")

    def afficher_resolution_auto(self):
        # fenetre affichee quand c'est le solveur qui a resolu la grille a la place du joueur
        QMessageBox.information(self, "Grille resolue !",
            "L'ordinateur a resolu la grille en 0.0001 seconde.\n"
            "Vous, ca fait " + self._texte_chrono() + " que vous etes dessus...\n"
            "Mais promis, on ne dira rien a personne.")

    def demander_difficulte(self):
        # propose les 4 difficultes au joueur, renvoie None s'il annule
        choix = ["Facile", "Moyen", "Difficile", "Hardcore"]
        difficulte, ok = QInputDialog.getItem(self, "Difficulte",
            "Choisissez la difficulte :", choix, 0, False)
        if ok:
            return difficulte
        return None

    def afficher_indices_restants(self, nombre):
        # met a jour le compteur du pied de page (-1 = illimites, on n'affiche rien)
        if nombre >= 0:
            self.label_indices.setText("Indices : " + str(nombre))
        else:
            self.label_indices.setText("")

    def afficher_plus_indice(self):
        # fenetre affichee quand le joueur a epuise ses indices
        QMessageBox.information(self, "Plus d'indice !",
            "Vous avez utilise tous vos indices pour cette difficulte.\n"
            "Il va falloir finir avec votre cerveau !")

    def afficher_defaite(self):
        # fenetre affichee quand le temps de la difficulte est ecoule
        QMessageBox.information(self, "Temps ecoule !",
            "Le temps est ecoule, la grille n'etait pas terminee...\n"
            "La partie recommence, plus de chance cette fois !")

    def activer_actions_jeu(self):
        # rend les actions de jeu cliquables, appele quand une grille est chargee
        for action in self.actions_jeu:
            action.setEnabled(True)

    def desactiver_actions_jeu(self):
        # grise les actions de jeu, appele quand on revient au menu d'accueil
        for action in self.actions_jeu:
            action.setEnabled(False)

    def _demander_confirmation(self, titre, message):
        # affiche une question Oui/Non et renvoie True si le joueur clique Oui
        reponse = QMessageBox.question(self, titre, message)
        return reponse == QMessageBox.StandardButton.Yes

    def confirmer_recommencer(self):
        if self._demander_confirmation("Recommencer",
                "Recommencer la grille ?\nTous vos chiffres seront effaces."):
            self.controleur.recommencer()

    def confirmer_resoudre(self):
        if self._demander_confirmation("Resoudre",
                "Laisser l'ordinateur resoudre la grille ?\nLa partie en cours sera terminee."):
            self.controleur.resoudre()

    def confirmer_retour_menu(self):
        if self._demander_confirmation("Retour au menu",
                "Revenir au menu ?\nLa partie en cours sera perdue."):
            self.controleur.retour_menu()

    def _confirmer_abandon(self):
        # renvoie True si aucune partie n'est en cours, ou si le joueur accepte de l'abandonner
        if not self.controleur.grille.cases:
            return True
        return self._demander_confirmation("Changer de grille",
                "Une partie est en cours.\nChanger de grille l'abandonnera.")

    def jouer_aleatoire(self):
        if self._confirmer_abandon():
            self.controleur.jouer_grille_aleatoire()

    def closeEvent(self, event):
        # appele automatiquement a la fermeture de la fenetre
        if self.controleur.grille.cases and not self._demander_confirmation("Quitter",
                "Quitter le jeu ?\nLa partie en cours sera perdue."):
            event.ignore()
        else:
            event.accept()

    def ouvrir(self):
        # demander confirmation si une partie est deja en cours
        if not self._confirmer_abandon():
            return
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille", "", "Fichiers JSON (*.json)")
        if chemin:
            # grille ouverte a la main : mode libre
            self.controleur.ouvrir_grille(chemin)

    def sauvegarder(self):
        chemin, _ = QFileDialog.getSaveFileName(self, "Sauvegarder la grille", "", "Fichiers JSON (*.json)")
        if chemin:
            self.controleur.sauvegarder_grille(chemin)