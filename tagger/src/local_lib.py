import os
import re

data_dir = "../data/initial"
file_format = re.compile(r'(.*)/([^/]+\.JPG)$')
brut_file = re.compile(r'(.*).JPG$')

def file_list(d):
    print('- collecting files of ' + d)
    all_files = os.popen('find ' + d).readlines()
    all_files = list(map(lambda l:l[0:-1], all_files))
    the_files = []
    for f in all_files:
        m = file_format.match(f)
        if m:
            dir = m.group(1)
            file = m.group(2)
            the_files.append((dir,file))
    the_files = list(sorted(the_files))
    return the_files


def tag_file(fn):
    m = brut_file.match(fn)
    if not m:
        print('Error: ' + fn + ' is not a picture file')
        return None
    root = m.group(1)
    return root + '.json'
    
