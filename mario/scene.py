#!/usr/bin/env python

import os
from PyQt5 import QtGui
import logging

LOG = logging.getLogger(__name__)


class Scene:
    gravity_accel = 1

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

