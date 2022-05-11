# Qu'est-ce que c'est ?
Gestion de tournoi d'échec

# Installation :
## Environnement virtuel(facultatif)
>pip install virtualenv<br>
>virtualenv .venv<br>
>source .venv/bin/activate

.venv est le nom par convention mais peut-être remplacé par ce que vous voulez.<br>
Pensez juste à le changer dans les commandes.

**Si vous utilisez un environnement virtuel, pensez à activer chaque fois avant d'utiliser le programme.**

## Installation des packages nécéssaires
>pip install -r requirement.txt

# Flake 8
Assurez-vous que flake8-html est installé en entrant la commande suivante :
>python3 -m pip install flake8-html<br>
(py pour windows)

Entrez ensuite cette commande pour générer le rapport flake8 :
>flake8 --format html --max-line-length 119 --htmldir=flake8-report --extend-exclude .venv

Naviguez maintenant dans le dossier flake8-report nouvellement <br>
créé est ouvrez dans votre navigateur le fichier index.html

# Lancement du programme :
>py -m main

## Fonctionnement :
Chaque menu donne le choix avec un numéro à entrer pour séléctionner un <br>
élément de la liste ou 'q' pour revenir au menu précédent ou quitter.

2 sous menu sont présents dans le menu principal : un pour le tournoi et un pour les rapports.