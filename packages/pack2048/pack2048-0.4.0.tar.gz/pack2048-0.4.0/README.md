Package 2048 - Projet informatique de 1er semestre ENSAE
========================================================

Ce module propose une fonction pour r�soudre le 2048.
La fonction snake_strategy r�sout le 2048 en utilisant la strat�gie du snake.
Afin de juger l'efficacit� de cet algorithme, vous pouvez utiliser la fonction evaluate_strategy 
qui prend en argument la fonction snake_strategy et le nombre de parties effectu�es.

Comment notre programme r�sout-il le 2048 ?
-------------------------------------------
La fonction snake_strategy prend en argument la grille de 2048 et les trois derniers mouvements effectu�s.
Elle renvoie une direction de jeu en accord avec le principe du programme qui suit.
L'id�e est d'agencer les cases de mani�re d�croissante, de fa�on � organiser un "snake" pour faciliter le repli de toutes ces cases.
En favorisant la fusion sur une m�me ligne ou � partir d'une ligne sup�rieure, notre algorithme assouplit le principe du snake.
A partir du score de 512, le programme accorde une grande importance au nombre de z�ros pr�sents dans le jeu, pour �viter � tout prix la fin du jeu.
De plus, il essaie de pr�voir cinq coups en avance afin de maximiser son score.

La fonction evaluate_strategy permet d'�valuer une strat�gie de jeu.
Pour cela, elle effectue le nombre de parties donn� en argument et renvoie un g�n�rateur.
Pour chaque partie, la grille de 2048 est initialis�e, puis une direction est choisie gr�ce � la strat�gie donn�e en argument.
La grille est alors mise � jour en effectuant un mouvement selon cette direction, et simultan�ment de nouveaux 2 ou 4 sont g�n�r�s dans la grille.
Si la grille arrive en situation de gameover, la partie se termine.


Quels tests avons nous programm� pour nos fonctions ?
-----------------------------------------------------

Le test test_game_play permet de v�rifier si la grille de 2048 r�agit correctement � l'annonce d'une direction.

Le test test_basic permet de v�rifier que la direction renvoy�e par la strat�gie snake_strat�gie est bien un �l�ment de {0, 1, 2, 3}.

Le test test_advanced permet de v�rifier la coh�rence de l'�volution de la grille de 2048 avec la strat�gie snake_strat�gie. 
Il se place dans le cas o� l'algorithme n'effectue aucune pr�vision sur les prochains tours.
Il s'int�resse particuli�rement au choix d'effectuer une fusion ou de favoriser une certaine direction.

Quelques commandes utiles.
--------------------------

Ce module peut �tre install� avec pip :

    pip install pack2048

Exemple d'usage :

    >>> from pack2048 import evaluate_strategy, snake_strategy
    >>> evaluate_strategy(snake_strategy,10)

Les tests doivent �tre effectu�s en console � l'aide de la commande suivante :

    python -m pack2048

Si vous souhaitez davantages de d�tails sur les tests, utilisez la commande suivante :

    python -m pack2048 -v

Ce code est sous licence GNU AGPLv3.