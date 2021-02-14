#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
#  File Name	: split_data.py
#  Author	: Steve NGUYEN
#  Contact      : steve.nguyen.000@gmail.com
#  Created	: dimanche, février  7 2021
#  Revised	:
#  Version	:
#  Target MCU	:
#
#  This code is distributed under the GNU Public License
# 		which can be found at http://www.gnu.org/licenses/gpl.txt
#
#
#  Notes:	notes
#

import sys
import glob
import os
import random
import numpy as np


OUTDIR = 'data/obj/'

if __name__ == '__main__':

    flist = glob.glob(sys.argv[1]+'/*.txt')
    fnamelist = []
    for f in flist:
        fnamelist.append(os.path.basename(f))
    print(fnamelist)

    random.shuffle(fnamelist)
    print(fnamelist)
    train, test = np.split(
        fnamelist, [int(len(fnamelist)*0.9)])

    print(len(fnamelist))
    print(len(train))
    print(len(test))

    with open('train.txt', 'w') as trainfile:
        for t in train:
            trainfile.write(OUTDIR+t.replace('txt', 'JPG')+'\n')

    with open('test.txt', 'w') as testfile:
        for t in test:
            testfile.write(OUTDIR+t.replace('txt', 'JPG')+'\n')
