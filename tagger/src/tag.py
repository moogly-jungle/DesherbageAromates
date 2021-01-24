import os
import sys
import cv2
import local_lib as ll
import json

# TODO: un clear all tag

the_files = None

def get_nth_file_path(n):
    return the_files[n][0] + '/' + the_files[n][1]

img = None
img_size = (800,800)

def relative_pos(pos):
    x = pos[0]/img_size[0]
    y = pos[1]/img_size[1]
    if x < 0: x = 0
    if x > 1: x = 1
    if y < 0: y = 0
    if y > 1: y = 1
    return (x, y)

def graphic_pos(pos):
    return (int(pos[0]*img_size[0]), int(pos[1]*img_size[1]))

colors = {'plant' : (0,255,0), 'adventice' : (0,0,255) }

typ = 'adventice'
tags = []
refPt = []
cropping = False

def draw_tag(img, tag):
    A = graphic_pos(tag[1])
    B = graphic_pos(tag[2])
    cv2.rectangle(img, A, B, colors[tag[0]], 2)
    
def mouse_handler(event, x, y, flags, param):
    global img, refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        tags.append((typ, relative_pos(refPt[0]), relative_pos(refPt[1])))
        draw_tag(img, tags[-1])
        cv2.imshow('image', img)

def read_tags(fn):
    global tags
    try:
        with open(ll.tag_file(fn)) as json_file:
            tags = json.load(json_file)
    except:
        tags = []
        print('  - no previous tags --')
    
def save_tags(fn):
    with open(ll.tag_file(fn), 'w') as outfile:  
        json.dump(tags, outfile)
    print('  - tags saved in ' + ll.tag_file(fn))
        
def process_file(fn):
    global img, typ, tags
    img = cv2.imread(fn)
    if img.size == 0:
        print("Error: bad file name: " + fn)
        return
    ## TOTO: resize avec proportion
    img = cv2.resize(img,img_size)
    read_tags(fn)
    for t in tags: draw_tag(img, t)
    cv2.namedWindow('image')
    cv2.moveWindow('image', 800,0);        
    cv2.setMouseCallback('image', mouse_handler)
    cv2.imshow("image", img)
    while(True):
        key = cv2.waitKey(0)
        if key in [ord('q'), ord('n'), ord('p'), 83, 81 ]: break
        if key == ord('a'):
            typ = 'adventice'
        if key == ord('z'):
            typ = 'plant'
        if key == ord('s'):
            save_tags(fn)
        redraw = False
        if key == ord('u'): # UNDO
            if len(tags) > 0: tags = tags[0:-1]
            redraw = True
        if key == ord('c'): # UNDO
            tags = []
            redraw = True
        img = cv2.imread(fn)
        img = cv2.resize(img,img_size)
        for t in tags: draw_tag(img, t)
        cv2.imshow("image", img)
    cv2.destroyAllWindows()
    save_tags(fn)
    return key

def main():
    global the_files
    print('usage:')
    print('- starting tagging:')
    print('> ' + sys.argv[0] + ' <data_dir>')
    print('  (a) selecting adventices')
    print('  (z) selecting plants')
    print('  (u) undo')
    print('  (c) clear')
    print('  (s) save tags (they are saved automatically by jumping from image to image')
    print('  (n) next image')
    print('  (p) previous image')
    print('')
    print('- removing all tag files ')
    print('> ' + sys.argv[0] + ' <data_dir> remove_tags')
    print('')
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        return

    if len(sys.argv) < 2:
        if not os.path.exists(ll.data_dir):
            print('Error: I need the data directory (default is "' + ll.data_dir + '"')
            return
    else:
        ll.data_dir = sys.argv[1]
        if not os.path.exists(ll.data_dir):
            print('Error: data directory does not exists ('+sys.argv[1]+'))')
            return

    print('- processing all JPG files in ' + ll.data_dir)
    the_files = ll.file_list(ll.data_dir)

    if len(sys.argv)>1:
        if sys.argv[1]=='remove_tags':
            n = 0
            while n < len(the_files):
                tag_file = ll.tag_file(get_nth_file_path(n))
                if os.path.isfile(tag_file):
                    print('removing ' + tag_file)
                    os.system('rm -f "' + tag_file + '"')
                n = n+1
            return
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
        if order in [ord('p'), 81] and n > 0: n = n-1
        if order in [ord('n'), 83] and n < (len(the_files)-1): n = n+1

main()
