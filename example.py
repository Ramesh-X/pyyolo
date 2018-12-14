"""
    File name: example.py
    Author: rameshpr
    Date: 10/29/18
"""
import cv2
import numpy as np
import pyyolo

meta_filepath = "./coco.data"
cfg_filepath = "./yolo.cfg"
weights_filepath = "./yolov3.weights"

image_filepath = './image.jpg'

meta = pyyolo.load_meta(meta_filepath)
net = pyyolo.load_net(cfg_filepath, weights_filepath, False)

im = cv2.imread(image_filepath)
yolo_img = pyyolo.array_to_image(im)
res = pyyolo.detect(net, meta, yolo_img)
colors = np.random.rand(meta.classes, 3) * 255

for r in res:
    cv2.rectangle(im, r.bbox.get_point(pyyolo.BBox.Location.TOP_LEFT, is_int=True),
                  r.bbox.get_point(pyyolo.BBox.Location.BOTTOM_RIGHT, is_int=True), tuple(colors[r.id].tolist()), 2)

cv2.imshow('Frame', im)
cv2.waitKey(0)

