#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
#  File Name	: yolo.py
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


# YOLO object detection
import cv2 as cv
import numpy as np
import time
import sys
WHITE = (255, 255, 255)
img = None
img0 = None
outputs = None


colors = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

classes = ['plant', 'adventice', 'unknown']


# classes = open('coco.names').read().strip().split('\n')
# np.random.seed(42)
# colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')


print(cv.__version__)
if len(sys.argv) < 4:
    print("USAGE: {} CFG WEIGHT IMAGE".format(sys.argv[0]))
    exit(-1)

# Give the configuration and weight files for the model and load the network.
net = cv.dnn.readNetFromDarknet(sys.argv[1], sys.argv[2])
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# determine the output layer
ln = net.getLayerNames()
print(len(ln), ln)
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def load_image(path):
    global img, img0, outputs, ln

    img0 = cv.imread(path)
    img0 = cv.resize(img0, (1024, 768))
    img = img0.copy()

    blob = cv.dnn.blobFromImage(
        img, 1/255.0, (608, 608), swapRB=True, crop=False)

    net.setInput(blob)
    # t0 = time.time()
    outputs = net.forward(ln)
    # t = time.time() - t0

    # combine the 3 output groups into 1 (10647, 85)
    # large objects (507, 85)
    # medium objects (2028, 85)
    # small objects (8112, 85)
    outputs = np.vstack(outputs)

    post_process(img, outputs, 0.5)
    cv.imshow('window',  img)
    # cv.displayOverlay('window', f'forward propagation time={t:.3}')
    cv.waitKey(0)


def post_process(img, outputs, conf):
    H, W = img.shape[:2]

    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        scores = output[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w//2), int(y - h//2)
            p1 = int(x + w//2), int(y + h//2)
            boxes.append([*p0, int(w), int(h)])
            confidences.append(float(confidence))
            classIDs.append(classID)
            cv.rectangle(img, p0, p1, WHITE, 1)

    indices = cv.dnn.NMSBoxes(boxes, confidences, conf, conf-0.1)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in colors[classIDs[i]]]
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
            cv.putText(img, text, (x, y - 5),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def trackbar(x):
    global img
    conf = x/100
    img = img0.copy()
    post_process(img, outputs, conf)
    # cv.displayOverlay('window', f'confidence level={conf}')
    # cv.putText(img, f'confidence level={conf}', (50, 50),
    #            cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv.imshow('window', img)


cv.namedWindow('window')
cv.createTrackbar('confidence', 'window', 50, 100, trackbar)
load_image(sys.argv[3])

cv.destroyAllWindows()
