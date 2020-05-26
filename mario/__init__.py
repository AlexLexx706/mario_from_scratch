#!/usr/bin/env python

from PyQt5 import QtGui, QtCore, QtWidgets
# from PyQt5 import QtOpenGL
from PyQt5.QtCore import Qt
import time
import logging
from mario.scene import Scene
from mario.block import Block
from mario.mario import Mario
from mario.secret_block import SecretBlock
import sys


LOG = logging.getLogger(__name__)


# class SceneWidget(QtOpenGL.QGLWidget):
class SceneWidget(QtWidgets.QWidget):
    text_font = QtGui.QFont("Arial", 30)

    def __init__(self, parent=None):
        super(SceneWidget, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.next_animation_frame)
        self.timer.start(50)
        # self.timer.start(1000)
        self.start_time = time.time()
        self.frame_no = 0
        self.antialiased = True

        # create scene and mario
        self.scene = Scene()
        mario = Mario(self.scene, [0.0, 0.0])

        block = Block(self.scene, Block.block_4, [0, 224], [256, 16])
        self.scene.items.append(block)

        # block = Block(self.scene, Block.block_5, [-1000, -300], [2000, 32])
        # self.scene.items.append(block)

        # block = Block(self.scene, Block.block_5, [-128, -32], [65, 32])
        # self.scene.items.append(block)

        # block = Block(self.scene, Block.block_5, [0, -128], [65, 32])
        # self.scene.items.append(block)

        block = SecretBlock(self.scene, [100, 160])
        self.scene.items.append(block)

        block = SecretBlock(self.scene, [116, 128])
        self.scene.items.append(block)

        block = SecretBlock(self.scene, [148, 128])
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
        painter.setFont(self.text_font)
        painter.drawText(0, 30, "frame:%d time:%3.3f" % (
            self.frame_no, time.time() - self.start_time))
        painter.setWindow(QtCore.QRect(0, 0, 256, 240))
        painter.setViewport(QtCore.QRect(0, 0, 256 * 4, 240 * 4))
        # painter.translate(self.width() / 2, self.height() / 2)
        self.scene.update(painter)

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self.scene.key_map[event.key()] = 1

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.scene.key_map[event.key()] = 0


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SceneWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
