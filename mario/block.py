from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import shape


class Block(shape.Shape):
    block_1 = QtCore.QRect(0, 0, 16, 16)
    block_2 = QtCore.QRect(16, 0, 16, 16)
    block_3 = QtCore.QRect(32, 0, 16, 16)
    block_4 = QtCore.QRect(48, 0, 16, 16)
    block_5 = QtCore.QRect(63, 0, 16, 16)

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
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
