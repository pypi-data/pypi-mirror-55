Package 2048 - Projet informatique de 1er semestre ENSAE
========================================================

Ce module propose une fonction pour r�soudre le 2048.
La fonction 'snake_strategy' r�sout le 2048 en utilisant la strat�gie du snake.
Afin de juger l'efficacit� de cette algorithme, vous pouvez utiliser la fonction 'evaluate_strategy' 
qui prend en argument la fonction 'snake_strategy' et le nombre de parties effectu�es.

Comment notre programme r�sout-il le 2048 ?
-------------------------------------------

Blablabla

Quels tests avons nous programm� pour nos fonctions ?
-----------------------------------------------------

Blablabla

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