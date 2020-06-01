#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "main_widget.ui"),
            self)
        self.widget.current_grid_changed.connect(self.update_settings)

        self.spinBox_rows.valueChanged.connect(self.rows_changed)
        self.spinBox_colums.valueChanged.connect(self.colums_changed)
        self.spinBox_rows_offset.valueChanged.connect(self.rows_offset_changed)
        self.spinBox_colums_offset.valueChanged.connect(self.colums_offset_changed)

    def rows_changed(self, value):
        if self.widget.cur_grid is not None:
            self.widget.cur_grid.set_rows(value)

    def colums_changed(self, value):
        if self.widget.cur_grid is not None:
            self.widget.cur_grid.set_columns(value)

    def rows_offset_changed(self, value):
        if self.widget.cur_grid is not None:
            self.widget.cur_grid.set_rows_offset(value)

    def colums_offset_changed(self, value):
        if self.widget.cur_grid is not None:
            self.widget.cur_grid.set_colums_offset(value)

    def update_settings(self, grid):
        if grid is not None:
            self.spinBox_rows.setValue(grid.rows)
            self.spinBox_colums.setValue(grid.columns)
            self.spinBox_rows_offset.setValue(grid.rows_offset)
            self.spinBox_colums_offset.setValue(grid.colums_offset)



def main():
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.show()
    res = app.exec_()
    sys.exit(res)
