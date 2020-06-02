from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
import math


class Grid:
    selected_size = 6
    not_selected_size = 4

    selected_brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 150))

    pen = QtGui.QPen(Qt.SolidLine)
    pen.setColor(Qt.red)
    pen.setCosmetic(True)
    pen.setWidth(not_selected_size)

    selector_brush = QtGui.QBrush(Qt.blue, Qt.SolidPattern)

    ide_state = 0
    move_state = 1
    move_top_left = 2
    move_top_right = 3
    move_bottom_left = 4
    move_bottom_right = 5

    selector_size = 15

    font_pen = QtGui.QPen(Qt.black)
    font = QtGui.QFont("Times", 24, QtGui.QFont.Bold)

    def __init__(self, view):
        self.view = view
        self.rect = QtCore.QRectF(0., 0., 32., 32.)
        self.state = self.ide_state
        self.rows = 3
        self.columns = 3
        self.colums_offset = 0
        self.rows_offset = 0
        self.selected = 1
        self.show_grid = 1
        self.selector_offsets = None
        self.show_selector = 1
        self.show_names = 1
        self.names = [
            [0, 0, "1"],
            [2, 1, "Hi"]
        ]
        self.selected_cell = None

    def set_rows(self, rows):
        if rows >= 1 and rows != self.rows:
            self.rows = rows
            self.view.update()

    def set_columns(self, columns):
        if columns >= 1 and columns != self.columns:
            self.columns = columns
            self.view.update()

    def set_colums_offset(self, offset):
        if offset != self.colums_offset:
            self.colums_offset = offset
            self.view.update()

    def set_rows_offset(self, offset):
        if offset != self.rows_offset:
            self.rows_offset = offset
            self.view.update()

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
            painter.drawRect(rect)

    def draw_grid(self, painter):
        painter.setBrush(Qt.NoBrush)
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
                painter.drawLine(
                    QtCore.QPointF(s_x, y),
                    QtCore.QPointF(e_x, y))
                painter.drawLine(
                    QtCore.QPointF(s_x, y_2),
                    QtCore.QPointF(e_x, y_2))
        else:
            for i in range(1, self.rows + 1):
                y = s_y + i * height
                painter.drawLine(
                    QtCore.QPointF(s_x, y),
                    QtCore.QPointF(e_x, y))

        # show colls
        width = self.rect.width() / self.columns
        if self.colums_offset:
            for i in range(1, self.columns + 1):
                x = s_x + i * width
                x_2 = x - self.colums_offset
                painter.drawLine(
                    QtCore.QPointF(x, s_y),
                    QtCore.QPointF(x, e_y))
                painter.drawLine(
                    QtCore.QPointF(x_2, s_y),
                    QtCore.QPointF(x_2, e_y))
        else:
            for i in range(1, self.columns + 1):
                x = s_x + i * width
                painter.drawLine(
                    QtCore.QPointF(x, s_y),
                    QtCore.QPointF(x, e_y))

    def draw_names(self, painter):
        points = []

        top_left = self.rect.topLeft()
        col_step = self.rect.width() / self.columns
        width = col_step - self.colums_offset

        row_step = self.rect.height() / self.rows
        height = row_step - self.rows_offset

        for row, col, text in self.names:
            if row >= 0 and row < self.rows and\
                    col >= 0 and col < self.columns:
                points.append((
                    painter.transform().mapRect(
                        QtCore.QRectF(
                            top_left.x() + col * col_step,
                            top_left.y() + row * row_step,
                            width,
                            height)), text))

        # draw selected cell
        if self.selected_cell is not None:
            painter.setBrush(self.selected_brush)
            painter.setPen(Qt.NoPen)
            painter.drawRect(
                QtCore.QRectF(
                    top_left + QtCore.QPointF(
                        col_step * self.selected_cell[0],
                        row_step * self.selected_cell[1],
                    ),
                    QtCore.QSizeF(width, height)
                )
            )

        # reset transform
        painter.save()
        painter.setWorldTransform(QtGui.QTransform())
        painter.setFont(self.font)
        painter.setPen(self.font_pen)

        for rect, text in points:
            painter.drawText(rect, text)
        painter.restore()

    def update(self, painter):
        painter.setBrush(Qt.NoBrush)
        self.pen.setWidth(
            self.selected_size if self.selected else self.not_selected_size)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

        if self.show_grid:
            self.draw_grid(painter)

        if self.show_names:
            self.draw_names(painter)

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
                            # move all
                            else:
                                self.state = self.move_state
                                self.start_move_pos = pos
                                self.top_left = self.rect.topLeft()

                                # get selected cell
                                width = self.rect.width() / self.columns
                                height = self.rect.height() / self.rows
                                pos = pos - self.rect.topLeft()
                                col = math.trunc(pos.x() / width)
                                row = math.trunc(pos.y() / height)
                                self.selected_cell = [col, row]
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

