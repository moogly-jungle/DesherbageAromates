# Tagger

Le tagger est écrit en python3

Pour l'installation (testée sous linux Ubuntu 18.04.4 LTS):
Prérequis:
- python3 (testé avec python 3.6.9)
- virtualenv:
```
  pip3 install --upgrade pip
  pip3 install virtualenv
```

Installation:
```
  ./install.sh
```

Placer l'arborescence des images dans le répertoire `data` du
repository (ou ailleurs, mais c'est le répertoire par défaut, ça n'est
pas obligatoire, de toute façon il faudra le spécifier en lançant le
script). Les données ne figurent pas dans le dépot.

Lancement du tagger:
```
  source venv/bin/activate
  python src/tag.py <PATH-ARBORESCENCE-IMAGE> <TAG-DIR>
```

Le tagger va chercher les fichiers images sous la forme de fichiers
JPG dans l'arborescence de `<PATH-ARBORESCENCE-IMAGE>`.

Le tagger enregistre les tags dans un fichier json pour chaque image
et place le fichier dans `<TAG-DIR>`. Le répertoire est créé si besoin.

A chaque lancement le tagger va à la premiere image qui n'a pas de tag.

On peut naviguer dans les images (voir documentation en tappant
`python tagger/tag.py help`)

