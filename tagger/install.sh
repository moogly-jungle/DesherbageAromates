#!/bin/bash

# prerequis: python3 virtualenv
# (testé avec python 3.6.9)

python3 -m virtualenv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip3 install numpy matplotlib opencv-python
echo
echo "** 'source venv/bin/activate' pour lancer l'environnement virtuel **"
