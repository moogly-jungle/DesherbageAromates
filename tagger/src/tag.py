#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import local_lib as ll
import json
try:
    from math import abs
except: pass
import extract_patch

# TODO: un clear all tag

the_files = None


def get_nth_file_path(n):
    return the_files[n][0] + '/' + the_files[n][1]


img = None


typ = 'adventice'
tags = []
refPt = []
cropping = False





def mouse_handler(event, x, y, flags, param):
    global img, refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        tags.append((typ, ll.relative_pos(img_size, refPt[0]), ll.relative_pos(img_size, refPt[1])))
        ll.draw_tag(img, tags[-1])
        cv2.imshow('image', img)


def read_tags(fn):
    try:
        with open(ll.tag_file(fn)) as json_file:
            the_tags = json.load(json_file)['tags']
    except:
        the_tags = []
        print('  - no previous tags --')
    return the_tags

def dump_yolo_tags(tags, outfile):
    for t in tags:
        outfile.write("{} {} {} {} {}\n".format(
            ll.CLASSES[t[0]], (t[1][0]+t[2][0])/2.0, (t[1][1]+t[2][1])/2.0, abs(t[2][0]-t[1][0]), abs(t[2][1]-t[1][1])))


def save_tags(fn, tagged_img):
    with open(ll.tag_file(fn), 'w') as outfile:
        fn_data = {'path': fn, 'tags': tags}
        json.dump(fn_data, outfile)

    with open(ll.tag_file_yolo(fn), 'w') as outfile:
        dump_yolo_tags(tags, outfile)

    print('  - tags saved in ' + ll.tag_file(fn))
    print('  - yolo tags saved in ' + ll.tag_file_yolo(fn))
    cv2.imwrite(ll.tag_img_file(fn), tagged_img)
    print('  - tagged image saved in ' + ll.tag_img_file(fn))


def process_file(fn):
    global img, typ, tags
    img = cv2.imread(fn)
    if img.size == 0:
        print("Error: bad file name: " + fn)
        return
    # TOTO: resize avec proportion
    img = cv2.resize(img, img_size)
    tags = read_tags(fn)
    for t in tags:
        ll.draw_tag(img, t)
    cv2.namedWindow('image')
    cv2.moveWindow('image', 800, 0)
    cv2.setMouseCallback('image', mouse_handler)
    cv2.imshow("image", img)
    while(True):
        key = cv2.waitKey(0)
        if key in [ord('q'), ord('n'), ord('p'), 83, 81]:
            break
        if key == ord('a'):
            typ = 'adventice'
        if key == ord('z'):
            typ = 'plant'
        if key == ord('e'):
            typ = 'unknown'
        if key == ord('s'):
            save_tags(fn, img)
        redraw = False
        if key == ord('u'):  # UNDO
            if len(tags) > 0:
                tags = tags[0:-1]
            redraw = True
        if key == ord('c'):  # UNDO
            tags = []
            redraw = True
        img = cv2.imread(fn)
        img = cv2.resize(img, img_size)
        for t in tags:
            ll.draw_tag(img, t)
        cv2.imshow("image", img)
    cv2.destroyAllWindows()
    save_tags(fn, img)
    return key

def tag_process():
    n = 0
    # on cherche le premier fichier non taggé
    while (os.path.isfile(ll.tag_file(get_nth_file_path(n)))):
        print('- ' + get_nth_file_path(n) + ' already tagged')
        n = n+1
    while(True):
        print('--- processing file ' + str(n) + ' : ' + get_nth_file_path(n))
        order = process_file(get_nth_file_path(n))
        if order == ord('q'):
            break
        if order in [ord('p'), 81] and n > 0:
            n = n-1
        if order in [ord('n'), 83] and n < (len(the_files)-1):
            n = n+1

def extract_patch_process():
    print('- extracting patch of tagged images')
    for n in [80]: # TODO: 100 est temporaire pour tester 
        fn = get_nth_file_path(n)
        print('--- analysing file ' + str(n) + ' : ' + fn)
        json_file = ll.tag_file(fn)
        if os.path.isfile(json_file):
            the_tags = read_tags(fn)
            extract_patch.extract_patch(fn, the_tags)
        else:
            print('no tag data for ' + fn)

def main():
    global the_files
    print('usage:')
    print('- starting tagging:')
    print('> ' + sys.argv[0] + ' <data_dir> <tag_dir> [special command]')
    print('  (a) selecting adventices')
    print('  (z) selecting plants')
    print('  (e) selecting unknown plant')
    print('  (u) undo')
    print('  (c) clear')
    print('  (s) save tags (they are saved automatically by jumping from image to image')
    print('  (n) next image')
    print('  (p) previous image')
    print('  special command is optional:')
    print('     - \'extract-patch\' for extracting patch')
    print('')
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        return

    if len(sys.argv) < 3:
        return

    special_command = None
    if len(sys.argv) >= 4:
        special_command = sys.argv[3]

    ll.data_dir = sys.argv[1]
    if not os.path.exists(ll.data_dir):
        print('Error: data directory does not exists ('+sys.argv[1]+'))')
        return
    ll.tag_dir = sys.argv[2]
    if not os.path.exists(ll.tag_dir):
        os.system('mkdir ' + ll.tag_dir + ' 2>/dev/null')
        print('tag directory created: ' + ll.tag_dir)

    print('- processing all JPG files in ' + ll.data_dir)
    the_files = ll.file_list(ll.data_dir)

    if special_command is None:
        tag_process()

    if special_command == 'extract-patch':
        extract_patch_process()

main()
