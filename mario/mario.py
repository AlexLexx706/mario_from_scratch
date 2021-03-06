#!/usr/bin/env python

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import enum
import time
import math
from mario import shape


class Mario(shape.Shape):
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

    walk_speed_max = 70.
    walk_accel = 100.
    stop_accel = 100.
    stop_speed = 10.

    run_speed_max = 10.
    max_jump_speed = 100.

    class Direction(enum.Enum):
        LEFT = 0
        RIGHT = 1

    def __init__(self, scene, pos):
        super().__init__(scene, pos, [18, 18])
        self.start_time = time.time()
        self.src_rect = self.left_stay
        self.old_speed = [0.0, 0.0]
        self.direction = self.Direction.LEFT

    def update(self, painter):
        # draw mario
        self.update_control()
        painter.drawPixmap(
            self.rect(),
            self.scene.mario_pixmap,
            self.get_sprite_rect())

    def update_control(self):
        # update acells
        x_accel = 0.
        y_accel = self.scene.gravity_accel
        max_x_speed = self.walk_speed_max

        # checks control
        if self.scene.key_map.get(Qt.Key_Left, 0):
            x_accel = -self.walk_accel
            self.direction = self.Direction.LEFT
        # start move right
        elif self.scene.key_map.get(Qt.Key_Right, 0):
            x_accel = self.walk_accel
            self.direction = self.Direction.RIGHT
        # try jump
        if self.scene.key_map.get(Qt.Key_Space, 0) and self.landing_flag:
            self.speed[1] = -self.max_jump_speed
            self.scene.key_map[Qt.Key_Space] = 0

        # press shift for run
        if self.scene.key_map.get(Qt.Key_Shift, 0):
            max_x_speed = self.run_speed_max

        # try stop mario
        if x_accel == 0:
            # speed more then stop_window
            if math.fabs(self.speed[0]) > self.stop_speed:
                x_accel = self.stop_accel\
                    if self.speed[0] < 0. else -self.stop_accel
            # stop mario
            else:
                x_accel = 0
                self.speed[0] = 0

        # update speed
        self.speed[0] += self.scene.dt * x_accel
        self.speed[1] += self.scene.dt * y_accel

        # checks x speed limmit
        fx_speed = math.fabs(self.speed[0])
        if fx_speed > max_x_speed:
            self.speed[0] = max_x_speed if self.speed[0] > 0\
                else -max_x_speed

        # checks y speed limmit
        fy_speed = math.fabs(self.speed[1])
        if fy_speed > self.max_jump_speed:
            self.speed[1] = self.max_jump_speed if self.speed[1] > 0\
                else -self.max_jump_speed

        # collision detection
        self.landing_flag = False

        self.pos[0] += self.scene.dt * self.speed[0]
        for item in self.scene.items:
            if item != self:
                self.collision(item, True)

        self.pos[1] += self.scene.dt * self.speed[1]
        for item in self.scene.items:
            if item != self:
                self.collision(item, False)
        self.old_speed = self.speed

    def get_sprite_rect(self):
        # not jump
        if self.speed[1] == 0 and self.landing_flag:
            # not move
            if self.speed[0] == 0:
                if self.direction == self.Direction.LEFT:
                    return self.left_stay
                else:
                    return self.right_stay
            # move
            else:
                # move left
                if self.speed[0] < 0.:
                    # move left
                    if self.direction == self.Direction.LEFT:
                        if self.old_speed[0] >= 0:
                            self.start_time = time.time()
                        return self.left_walk_seq[int(
                            (time.time() - self.start_time) /
                            self.walk_animation_speed) % len(self.left_walk_seq)]
                    # change direction
                    else:
                        return self.left_stop
                # move right
                elif self.speed[0] > 0.:
                    # move right
                    if self.direction == self.Direction.RIGHT:
                        if self.old_speed[0] <= 0.:
                            self.start_time = time.time()
                        return self.right_walk_seq[int(
                            (time.time() - self.start_time) /
                            self.walk_animation_speed) % len(self.right_walk_seq)]
                    # change direction
                    else:
                        return self.right_stop
        # jump
        else:
            if self.direction == self.Direction.LEFT:
                return self.left_jump
            else:
                return self.right_jump
