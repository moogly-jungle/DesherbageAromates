Le tagger est écrit en python3

Pour l'installation (testé sous linux Ubuntu 18.04.4 LTS):
Prérequis:
- python3 (testé avec python 3.6.9)
- virtualenv:
  > pip3 install --upgrade pip
  > pip3 install virtualenv

Installation:
> ./install.sh

Lancement du tagger:
> source venv/bin/activate
> python tagger/tag.py <PATH-ARBORESCENCE-IMAGE>

Le tagger enregistre les tags dans un fichier json pour chaque image dans le même répertoire que l'image elle meme.
A chaque lancement le tagger va à la premiere image qui n'a pas de tag
On peut naviguer dans les images (voir documentation en tappant > python tagger/tag.py help

