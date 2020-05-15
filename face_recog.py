import sys
from MainWindow import Ui_face_recog
from InsertWindow import Ui_Insert
from CheckWindow import Ui_Check
from PyQt5 import QtWidgets


# 主界面
class MainWindow(QtWidgets.QWidget, Ui_face_recog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class InsertWindow(QtWidgets.QWidget, Ui_Insert):
    def __init__(self, parent=None):
        super(InsertWindow, self).__init__(parent)
        self.setupUi(self)


class CheckWindow(QtWidgets.QWidget, Ui_Check):
    def __init__(self, parent=None):
        super(CheckWindow, self).__init__(parent)
        self.setupUi(self)
        self.encode()


# 调用show
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MW = MainWindow()
    IW = InsertWindow()
    CW = CheckWindow()
    MW.button_input.clicked.connect(IW.show)
    MW.button_check.clicked.connect(CW.show)
    MW.button_check.clicked.connect(CW.encode)
    CW.exitbutton.clicked.connect(MW.show)
    IW.exitbutton.clicked.connect(MW.show)
    MW.show()
    sys.exit(app.exec_())
