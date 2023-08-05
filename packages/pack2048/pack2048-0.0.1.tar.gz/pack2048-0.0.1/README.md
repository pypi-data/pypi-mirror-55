Package 2048 - Projet informatique de 1er semestre ENSAE
========================================================

Ce module propose une fonction pour résoudre le 2048 avec une efficacité inversement proportionnelle à sa rapidité.
La fonction Evaluer(n,c) résout le 2048 n fois. c est un entier dont la taille détermine l'efficacité de l'algorithme.
Par exemple, si c=100, l'algorithme sera relativement rapide mais peu efficace.
Si c=1000, l'algorithme gagnera avec une forte probabilité mais sera excessivement lent.
Une barre de progression sera visible. Toutefois, le pourcentage peut diminuer si l'algorithme trouve une solution astucieuse imprévu.
De plus lorsque un 2048 est résolu, la barre est remis à 0%.

Quelques détails sur la stratégie :

La stratégie consiste à faire plusieurs parties en choisissant la direction au hasard. Pour chaques parties, le score final est calculé.
On calcule alors la moyenne des scores pour une direction donnée. La direction choisi sera celle dont le score associée est le plus élevé.

Quelques détails sur les tests :

Pour executer les tests unitaires, il faut lancer le script Test.py à la main


Ce module peut être installé avec pip:

    pip install pack2048

Exemple d'usage:

    >>> from pack2048 import Evaluer
    >>> Evaluer(10,100)

Ce code est sous licence GNU AGPLv3.