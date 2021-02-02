import os
import re

data_dir = '../data'
tag_dir = '../data/tags'

file_format = re.compile(r'(.*lavandin*)/([^/]+)\.JPG$')


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
