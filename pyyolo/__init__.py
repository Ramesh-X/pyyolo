import numpy as np
from ctypes import *

import cv2
from darknet import c_array, IMAGE, predict_image, get_network_boxes, \
    do_nms_obj, do_nms_sort, free_image, free_detections
import darknet

__version__ = '1.0'


def load_image(filename, flags=None):
    """
    This will call cv2.imread() with the given arguments and convert
    the resulting numpy array to a darknet image

    :param filename: Image file name
    :param flags: imread flags
    :return: Given image file as a darknet image
    :rtype: IMAGE
    """
    image = cv2.imread(filename, flags)
    return array_to_image(image)


def array_to_image(arr):
    """
    Given image with numpy array will be converted to
    darkent image

    :rtype: IMAGE
    :param arr: numpy array
    :return: darknet image
    """
    c = arr.shape[2]
    h = arr.shape[0]
    w = arr.shape[1]
    arr = np.flip(arr.reshape((-1, 3)).transpose(), 0).flatten() / 255.0
    data = c_array(c_float, arr)
    im = IMAGE(w, h, c, data)
    return im


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, im, thresh=.2, hier_thresh=0, nms=.4):
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if nms:
        do_nms_sort(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_detections(dets, num)
    return res


def load_net(cfg_filepath, weights_filepath, clear):
    """

    :param cfg_filepath: cfg file name
    :param weights_filepath: weights file name
    :param clear: 1 if you want to clear the weights otherwise 0
    :return: darknet network object
    """
    return darknet.load_net(cfg_filepath, weights_filepath, clear)


def load_meta(meta_filepath):
    """

    :param meta_filepath: metadata file path
    :return: darknet metadata object
    """
    return darknet.load_meta(meta_filepath)



