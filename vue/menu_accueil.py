from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

# Page d'accueil du jeu : titre, bouton jouer et boutons secondaires
class MenuAccueil(QWidget):

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur

        # fond sombre, texte creme 
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("MenuAccueil { background-color: #202020; }")

        layout = QVBoxLayout()
        self.setLayout(layout)

        titre = QLabel("NEONAURE")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size: 60px; font-weight: bold; color: #fef9e7; letter-spacing: 12px;")

        # bouton principal en orange
        bouton_jouer = QPushButton("JOUER")
        bouton_jouer.setFixedSize(240, 70)
        bouton_jouer.setStyleSheet("font-size: 24px; font-weight: bold; color: black; background-color: #f5a623; border: 3px solid #fef9e7;")
        bouton_jouer.clicked.connect(self.controleur.jouer_grille_aleatoire)

        # boutons secondaires en bleu
        bouton_charger = QPushButton("Charger une grille")
        bouton_regles = QPushButton("Regles")
        bouton_quitter = QPushButton("Quitter")
        for bouton in [bouton_charger, bouton_regles, bouton_quitter]:
            bouton.setFixedSize(180, 40)
            bouton.setStyleSheet("font-size: 14px; color: black; background-color: #b8d4e8; border: 1px solid #fef9e7;")

        bouton_charger.clicked.connect(self.controleur.fenetre.ouvrir)
        bouton_regles.clicked.connect(self.controleur.fenetre.afficher_regles)
        bouton_quitter.clicked.connect(self.controleur.fenetre.close)

        # centrage verticale
        layout.addStretch(2)
        layout.addWidget(titre)
        layout.addSpacing(40)
        layout.addWidget(bouton_jouer, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(bouton_charger, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(bouton_regles, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(bouton_quitter, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(3)
