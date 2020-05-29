#!/usr/bin/env python
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import time
import logging
import sys


LOG = logging.getLogger(__name__)


class TilesView(QtWidgets.QWidget):
    class Camera:
        ide_state = 0
        move_state = 1

        def __init__(self):
            self.pos = QtCore.QPointF(0., 0.)
            self.scale = 10.
            self.state = self.ide_state
            self.start_pos = QtCore.QPoint()
            self.offset = QtCore.QPointF()

        def move(self, pos):
            if self.state == self.move_state:
                offset = (pos - self.start_pos)
                self.offset.setX(offset.x())
                self.offset.setY(offset.y())
                return 1

        def get_pos(self):
            return self.pos + self.offset

        def start_move(self, pos):
            self.start_pos = pos
            self.state = self.move_state

        def stop_move(self):
            if self.state == self.move_state:
                self.pos = self.get_pos()
                self.offset = QtCore.QPointF()
                self.state = self.ide_state

        def update_scale(self, pos):
            self.scale += pos.y() * 0.01

    class Grid:
        brush = QtGui.QBrush(Qt.NoBrush)
        pen = QtGui.QPen(Qt.SolidLine)
        pen.setColor(Qt.red)
        pen.setCosmetic(True)
        pen.setWidth(2)

        ide_state = 0
        move_state = 1

        def __init__(self, scene):
            self.scene = scene
            self.rect = QtCore.QRect(0, 0, 32, 32)
            self.offset = QtCore.QPointF()
            self.size = [0, 0]
            self.state = self.ide_state

        def update(self, painter):
            painter.setBrush(self.brush)
            painter.setPen(self.pen)
            painter.drawRect(self.rect)

        def start_move(self, pos):
            self.state = self.move_state
            self.offset_start_pos = pos
            self.top_left = self.rect.topLeft()

        def stop_move(self, pos):
            if self.state == self.move_state:
                self.state = self.ide_state

        def move(self, pos):
            if self.state == self.move_state:
                self.rect.moveTopLeft(
                    self.top_left + (
                        pos - self.offset_start_pos) / self.scene.camera.scale)
                return 1

    def __init__(self, parent=None):
        super(TilesView, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        file_path = os.path.join(
            os.path.split(__file__)[0], '../images/tiles.png')
        self.pixmap = QtGui.QPixmap(file_path)
        self.key_map = {}
        self.camera = self.Camera()
        self.grid = self.Grid(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.translate(self.camera.get_pos())
        painter.scale(self.camera.scale, self.camera.scale)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPixmap(QtCore.QPointF(), self.pixmap)

        # drow grid
        self.grid.update(painter)

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self.key_map[event.key()] = 1
        event.accept()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.key_map[event.key()] = 0

        if event.key() == Qt.Key_Shift:
            self.camera.stop_move()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.key_map.get(Qt.Key_Shift, 0):
                self.camera.start_move(event.pos())
            else:
                self.grid.start_move(event.pos())
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.key_map.get(Qt.Key_Shift, 0):
                self.camera.stop_move()
            else:
                self.grid.stop_move(event.pos())
        event.accept()

    def mouseMoveEvent(self, event):
        update = False

        if self.camera.move(event.pos()):
            update = True

        if self.grid.move(event.pos()):
            update = True

        if update:
            self.update()

        event.accept()

    def wheelEvent(self, event):
        if self.key_map.get(Qt.Key_Shift, 0):
            self.camera.update_scale(event.pixelDelta())
            self.update()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TilesView()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
