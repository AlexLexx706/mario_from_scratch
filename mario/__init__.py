#!/usr/bin/env python

import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import enum
import time
import logging

LOG = logging.getLogger(__name__)



class SceneWidget(QtWidgets.QWidget):
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

    all_steps = [
        left_jump, left_stop, left_start, left_walk_1, left_walk_2, left_stay,
        right_stay, right_walk_2, right_walk_1, right_start, right_stop, right_jump,
        fail_left, fail_right
    ]

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

    def __init__(self, parent=None):
        super(SceneWidget, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.next_animation_frame)
        self.timer.start(50)
        self.frame_no = 0
        self.antialiased = True
        self.key_map = {}
        self.state = self.States.WAIT_LEFT
        self.start_time = time.time()
        self.src_rect = self.left_stay

        # load character texrure
        file_path = os.path.join(
            os.path.split(__file__)[0], 'images/mario.png')
        self.pixmap_characters = QtGui.QPixmap(file_path)

        if self.pixmap_characters.isNull():
            LOG.warning('cult not load texture:%s' % (file_path, ))

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
        target = QtCore.QRectF(0.0, 0.0, 100.0, 100.0)

        # update states
        if self.state == self.States.WAIT_LEFT:
            self.src_rect = self.left_stay
            self.check_start_move()
        elif self.state == self.States.WAIT_RIGHT:
            self.src_rect = self.right_stay
            self.check_start_move()
        elif self.state == self.States.RUN_LEFT:
            if not self.key_map.get(Qt.Key_Left, 0):
                self.state = self.States.WAIT_LEFT
                self.src_rect = self.left_stay
            else:
                self.src_rect = self.left_walk_seq[int(
                    (time.time() - self.start_time) /
                    self.walk_animation_speed) % len(self.left_walk_seq)]
        elif self.state == self.States.RUN_RIGHT:
            if not self.key_map.get(Qt.Key_Right, 0):
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
            self.pixmap_characters,
            # self.all_steps[self.frame_no % len(self.all_steps)]
            self.src_rect)

        painter.drawRect(target)

    def check_start_move(self):
        # start move left
        if self.key_map.get(Qt.Key_Left, 0):
            self.state = self.States.RUN_LEFT
            self.src_rect = self.left_start
            self.start_time = time.time()
        # start move right
        elif self.key_map.get(Qt.Key_Right, 0):
            self.state = self.States.RUN_RIGHT
            self.src_rect = self.right_start
            self.start_time = time.time()

    def keyPressEvent(self, event):
        self.key_map[event.key()] = 1
        if event.key() == Qt.Key_Up:
            print('up')
        elif event.key() == Qt.Key_Down:
            print('down')
        elif event.key() == Qt.Key_Left:
            print('left')
        elif event.key() == Qt.Key_Right:
            print('right')

    def keyReleaseEvent(self, event):
        self.key_map[event.key()] = 0


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SceneWidget()
    window.show()
    sys.exit(app.exec_())
