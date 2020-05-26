#!/usr/bin/env python

import os
from PyQt5 import QtGui
import logging
import time
LOG = logging.getLogger(__name__)


class Scene:
    gravity_accel = 1

    def __init__(self):
        self.items = []
        self.dt = 0.1
        self.last_time = None
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
        cur_time = time.time()
        if self.last_time is not None:
            self.dt = cur_time - self.last_time

        for item in self.items:
            item.update(painter)
        self.last_time = cur_time

