from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
import math


class Grid:
    selected_size = 4
    not_selected_size = 2

    brush = QtGui.QBrush(Qt.NoBrush)

    pen = QtGui.QPen(Qt.SolidLine)
    pen.setColor(Qt.red)
    pen.setCosmetic(True)
    pen.setWidth(not_selected_size)

    pen_blue = QtGui.QPen(Qt.SolidLine)
    pen_blue.setColor(Qt.blue)
    pen_blue.setCosmetic(True)
    pen_blue.setWidth(2)

    selector_brush = QtGui.QBrush(Qt.blue, Qt.SolidPattern)

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
        self.rows = 3
        self.columns = 3
        self.columns_offset = 0
        self.rows_offset = 0
        self.selected = 1
        self.show_grid = 1
        self.selector_offsets = None
        self.show_selector = 1

    def set_rows(self, rows):
        self.rows = rows

    def set_columns(self, columns):
        self.columns = columns

    def set_columns_offset(self, offset):
        self.columns_offset = offset

    def set_rows_offset(self, offset):
        self.rows_offset = offset

    def draw_selecter(self, painter):
        painter.setBrush(self.selector_brush)
        painter.setPen(Qt.NoPen)
        pos = None
        if self.state == self.move_top_left:
            pos = self.rect.topLeft()
        elif self.state == self.move_top_right:
            pos = self.rect.topRight() - QtCore.QPointF(
                self.selector_offsets.x(), 0)
        elif self.state == self.move_bottom_left:
            pos = self.rect.bottomLeft() - QtCore.QPointF(
                0., self.selector_offsets.y())
        elif self.state == self.move_bottom_right:
            pos = self.rect.bottomRight() - QtCore.QPointF(
                self.selector_offsets.x(), self.selector_offsets.y())
        if pos is not None:
            rect = QtCore.QRectF(
                pos.x(),
                pos.y(),
                self.selector_offsets.x(),
                self.selector_offsets.y())
            print(rect)
            painter.drawRect(rect)

    def draw_grid(self, painter):
        painter.setBrush(self.brush)
        self.pen.setWidth(self.not_selected_size)
        painter.setPen(self.pen)

        s_x = self.rect.x()
        s_y = self.rect.y()

        bottom_right = self.rect.bottomRight()
        e_x = bottom_right.x()
        e_y = bottom_right.y()

        # show rows
        height = self.rect.height() / self.rows
        if self.rows_offset:
            for i in range(1, self.rows + 1):
                y = s_y + i * height
                y_2 = y - self.rows_offset
                painter.drawLine(s_x, y, e_x, y)
                painter.drawLine(s_x, y_2, e_x, y_2)
        else:
            for i in range(1, self.rows + 1):
                y = s_y + i * height
                painter.drawLine(s_x, y, e_x, y)

        # show colls
        width = self.rect.width() / self.columns
        if self.columns_offset:
            for i in range(1, self.columns + 1):
                x = s_x + i * width
                x_2 = x - self.columns_offset
                painter.drawLine(x, s_y, x, e_y)
                painter.drawLine(x_2, s_y, x_2, e_y)
        else:
            for i in range(1, self.columns + 1):
                x = s_x + i * width
                painter.drawLine(x, s_y, x, e_y)

    def update(self, painter):
        painter.setBrush(self.brush)
        self.pen.setWidth(
            self.selected_size if self.selected else self.not_selected_size)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

        if self.show_grid:
            self.draw_grid(painter)

        if self.show_selector:
            self.draw_selecter(painter)

    def start_move(self, pos):
        try:
            if self.rect.contains(pos):
                top_left = self.rect.topLeft()
                # 1. calculate offset for choose borders
                self.selector_offsets = self.view.camera.to_scene(
                    self.view.camera.to_view(top_left) +
                    QtCore.QPointF(
                        self.selector_size,
                        self.selector_size)) - top_left

                top_left_rect = QtCore.QRectF(
                    top_left.x(),
                    top_left.y(),
                    self.selector_offsets.x(),
                    self.selector_offsets.y())
                if top_left_rect.contains(pos):
                    self.state = self.move_top_left
                    self.start_move_pos = pos
                    self.top_left = self.rect.topLeft()
                    return 1
                else:
                    top_right = self.rect.topRight()
                    top_right_rect = QtCore.QRectF(
                        top_right.x() - self.selector_offsets.x(),
                        top_left.y(),
                        self.selector_offsets.x(),
                        self.selector_offsets.y())

                    if top_right_rect.contains(pos):
                        self.state = self.move_top_right
                        self.start_move_pos = pos
                        self.top_right = self.rect.topRight()
                        return 1
                    else:
                        bottom_left = self.rect.bottomLeft()
                        bottom_left_rect = QtCore.QRectF(
                            bottom_left.x(),
                            bottom_left.y() - self.selector_offsets.x(),
                            self.selector_offsets.x(),
                            self.selector_offsets.y())

                        if bottom_left_rect.contains(pos):
                            self.state = self.move_bottom_left
                            self.start_move_pos = pos
                            self.bottom_left = self.rect.bottomLeft()
                            return 1
                        else:
                            bottom_right = self.rect.bottomRight()
                            bottom_right_rect = QtCore.QRectF(
                                bottom_right.x() - self.selector_offsets.x(),
                                bottom_right.y() - self.selector_offsets.x(),
                                self.selector_offsets.x(),
                                self.selector_offsets.y())

                            if bottom_right_rect.contains(pos):
                                self.state = self.move_bottom_right
                                self.start_move_pos = pos
                                self.bottom_right = self.rect.bottomRight()
                                return 1
                            else:
                                self.state = self.move_state
                                self.start_move_pos = pos
                                self.top_left = self.rect.topLeft()
                                return 1
        finally:
            self.view.update()

    def set_selected(self, selected):
        self.selected = selected
        self.view.update()

    def stop_move(self):
        self.state = self.ide_state
        self.selector_offsets = None
        self.rect = self.rect.normalized()
        self.view.update()


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

