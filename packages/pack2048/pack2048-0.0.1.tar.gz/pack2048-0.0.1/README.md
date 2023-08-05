Package 2048 - Projet informatique de 1er semestre ENSAE
========================================================

Ce module propose une fonction pour r�soudre le 2048 avec une efficacit� inversement proportionnelle � sa rapidit�.
La fonction Evaluer(n,c) r�sout le 2048 n fois. c est un entier dont la taille d�termine l'efficacit� de l'algorithme.
Par exemple, si c=100, l'algorithme sera relativement rapide mais peu efficace.
Si c=1000, l'algorithme gagnera avec une forte probabilit� mais sera excessivement lent.
Une barre de progression sera visible. Toutefois, le pourcentage peut diminuer si l'algorithme trouve une solution astucieuse impr�vu.
De plus lorsque un 2048 est r�solu, la barre est remis � 0%.

Quelques d�tails sur la strat�gie :

La strat�gie consiste � faire plusieurs parties en choisissant la direction au hasard. Pour chaques parties, le score final est calcul�.
On calcule alors la moyenne des scores pour une direction donn�e. La direction choisi sera celle dont le score associ�e est le plus �lev�.

Quelques d�tails sur les tests :

Pour executer les tests unitaires, il faut lancer le script Test.py � la main


Ce module peut �tre install� avec pip:

    pip install pack2048

Exemple d'usage:

    >>> from pack2048 import Evaluer
    >>> Evaluer(10,100)

Ce code est sous licence GNU AGPLv3.