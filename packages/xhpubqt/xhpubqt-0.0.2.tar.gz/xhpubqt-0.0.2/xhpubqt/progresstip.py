# -*- coding:utf-8 -*-
'''
@Author: lamborghini1993
@Date: 2019-11-06 16:27:05
@UpdateDate: 2019-11-06 17:10:35
@Description: 进度条提示
'''

import sys

from PyQt5 import QtWidgets


class ProgressTip(QtWidgets.QProgressDialog):
    def __init__(self, tip="waiting...", parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setLabelText(tip)
        self.setCancelButton(None)
        self.setAutoClose(True)


class TestWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 50)
        hbox = QtWidgets.QHBoxLayout(self)
        btn = QtWidgets.QPushButton("开始", self)
        hbox.addWidget(btn)
        btn.clicked.connect(self.Start)
        self.progress = ProgressTip("Test")

    def Start(self):
        import time
        self.progress.open()
        for x in range(101):
            time.sleep(0.1)
            self.progress.setValue(x)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    obj = TestWidget()
    obj.show()
    sys.exit(app.exec_())
