import os
import re
import cv2

data_dir = '../data'
tag_dir = '../data/tags'

img_size = (1024, 768)

CLASSES = {'plant': 0, 'adventice': 1, 'unknown': 2}
colors = {'plant': (0, 255, 0), 'adventice': (0, 0, 255), 'unknown':(0,200,255) }

file_format = re.compile(r'(.*lavandin.*)/([^/]+)\.JPG$')


def file_list(d):
    print('- current directory: %s' % os.getcwd())
    print('- collecting files of ' + d)
    all_files = os.popen('find -L ' + d).readlines()
    all_files = list(map(lambda l:l[0:-1], all_files))
    the_files = []
    for f in all_files:
        m = file_format.match(f)
        if m:
            dir = m.group(1)
            file = m.group(2) + '.JPG'
            the_files.append((dir, file))
    the_files = list(sorted(the_files))
    print('  [%d files ]' % len(the_files))
    return the_files


def get_file_name(fn):
    m = file_format.match(fn)
    if not m:
        print('Error: unable to get the file name from ' + fn)
    return m.group(2) + '.JPG'


def tag_file(fn):
    m = file_format.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(2)
    return tag_dir + '/' + root + '.json'

def roi_file(fn, n):
    m = file_format.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(2)
    return tag_dir + '/' + root + '-roi-' + str(n) + '.jpg'

def roi_hsv_file(fn, n):
    m = file_format.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(2)
    return tag_dir + '/' + root + '-roi-HSV-' + str(n) + '.jpg'

def tag_file_yolo(fn):
    m = file_format.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(2)
    return tag_dir + '/' + root + '.txt'


def tag_img_file(fn):
    m = file_format.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(2)
    return tag_dir + '/' + root + '-TAG.JPG'

def relative_pos(img_size, pos):
    x = pos[0]/img_size[0]
    y = pos[1]/img_size[1]
    if x < 0:
        x = 0
    if x > 1:
        x = 1
    if y < 0:
        y = 0
    if y > 1:
        y = 1
    return (x, y)


def graphic_pos(img_size, pos):
    return (int(pos[0]*img_size[0]), int(pos[1]*img_size[1]))

def draw_tag(img, tag):

    A = graphic_pos(img_size, tag[1])
    B = graphic_pos(img_size, tag[2])
    cv2.rectangle(img, A, B, colors[tag[0]], 2)

def cut_patch(img, x1, y1, x2, y2) :

    if (x1 > x2) :
        i = x1
        x1 = x2
        x2 = i
    
    if(y1 > y2) :
        j = y1
        y1 = y2
        y2 = j

    image_coupee = img[y1:y2, x1:x2]

    return image_coupee