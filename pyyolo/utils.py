"""
    File name: utils
    Author: rameshpr
    Date: 11/5/18
"""

import numpy as np
from ctypes import *
from typing import List, Tuple

import cv2
from darknet import c_array, IMAGE, METADATA, predict_image, get_network_boxes, \
    do_nms_obj, do_nms_sort, free_image, free_detections, ndarray_image
import darknet
from yolo_data import BBox, YoloData


def load_image(filename, flags=None):
    # type: (str, int) -> IMAGE
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
    # type: (np.ndarray) -> IMAGE
    """
    Given image with numpy array will be converted to
    darkent image
    Remember to call free_image(im) function after using this image

    :rtype: IMAGE
    :param arr: numpy array
    :return: darknet image
    """
    data = arr.ctypes.data_as(POINTER(c_ubyte))
    im = ndarray_image(data, arr.ctypes.shape, arr.ctypes.strides)
    return im


def classify(net, meta, im):
    # type: (object, METADATA, IMAGE) -> Tuple[str, float]
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, im, thresh=.2, hier_thresh=0, nms=.4):
    # type: (object, METADATA, IMAGE, float, float, float) -> List[YoloData]
    """
    Detect the objects in the given image. free_image function is called inside this function.
    Therefore the input darkent image is not usable after calling this function.
    :param net:
    :param meta:
    :param im:
    :param thresh:
    :param hier_thresh:
    :param nms:
    :return:
    """
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
                res.append(YoloData(id=i, name=meta.names[i], bbox=BBox(b.x - b.w/2.0, b.y - b.h/2.0, b.w, b.h, dets[j].prob[i])))
    res = sorted(res, key=lambda x: -x.bbox.c)
    free_image(im)
    free_detections(dets, num)
    return res


def load_net(cfg_filepath, weights_filepath, clear):
    # type: (str, str, bool) -> object
    """

    :param cfg_filepath: cfg file name
    :param weights_filepath: weights file name
    :param clear: True if you want to clear the weights otherwise False
    :return: darknet network object
    """
    return darknet.load_net(cfg_filepath, weights_filepath, clear)


def load_meta(meta_filepath):
    # type: (str) -> METADATA
    """

    :param meta_filepath: metadata file path
    :return: darknet metadata object
    """
    return darknet.load_meta(meta_filepath)



