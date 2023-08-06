Package 2048 - Projet informatique de 1er semestre ENSAE
========================================================

Ce module propose une fonction pour résoudre le 2048.
La fonction adeterminer résout le 2048 en utilisant la stratégie du snake.
Afin de juger l'efficacité de cette algorithme, vous pouvez utiliser la fonction evaluate_strategy qui prend en argument la
fonction adeterminer et le nombre de parties effectuées.

Comment notre programme résout-il le 2048 ?
-------------------------------------------

Blablabla

Quels tests avons nous programmé pour nos fonctions ?
-----------------------------------------------------

Blablabla

Quelques commandes utiles.
--------------------------

Ce module peut être installé avec pip :

    pip install pack2048

Exemple d'usage :

    >>> from pack2048 import evaluate_strategy, adeterminer
    >>> evaluate_strategy(adeterminer,10)

Les tests doivent être effectués en console à l'aide de la commande suivante :

    python -m pack2048

Si vous souhaitez davantages de détails sur les tests, utilisez la commande suivante :

    python -m pack2048 -v

Ce code est sous licence GNU AGPLv3.