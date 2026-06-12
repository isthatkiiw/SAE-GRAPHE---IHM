import random
from modele.grille import Grille
from vue.fenetre import FenetrePrincipale
from vue.grille_widget import GrilleWidget
from vue.menu_accueil import MenuAccueil
from solveur.solveur import Solveur

class Controleur:

    def __init__(self):
        self.grille = Grille()
        self.fenetre = FenetrePrincipale(self)
        self.grille_widget = GrilleWidget(self)
        self.menu_accueil = MenuAccueil(self)
        self.fenetre.ajouter_pages(self.menu_accueil, self.grille_widget)
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
        # oublier la selection de la partie precedente
        self.case_selectionnee = None
        self.chiffre_selectionne = 0
        self.case_erreur = None
        n_max = max(motif.taille() for motif in self.grille.motifs)
        self.grille_widget.afficher_grille(self.grille)
        self.grille_widget.afficher_pave(n_max)
        # basculer du menu d'accueil vers la page de jeu
        self.fenetre.afficher_jeu()
        self.fenetre.demarrer_chrono()
        self.fenetre.statusBar().showMessage("Grille chargee !")

    def jouer_grille_aleatoire(self):
        # tirer un numero au hasard parmi les grilles grille1.json a grille9.json
        numero = random.randint(1, 9)
        self.charger_grille("Grille/grille" + str(numero) + ".json")

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
            self.fenetre.afficher_resolution_auto()
            # repartir sur une grille vierge une fois la pop up fermee
            self.recommencer()
        else:
            self.grille_widget.afficher_grille(self.grille)
            self.fenetre.statusBar().showMessage("Cette grille n'a pas de solution.")

    def indice(self):
        if not self.grille.cases:
            return

        # memoriser la valeur de chaque case avant de resoudre
        sauvegarde = []
        for ligne in self.grille.cases:
            for case in ligne:
                sauvegarde.append((case, case.valeur))

        # resoudre la grille pour connaitre les bonnes valeurs
        if not Solveur().resoudre(self.grille):
            self.fenetre.statusBar().showMessage("Pas d'indice possible : un des chiffres deja poses est faux.")
            return

        # retrouver les cases qui etaient vides avant la resolution
        cases_vides = []
        for case, ancienne_valeur in sauvegarde:
            if ancienne_valeur == 0:
                cases_vides.append(case)

        if not cases_vides:
            self.fenetre.statusBar().showMessage("La grille est deja remplie !")
            return

        case_indice = None
        # si la case selectionnee est vide, on revele celle-ci
        if self.case_selectionnee in cases_vides:
            case_indice = self.case_selectionnee
        # si la case selectionnee est deja remplie, on revele une case vide de son motif
        elif self.case_selectionnee is not None:
            for motif in self.grille.motifs:
                if self.case_selectionnee in motif.cases:
                    vides_du_motif = []
                    for case in motif.cases:
                        if case in cases_vides:
                            vides_du_motif.append(case)
                    if vides_du_motif:
                        case_indice = random.choice(vides_du_motif)

        # sans selection, ou si le motif est deja complet : une case vide au hasard
        if case_indice is None:
            case_indice = random.choice(cases_vides)

        # garder la valeur trouvee par le solveur pour cette case
        valeur_indice = case_indice.valeur

        # remettre les valeurs du joueur partout
        for case, ancienne_valeur in sauvegarde:
            case.valeur = ancienne_valeur

        # poser l'indice comme un coup normal, annulable avec Ctrl+Z
        self.historique.append((case_indice, case_indice.valeur))
        case_indice.valeur = valeur_indice
        self.grille_widget.afficher_grille(self.grille)
        self.fenetre.statusBar().showMessage("Indice : un chiffre a ete place pour vous.")
        if self.grille.est_resolue():
            self.fenetre.arreter_chrono()
            self.fenetre.afficher_victoire()
            # repartir sur une grille vierge une fois la pop up fermee
            self.recommencer()

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

    def deselectionner_case(self):
        if not self.grille.cases:
            return
        self.case_selectionnee = None
        self.case_erreur = None
        self.grille_widget.afficher_grille(self.grille)

    def selectionner_chiffre(self, chiffre):
        self.chiffre_selectionne = chiffre
        if self.case_selectionnee is not None:
            self._poser_chiffre()
        else:
            self.grille_widget.afficher_selection_pave()

    def double_clic_case(self, ligne, colonne):
        # double clic sur une case : on la selectionne puis on efface son chiffre
        if not self.grille.cases:
            return
        self.case_selectionnee = self.grille.cases[ligne][colonne]
        self.effacer_case()

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
            # repartir sur une grille vierge une fois la pop up fermee
            self.recommencer()