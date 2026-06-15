# Neonaure

Neonaure est un jeu de logique inspiré du Sudoku (avec un magnifique jeu de mot)
On utilise la bibliothèque PyQt6, en suivant une architecture MVC (Modèle - Vue - Controleur).

## Regles du jeu

La grille est découpée en motifs (les zones entourées de traits gras). Il faut remplir toute la grille en respectant 3 régles :

- un seul chiffre par case
- un chiffre doit être différent de tout ses voisins (les 8 cases autour, diagonales comprises)
- un motif de N cases doit contenir tous les chiffres de 1 jusqu'a N


## Comment jouer

Au démarrage on arrive sur le menu d'accueil. Le bouton JOUER lance une grille au hasard et demande d'abord la difficulté. On peut aussi charger une grille avec le bouton "Charger une grille", ce qui lancera le mode sans difficulté (infinité d'indices et de temps).

Pour remplir une case : on clique dessus pour la sélectionner (elle devient orange) puis on choisit un chiffre, soit en cliquant sur le pavé de droite, soit en tapant ²&directement au clavier. Si le coup ne respecte pas les regles, la case devient rouge.

### Les raccourcis

- **1 à 9** : poser le chiffre dans la case selectionnée (même si un motif à au maxima 5 cases, donc les chiffres de 6 à 9 sont d'une utilité anecdotique)
- **Suppr** ou **Retour arriere** : effacer le chiffre de la case
- **Double clic** sur une case : effacer son chiffre aussi
- **Ctrl + Z** : annuler le dernier coup
- **Ctrl + I** : demander un indice (si a déjà selectionné un motif, ça donnera un indice dans celui-ci et sinon ça mettra un indice aléatoirement dans la grille)
- **Ctrl + O** : ouvrir une grille
- **Ctrl + S** : sauvegarder
- **Ctrl + Q** : quitter

## Les difficultés

Quand on lance une partie aléatoire, on choisit un niveau. Chaque niveau impose une limite de temps (un compte à rebours) et un nombre d'indices limité :

 Facile     30 min  5 indices
 Moyen      20 min  3 indices
 Difficile  10 min  1 indice
 Hardcore   5 min   0 indice

Si le temps est écoulé avant la fin, la partie est perdue et recommence. En mode "Charger une grille" il n'y a pas de limite, c'est un mode libre pour s'entrainer.

## Fonctionnalités

- charger et sauvegarder une grille 
- jouer avec la souris ou le clavier
- verification des règles en temps réel
- annulation des coups (Ctrl+Z)
- solveur automatique (algorithme de backtracking)
- systeme d'indices qui place un chiffre correct
- chronometre / compte à rebours
- 4 niveaux de difficulté
- menu d'accueil

## Organisation du projet

Le code est séparé selon le modèle MVC :

modele      les données du jeu (Case, Motif, Grille)
vue         l'affichage avec PyQt6 (fenetre, grille, menu)
controleur  le lien entre le modèle et la vue
solveur     l'algorithme de résolution
Grille      les grilles de jeu au format JSON
main.py      le point d'entrée du programme


## Si vous avez du mal.. (SOLVEUR)

Le solveur est disponible dans jeu > résoudre avec le mot de passe "conoirlebest" 

## Équipe

- **Kyliane** (isthatkiiw sur github)
- **Kassim** 
- **Kevin** 
