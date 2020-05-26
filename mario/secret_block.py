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
    max_jump_speed = 40.
    max_jump_distance = 10

    def __init__(self, scene, pos):
        super().__init__(scene, pos, [16, 16])
        self.state = 0

    def update(self, painter):
        old_state = self.state

        if self.intersection_info is not None and self.state == 0:
            # check type of intersection with mario
            if self.intersection_info[0][1] != 0 and\
                    self.intersection_info[1][1] < 0.:
                self.intersection_info = None
                self.state = 1

        # animate blinking
        if self.state == 0:
            src = self.animate[int(
                (time.time() - self.start_time) / self.anim_speed) %
                len(self.animate)]
        # animate jump of block
        elif self.state == 1:
            if self.state != old_state:
                self.start_jump = time.time()
                self.jump_direction = 0
                self.start_jump_pos = self.pos.copy()
                self.jump_distance = 0.

            if self.jump_direction == 0:
                self.jump_distance += self.max_jump_speed * self.scene.dt
                if self.jump_distance > self.max_jump_distance:
                    self.jump_distance = self.max_jump_distance
                    self.jump_direction = 1
            else:
                self.jump_distance -= self.max_jump_speed * self.scene.dt
                if self.jump_distance <= 0:
                    self.jump_distance = 0
                    self.state = 3
            self.pos[1] = self.start_jump_pos[1] - self.jump_distance
            src = self.last
        elif self.state == 3:
            print("boom")
            src = self.last

        painter.drawPixmap(
            self.rect(),
            self.scene.blocks_pixmap,
            src)
