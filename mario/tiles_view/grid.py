from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
import math


class Grid:
    brush = QtGui.QBrush(Qt.NoBrush)
    pen = QtGui.QPen(Qt.SolidLine)
    pen.setColor(Qt.red)
    pen.setCosmetic(True)
    pen.setWidth(2)

    ide_state = 0
    move_state = 1
    move_top_left = 2
    move_top_right = 3
    move_bottom_left = 4
    move_bottom_right = 5

    selector_size = 10

    def __init__(self, view):
        self.view = view
        self.rect = QtCore.QRectF(0., 0., 32., 32.)
        self.state = self.ide_state

    def update(self, painter):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

    def start_move(self, pos):

        top_left = self.rect.topLeft()
        # 1. calculate offset for choose borders
        offsets = self.view.camera.to_scene(
            self.view.camera.to_view(top_left) +
            QtCore.QPointF(self.selector_size, self.selector_size)) - top_left

        if self.rect.contains(pos):
            top_left_rect = QtCore.QRectF(
                top_left.x(),
                top_left.y(),
                offsets.x(),
                offsets.y())

            if top_left_rect.contains(pos):
                self.state = self.move_top_left
                self.start_move_pos = pos
                self.top_left = self.rect.topLeft()
            else:
                top_right = self.rect.topRight()
                top_right_rect = QtCore.QRectF(
                    top_right.x() - offsets.x(),
                    top_left.y(),
                    offsets.x(),
                    offsets.y())

                if top_right_rect.contains(pos):
                    self.state = self.move_top_right
                    self.start_move_pos = pos
                    self.top_right = self.rect.topRight()
                else:
                    bottom_left = self.rect.bottomLeft()
                    bottom_left_rect = QtCore.QRectF(
                        bottom_left.x(),
                        bottom_left.y() - offsets.x(),
                        offsets.x(),
                        offsets.y())

                    if bottom_left_rect.contains(pos):
                        self.state = self.move_bottom_left
                        self.start_move_pos = pos
                        self.bottom_left = self.rect.bottomLeft()
                    else:
                        bottom_right = self.rect.bottomRight()
                        bottom_right_rect = QtCore.QRectF(
                            bottom_right.x() - offsets.x(),
                            bottom_right.y() - offsets.x(),
                            offsets.x(),
                            offsets.y())

                        if bottom_right_rect.contains(pos):
                            self.state = self.move_bottom_right
                            self.start_move_pos = pos
                            self.bottom_right = self.rect.bottomRight()
                        else:
                            print("all")
                            self.state = self.move_state
                            self.start_move_pos = pos
                            self.top_left = self.rect.topLeft()

    def stop_move(self):
        if self.state == self.move_state:
            self.state = self.ide_state

    def move(self, pos):
        if self.state == self.move_state:
            new_pos = self.top_left + pos - self.start_move_pos
            new_pos = QtCore.QPointF(
                math.trunc(new_pos.x()),
                math.trunc(new_pos.y()))
            self.rect.moveTopLeft(new_pos)
            return 1
        elif self.state == self.move_top_left:
            new_pos = self.top_left + pos - self.start_move_pos
            new_pos = QtCore.QPointF(
                math.trunc(new_pos.x()),
                math.trunc(new_pos.y()))
            self.rect.setTopLeft(new_pos)
            return 1
        elif self.state == self.move_top_right:
            new_pos = self.top_right + pos - self.start_move_pos
            new_pos = QtCore.QPointF(
                math.trunc(new_pos.x()),
                math.trunc(new_pos.y()))
            self.rect.setTopRight(new_pos)
            return 1
        elif self.state == self.move_bottom_left:
            new_pos = self.bottom_left + pos - self.start_move_pos
            new_pos = QtCore.QPointF(
                math.trunc(new_pos.x()),
                math.trunc(new_pos.y()))
            self.rect.setBottomLeft(new_pos)
            return 1
        elif self.state == self.move_bottom_right:
            new_pos = self.bottom_right + pos - self.start_move_pos
            new_pos = QtCore.QPointF(
                math.trunc(new_pos.x()),
                math.trunc(new_pos.y()))
            self.rect.setBottomRight(new_pos)
            return 1

