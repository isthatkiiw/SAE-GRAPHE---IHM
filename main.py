# Point d'entree du programme
import sys
from PyQt6.QtWidgets import QApplication
from vue.fenetre import FenetrePrincipale

# controleur temporaire pour tester la vue sans le vrai controleur
class ControleurProvisoire:
    def charger_grille(self, chemin):
        print("charger :", chemin)
    def sauvegarder_grille(self, chemin):
        print("sauvegarder :", chemin)
    def verifier(self):
        print("verifier")
    def resoudre(self):
        print("resoudre")
    def recommencer(self):
        print("recommencer")

app = QApplication(sys.argv)
controleur = ControleurProvisoire()
fenetre = FenetrePrincipale(controleur)
fenetre.show()
sys.exit(app.exec())
