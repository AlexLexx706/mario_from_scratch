#!/usr/bin/env python
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import logging
import sys
from . import camera, grid

LOG = logging.getLogger(__name__)


class TilesView(QtWidgets.QWidget):
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
        self.camera = camera.Camera()
        self.grids = []
        self.grids.append(grid.Grid(self))
        self.cur_grid = None
        self.showMaximized()
        self.camera.scale(4)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setTransform(self.camera.transform)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPixmap(QtCore.QPointF(), self.pixmap)

        # drow grid
        for cur_grid in self.grids:
            cur_grid.update(painter)

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
            elif self.key_map.get(Qt.Key_Control, 0):
                for cur_grid in self.grids:
                    if cur_grid.start_move(
                            self.camera.to_scene(event.pos())):
                        self.cur_grid = cur_grid
                        break
                else:
                    print("nooo")
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.camera.stop_move()
            if self.cur_grid:
                self.cur_grid.stop_move()
        event.accept()

    def mouseMoveEvent(self, event):
        update = False

        if self.camera.move(event.pos()):
            update = True

        if self.cur_grid:
            if self.cur_grid.move(self.camera.to_scene(event.pos())):
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
