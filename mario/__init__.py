#!/usr/bin/env python

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import time
import logging
from scene import Scene
from block import Block
from mario import Mario

LOG = logging.getLogger(__name__)

class SceneWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SceneWidget, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.next_animation_frame)
        self.timer.start(50)
        self.start_time = time.time()
        self.frame_no = 0
        self.antialiased = True

        # create scene and mario
        self.scene = Scene()

        mario = Mario(self.scene, [0.0, -100])

        block = Block(self.scene, Block.block_1, [-1000, 0], [2000, 16])
        self.scene.items.append(block)

        block = Block(self.scene, Block.block_5, [-1000, -300], [2000, 32])
        self.scene.items.append(block)

        block = Block(self.scene, Block.block_5, [-128, -32], [80, 32])
        self.scene.items.append(block)

        block = Block(self.scene, Block.block_5, [0, -128], [80, 32])
        self.scene.items.append(block)

        self.scene.items.append(mario)

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

    def next_animation_frame(self):
        self.frame_no += 1
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(
            QtGui.QPainter.Antialiasing,
            False)

        painter.setPen(Qt.blue)
        painter.setFont(QtGui.QFont("Arial", 30))
        painter.drawText(0, 30, "frame:%d time:%3.3f" % (
            self.frame_no, time.time() - self.start_time))
        painter.translate(self.width() / 2, self.height() / 2)
        self.scene.update(painter)

    def keyPressEvent(self, event):
        self.scene.key_map[event.key()] = 1

    def keyReleaseEvent(self, event):
        self.scene.key_map[event.key()] = 0


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SceneWidget()
    window.show()
    sys.exit(app.exec_())
