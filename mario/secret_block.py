from PyQt5 import QtCore
import time
from mario import shape


class SecretBlock(shape.Shape):
    animate = [
        QtCore.QRectF(0, 0, 16, 16),
        QtCore.QRectF(16, 0, 16, 16),
        QtCore.QRectF(32, 0, 16, 16)
    ]
    last = QtCore.QRectF(48, 0, 16, 16)
    anim_speed = 0.3
    start_time = time.time()

    def __init__(self, scene, pos):
        super().__init__(scene, pos, [16, 16])
        self.state = 0

    def update(self, painter):
        if self.state == 0:
            src = self.animate[int(
                (time.time() - self.start_time) / self.anim_speed) %
                len(self.animate)]

            painter.drawPixmap(
                self.rect(),
                self.scene.blocks_pixmap,
                src)
