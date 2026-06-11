from modele.grille import Grille
from vue.fenetre import FenetrePrincipale
from vue.grille_widget import GrilleWidget

class Controleur:

    def __init__(self):
        self.grille = Grille()
        self.fenetre = FenetrePrincipale(self)
        self.grille_widget = GrilleWidget(self)
        self.fenetre.setCentralWidget(self.grille_widget)
        self.case_selectionnee = None
        self.chiffre_selectionne = 0
        # chemin du fichier ouvert, utile pour recommencer
        self.chemin_actuel = None
        # pile des coups pour le Ctrl+Z : liste de (case, ancienne_valeur)
        self.historique = []

    def charger_grille(self, chemin):
        self.grille.charger(chemin)
        self.chemin_actuel = chemin
        self.historique = []
        n_max = max(motif.taille() for motif in self.grille.motifs)
        self.grille_widget.afficher_grille(self.grille)
        self.grille_widget.afficher_pave(n_max)
        self.fenetre.statusBar().showMessage("Grille chargee !")

    def sauvegarder_grille(self, chemin):
        self.grille.sauvegarder(chemin)
        self.fenetre.statusBar().showMessage("Grille sauvegardee !")

    def verifier(self):
        if not self.grille.cases:
            return
        if self.grille.est_resolue():
            self.fenetre.statusBar().showMessage("Bravo ! La grille est resolue !")
        else:
            self.fenetre.statusBar().showMessage("La grille n'est pas encore resolue.")

    def recommencer(self):
        if self.chemin_actuel:
            self.charger_grille(self.chemin_actuel)
            
    def annuler(self):
        if not self.historique:
            return
        case, ancienne_valeur = self.historique.pop()
        case.valeur = ancienne_valeur
        self.grille_widget.afficher_grille(self.grille)

    def resoudre(self):
        # implemente en phase 4
        pass

    def selectionner_case(self, ligne, colonne):
        if not self.grille.cases:
            return
        self.case_selectionnee = self.grille.cases[ligne][colonne]
        if self.chiffre_selectionne != 0:
            self._poser_chiffre()

    def selectionner_chiffre(self, chiffre):
        self.chiffre_selectionne = chiffre
        if self.case_selectionnee is not None:
            self._poser_chiffre()

    