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

    for t in tags :
        ll.draw_tag(img, t)
    cv2.namedWindow('image')
    cv2.moveWindow('image', 800, 0)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    n = 1
    for t in tags :

        cv2.imwrite(ll.roi_file(fn, n), ll.cut_patch(img, ll.graphic_pos(img_size, t[1])[0], ll.graphic_pos(img_size, t[1])[1], ll.graphic_pos(img_size, t[2])[0], ll.graphic_pos(img_size, t[2])[1]))
        
        n += 1


def extract_patch_hsv(fn, tags):
    """ fn est le nom du fichier image d'origine
        tags est la liste des tags en coordonnées relatives"""
    print('  - extracting patch from ', fn)
    img = cv2.imread(fn)
    if img.size == 0:
        print("Error: bad file name: " + fn)
        return
    img = cv2.resize(img, img_size)

    for t in tags :
        ll.draw_tag(img, t)
    cv2.namedWindow('image')
    cv2.moveWindow('image', 800, 0)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    n = 1
    for t in tags :

        image = ll.cut_patch(img, ll.graphic_pos(img_size, t[1])[0], ll.graphic_pos(img_size, t[1])[1], ll.graphic_pos(img_size, t[2])[0], ll.graphic_pos(img_size, t[2])[1])

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cv2.imwrite(ll.roi_hsv_file(fn, n), hsv_image)
        
        n += 1