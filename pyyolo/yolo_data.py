"""
    File name: yolo_data
    Author: rameshpr
    Date: 10/25/18
"""


class BBox(object):
    def __init__(self, x=0, y=0, w=0, h=0, c=0):
        """
        Collect information of a bounding box

        :param x: x co-ordinate of top left corner
        :param y: y co-ordinate of top left corner
        :param w: width
        :param h: height
        :param c: confidence
        """
        self.x = x  # type: float
        self.y = y  # type: float
        self.w = w  # type: float
        self.h = h  # type: float
        self.c = c  # type: float


class YoloData(object):
    def __init__(self, name, bbox):
        self.name = name    # type: str
        self.bbox = bbox    # type: BBox

