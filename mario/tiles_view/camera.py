from PyQt5 import QtGui, QtCore


class Camera:
    ide_state = 0
    move_state = 1

    def __init__(self):
        self.transform = QtGui.QTransform()
        self.inverted = self.transform.inverted()[0]
        self.state = self.ide_state

    def move(self, pos):
        if self.state == self.move_state:
            offset = self.inverted.map(pos) -\
                self.inverted.map(self.last_pos)
            self.last_pos = pos
            self.transform.translate(offset.x(), offset.y())
            self.inverted = self.transform.inverted()[0]
            return 1

    def start_move(self, pos):
        self.last_pos = pos
        self.state = self.move_state

    def stop_move(self):
        if self.state == self.move_state:
            self.state = self.ide_state

    def update_scale(self, pos):
        scale = 1.2 if pos.y() > 0 else 0.8
        self.transform.scale(scale, scale)
        self.inverted = self.transform.inverted()[0]

    def to_scene(self, pos):
        return self.inverted.map(QtCore.QPointF(pos.x(), pos.y()))

    def to_view(self, pos):
        return self.transform.map(pos)
