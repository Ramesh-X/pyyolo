"""
    File name: example.py
    Author: rameshpr
    Date: 10/29/18
"""
import cv2
import numpy as np
import pyyolo

meta_filepath = "/home/rameshpr/Downloads/darknet_google_server/data/obj.data"
cfg_filepath = "/home/rameshpr/Downloads/darknet_google_server/cfg/yolo-lb.cfg"
weights_filepath = "/home/rameshpr/Downloads/darknet_google_server/backup/yolo-v3.weights"

video_filepath = './test.mp4'

meta = pyyolo.load_meta(meta_filepath)
net = pyyolo.load_net(cfg_filepath, weights_filepath, False)
cap = cv2.VideoCapture(video_filepath)
colors = np.random.rand(meta.classes, 3) * 255

while True:
    ret, im = cap.read()
    if not ret:
        break
    yolo_img = pyyolo.array_to_image(im)
    res = pyyolo.detect(net, meta, yolo_img)

    for r in res:
        cv2.rectangle(im, r.bbox.get_point(pyyolo.BBox.Location.TOP_LEFT, is_int=True),
                      r.bbox.get_point(pyyolo.BBox.Location.BOTTOM_RIGHT, is_int=True), tuple(colors[r.id].tolist()), 2)
        cv2.putText(im, r.name, r.bbox.get_point(pyyolo.BBox.Location.MID, is_int=True), cv2.FONT_HERSHEY_SIMPLEX, 0.8, tuple(colors[r.id].tolist()))

    cv2.imshow('Frame', im)
    if cv2.waitKey(80) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

