from modele.grille import Grille
from vue.fenetre import FenetrePrincipale
from vue.grille_widget import GrilleWidget
from solveur.solveur import Solveur

class Controleur:

    def __init__(self):
        self.grille = Grille()
        self.fenetre = FenetrePrincipale(self)
        self.grille_widget = GrilleWidget(self)
        self.fenetre.setCentralWidget(self.grille_widget)
        self.case_selectionnee = None
        self.chiffre_selectionne = 0
        # case du dernier coup refuse, affichee en rouge par la vue
        self.case_erreur = None
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
        self.fenetre.demarrer_chrono()
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
        if not self.grille.cases:
            return
        if Solveur().resoudre(self.grille):
            self.grille_widget.afficher_grille(self.grille)
            self.fenetre.arreter_chrono()
            self.fenetre.statusBar().showMessage("Grille resolue !")
        else:
            self.grille_widget.afficher_grille(self.grille)
            self.fenetre.statusBar().showMessage("Cette grille n'a pas de solution.")

    def selectionner_case(self, ligne, colonne):
        if not self.grille.cases:
            return
        # un nouveau clic efface l'erreur precedente
        self.case_erreur = None
        self.case_selectionnee = self.grille.cases[ligne][colonne]
        if self.chiffre_selectionne != 0:
            self._poser_chiffre()
        else:
            self.grille_widget.afficher_grille(self.grille)

    def selectionner_chiffre(self, chiffre):
        self.chiffre_selectionne = chiffre
        if self.case_selectionnee is not None:
            self._poser_chiffre()
        else:
            self.grille_widget.afficher_selection_pave()

    def effacer_case(self):
        case = self.case_selectionnee
        # rien a faire si aucune case n'est selectionnee, si elle est fixe ou deja vide
        if case is None or case.fixe or case.valeur == 0:
            return
        # sauvegarder avant modification pour le Ctrl+Z
        self.historique.append((case, case.valeur))
        case.valeur = 0
        # une case videe n'est plus en erreur pour qu'elle reste selectionnee
        self.case_erreur = None
        self.grille_widget.afficher_grille(self.grille)

    def _poser_chiffre(self):
        case = self.case_selectionnee
        if case.fixe:
            return

        # refuser le coup s'il ne respecte pas les regles du jeu
        if not self.grille.placement_valide(case.ligne, case.colonne, self.chiffre_selectionne):
            self.case_erreur = case
            # on garde la case selectionnee 
            self.chiffre_selectionne = 0
            self.grille_widget.afficher_grille(self.grille)
            self.grille_widget.afficher_selection_pave()
            self.fenetre.statusBar().showMessage("Coup invalide : ce chiffre ne respecte pas les regles ici.")
            return

        self.case_erreur = None
        # sauvegarder avant modification pour le Ctrl+Z
        self.historique.append((case, case.valeur))
        case.valeur = self.chiffre_selectionne
        # on garde la case selectionnee pour pouvoir changer sa valeur sans recliquer
        self.chiffre_selectionne = 0
        self.grille_widget.afficher_grille(self.grille)
        self.grille_widget.afficher_selection_pave()
        if self.grille.est_resolue():
            self.fenetre.arreter_chrono()
            self.fenetre.statusBar().showMessage("La grille est resolue ! Vous etes un expert du Neonaure !!")
            self.fenetre.afficher_victoire()