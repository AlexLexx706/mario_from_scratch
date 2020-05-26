from PyQt5 import QtCore
import math


class Shape:
    def __init__(self, scene, pos, size):
        self.pos = pos
        self.size = size
        self.speed = [0, 0]
        self.scene = scene
        self.x_intersection = 0
        self.y_intersection = 0
        self.landing_flag = False

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

    def collision(self, shape, update_x):
        center = self.center()
        shape_center = shape.center()
        x = center[0] - shape_center[0]
        y = center[1] - shape_center[1]
        fabs_x = math.fabs(x)
        fabs_y = math.fabs(y)

        width = (self.size[0] + shape.size[0]) / 2.
        height = (self.size[1] + shape.size[1]) / 2.

        # collision detected
        if fabs_x < width and fabs_y < height:
            if update_x:
                shape.x_intersection = 1. if x > 0. else -1.
                offset_x = shape.x_intersection * (width - fabs_x)
                self.pos[0] += offset_x
                self.speed[0] = 0.
            else:
                shape.y_intersection = (1. if y > 0. else -1.)
                offset_y = shape.y_intersection * (height - fabs_y)
                self.pos[1] += offset_y
                self.speed[1] = 0.

                if shape.y_intersection == -1.:
                    self.landing_flag = True
