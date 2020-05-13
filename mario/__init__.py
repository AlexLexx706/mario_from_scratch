#!/usr/bin/env python

import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import enum
import time
import logging

LOG = logging.getLogger(__name__)


class Box:
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


class Block(Box):
    block_1 = QtCore.QRect(0, 0, 16, 16)
    block_2 = QtCore.QRect(16, 0, 16, 16)

    def __init__(self, scene, src_rect, pos, size):
        super().__init__(scene, pos, size)

        # create brush if not exist
        src_rect_hash = str(src_rect)
        if src_rect_hash not in self.scene.blocks_brushs_map:
            self.scene.blocks_brushs_map[src_rect_hash] = QtGui.QBrush(
                self.scene.blocks_pixmap.copy(src_rect))

        self.brush = self.scene.blocks_brushs_map[src_rect_hash]
        self.transform = QtGui.QTransform()
        self.transform.translate(pos[0], pos[1])

    def update(self, painter):
        self.brush.setTransform(self.transform)
        painter.setBrush(self.brush)
        painter.setPen(Qt.darkCyan)
        painter.drawRect(self.rect())
        # painter.drawPixmap(
        #     self.rect(),
        #     self.scene.blocks_pixmap,
        #     self.src_rect)


class Mario(Box):
    left_jump = QtCore.QRectF(29, 0, 18, 16)
    left_stop = QtCore.QRectF(58, 0, 18, 16)
    left_start = QtCore.QRectF(88, 0, 18, 16)
    left_walk_1 = QtCore.QRectF(118, 0, 18, 16)
    left_walk_2 = QtCore.QRectF(148, 0, 18, 16)
    left_stay = QtCore.QRectF(178, 0, 18, 16)

    right_stay = QtCore.QRectF(208, 0, 18, 16)
    right_walk_2 = QtCore.QRectF(238, 0, 18, 16)
    right_walk_1 = QtCore.QRectF(268, 0, 18, 16)
    right_start = QtCore.QRectF(298, 0, 18, 16)
    right_stop = QtCore.QRectF(328, 0, 18, 16)
    right_jump = QtCore.QRectF(358, 0, 18, 16)

    fail_left = QtCore.QRectF(0, 15, 15, 16)
    fail_right = QtCore.QRectF(390, 15, 15, 16)

    left_walk_seq = [left_start, left_walk_1, left_walk_2]
    right_walk_seq = [right_start, right_walk_1, right_walk_2]

    walk_animation_speed = 0.1

    class States(enum.Enum):
        WAIT_LEFT = 1
        WAIT_RIGHT = 2
        RUN_LEFT = 3
        RUN_RIGHT = 4
        JUMP_LEFT = 5
        JUMP_RIGHT = 6

    def __init__(self, scene, pos):
        super().__init__(scene, pos, [40, 40])
        self.state = self.States.WAIT_LEFT
        self.start_time = time.time()
        self.src_rect = self.left_stay

    def update(self, painter):
        target = self.rect()

        # update states
        if self.state == self.States.WAIT_LEFT:
            self.src_rect = self.left_stay
            self.check_start_move()
        elif self.state == self.States.WAIT_RIGHT:
            self.src_rect = self.right_stay
            self.check_start_move()
        elif self.state == self.States.RUN_LEFT:
            if not self.scene.key_map.get(Qt.Key_Left, 0):
                self.state = self.States.WAIT_LEFT
                self.src_rect = self.left_stay
            else:
                self.src_rect = self.left_walk_seq[int(
                    (time.time() - self.start_time) /
                    self.walk_animation_speed) % len(self.left_walk_seq)]
        elif self.state == self.States.RUN_RIGHT:
            if not self.scene.key_map.get(Qt.Key_Right, 0):
                self.state = self.States.WAIT_RIGHT
                self.src_rect = self.right_stay
            else:
                self.src_rect = self.right_walk_seq[int(
                    (time.time() - self.start_time) /
                    self.walk_animation_speed) % len(self.right_walk_seq)]
        elif self.state == self.States.JUMP_LEFT:
            pass
        elif self.state == self.States.JUMP_RIGHT:
            pass

        painter.drawPixmap(
            target,
            self.scene.mario_pixmap,
            self.src_rect)

        painter.drawRect(target)

    def check_start_move(self):
        # start move left
        if self.scene.key_map.get(Qt.Key_Left, 0):
            self.state = self.States.RUN_LEFT
            self.src_rect = self.left_start
            self.start_time = time.time()
        # start move right
        elif self.scene.key_map.get(Qt.Key_Right, 0):
            self.state = self.States.RUN_RIGHT
            self.src_rect = self.right_start
            self.start_time = time.time()


class Scene:
    def __init__(self):
        self.items = []
        self.key_map = {}
        self.blocks_brushs_map = {}
        file_path = os.path.join(
            os.path.split(__file__)[0], 'images/mario.png')
        self.mario_pixmap = QtGui.QPixmap(file_path)

        if self.mario_pixmap.isNull():
            LOG.error("Cannot load pixmap:%s" % (file_path))

        file_path = os.path.join(
            os.path.split(__file__)[0], 'images/blocks.png')
        self.blocks_pixmap = QtGui.QPixmap(file_path)

        if self.blocks_pixmap.isNull():
            LOG.error("Cannot load pixmap:%s" % (file_path))

    def update(self, painter):
        for item in self.items:
            item.update(painter)


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

        mario = Mario(self.scene, [0.0, -40])
        self.scene.items.append(mario)

        block = Block(self.scene, Block.block_1, [-1000, 0], [2000, 32])
        self.scene.items.append(block)

        block = Block(self.scene, Block.block_2, [-1000, 32], [2000, 32])
        self.scene.items.append(block)

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
            self.antialiased)

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
