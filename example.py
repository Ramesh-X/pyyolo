"""
    File name: example.py
    Author: rameshpr
    Date: 10/29/18
"""
import cv2
import pyyolo


meta = pyyolo.load_meta("/home/rameshpr/Downloads/darknet_google_server/data/obj.data")
net = pyyolo.load_net("/home/rameshpr/Downloads/darknet_google_server/cfg/yolo-lb.cfg",
                      "/home/rameshpr/Downloads/darknet_google_server/backup/yolo-v3.weights", 0)

im = cv2.imread('./image.jpg')
yolo_img = pyyolo.array_to_image(im)
res = pyyolo.detect(net, meta, yolo_img)

for r in res:
    cv2.rectangle(im, r.bbox.get_point(pyyolo.BBox.Location.TOP_LEFT, True),
                  r.bbox.get_point(pyyolo.BBox.Location.BOTTOM_RIGHT, True), (0, 255, 0), 2)

cv2.imshow('Frame', im)
cv2.waitKey(0)

