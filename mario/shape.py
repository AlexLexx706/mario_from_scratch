from PyQt5 import QtCore
import math


class Shape:
    def __init__(self, scene, pos, size):
        self.pos = pos
        self.size = size
        self.scene = scene

    def update(self, painter):
        pass

    def rect(self):
        return QtCore.QRectF(
            self.pos[0], self.pos[1],
            self.size[0], self.size[1])

    def center(self):
        return [
            self.pos[0] + self.size[0] / 2.,
            self.pos[1] + self.size[1] / 2.]

    def move(self, pos):
        self.pos = [
            pos[0] + self.pos[0],
            pos[1] + self.pos[1]]

    def is_intersected(self, shape):
        if (self.pos[0] < shape.pos[0] + shape.size[0]) and\
                (self.pos[0] + self.size[0] > shape.pos[0]) and\
                (self.pos[1] < shape.pos[1] + shape.size[1]) and\
                (self.pos[1] + self.size[1] > shape.pos[1]):
            return True
        return False

    def get_offset(self, shape):
        center = self.center()
        s_center = shape.center()
        x = center[0] - s_center[0]
        y = center[1] - s_center[1]

        f_x = math.fabs(x)
        f_y = math.fabs(y)

        offset = [
            (1. if x > 0 else -1) * ((self.size[0] + shape.size[0]) / 2. - f_x),
            (1. if y > 0 else -1.) * ((self.size[1] + shape.size[1]) / 2. - f_y)
        ]

        if math.fabs(offset[0]) < math.fabs(offset[1]):
            offset[1] = 0.
        else:
            offset[0] = 0.
        return offset
