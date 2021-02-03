#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import local_lib as ll

img_size = (1024, 768)

def extract_patch(fn, tags):
    """ fn est le nom du fichier image d'origine
        tags est la liste des tags en coordonnées relatives"""
    print('  - extracting patch from ', fn)
    img = cv2.imread(fn)
    if img.size == 0:
        print("Error: bad file name: " + fn)
        return
    img = cv2.resize(img, img_size)

    # MARCEL: dessine les rectangles des patchs avec les bonnes couleurs 

    cv2.namedWindow('image')
    cv2.moveWindow('image', 800, 0)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
