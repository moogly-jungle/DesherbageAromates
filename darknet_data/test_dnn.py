#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
#  File Name	: test_dnn.py
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

import cv2
import time
import sys
import numpy as np

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
class_names = ['plant', 'adventice', 'unknown']
# class_names = open('coco.names').read().strip().split('\n')


if len(sys.argv) < 4:
    print("USAGE: {} IMAGE WEIGHT CFG".format(sys.argv[0]))
    exit(-1)
# vc = cv2.VideoCapture("demo.mp4")
frame = cv2.imread(sys.argv[1])
frame = cv2.resize(frame, (1024, 768))
net = cv2.dnn.readNet(sys.argv[2], sys.argv[3])

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
print(model.getLayerNames())
model.setInputParams(size=(416, 416), scale=1/255)


classes, scores, boxes = model.detect(
    frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
print(classes)
for (classid, score, box) in zip(classes, scores, boxes):
    color = COLORS[int(classid) % len(COLORS)]
    label = "%s : %f" % (class_names[classid[0]], score)
    cv2.rectangle(frame, box, color, 2)
    cv2.putText(frame, label, (box[0], box[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imshow("detections", frame)
cv2.waitKey()
cv2.destroyAllWindows()
