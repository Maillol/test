Test logiciel
=============

Niveau de test
--------------

On peut tester plusieurs niveaux d'un logiciel

- Tester le logiciel complet en se métant à la place d'un utilisateur. (test d'acceptation)
- Tester les fonctions et classes composant le logiciel. (test unitaire)

Et entre ces 2 niveaux il existe des niveau intermédiare, dont la dénomination change en fonction des années et des normes.
L'idée à retenir et que si un logiciel est un aggregat de composants, on peut aussi tester ces composants indépadaments.


Boite noire / boite blanche
---------------------------

En boite noire on se base uniquement sur les spécifications en boite blanche on se base sur le code source.

- Quelle sont selon vous, les avantages/inconvénients des tests en boite blanche/boite noire ?
- Quelle impacte il y a t'il si la personne qui écrit les tests est celle qui à écrit le programme ?

Test manuel / Test automatique
------------------------------

Les tests manuels sont couteux à executer, les tests automatiques sont couteux à mettre en place mais
peuvent être rejoué très facilement.


Test unitaire, exo:
-------------------

Dans cet exercice, on va tester une application de gestion de chambres d'hotel.

I - Executer des tests:

Allez dans le répertoire **unittest_training** est executer la commande:

    python3 -m unittest -v


II - Ecrire des tests:

Nous allons completer les tests dans le fichier *unittest_training/tests/test_model.py*
Avans ça, jetez un oeuil sur la documentation de la classe Hotel:

    python3 -c 'from hotels import model; help(model.Hotel)'


Le fichier test_model.py importe la classe Hotel et va executer divers opérations avec afin de la tester.

L'écriture de test ce fait généralement comme ceci:

1. Hériter de la classe unittest.TestCase.

2. Redéfinir la méthode setUp dans laquelle on initialisera l'objet à tester.

3. Définir plusieur méthodes dont le nom commence par test et qui controleront
   que l'objet à tester est bien comme on l'attend.
   Dans ces méthodes on appelera self.assertEqual pour faire ces vérifications,
   mais il existe d'autre posibilités:
   https://docs.python.org/3/library/unittest.html#assert-methods

Dans le fichier *unittest_training/tests/test_model.py* completez l'écriture des méthodes.
