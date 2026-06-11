# Point d'entree du programme
import sys
from PyQt6.QtWidgets import QApplication
from controleur.controleur import Controleur

app = QApplication(sys.argv)
controleur = Controleur()
controleur.fenetre.show()
sys.exit(app.exec())