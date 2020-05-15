# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication


class Ui_face_recog(object):
    def setupUi(self, face_recog):
        face_recog.setObjectName("face_recog")
        face_recog.resize(300, 400)
        self.centralwidget = QtWidgets.QWidget(face_recog)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(235, 230, 210);")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 300, 400))
        self.groupBox.setObjectName("groupBox")
        self.bottons = QtWidgets.QVBoxLayout(self.groupBox)
        self.bottons.setContentsMargins(10, 20, 10, 20)
        self.bottons.setSpacing(10)
        self.bottons.setObjectName("bottons")
        self.button_input = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_input.sizePolicy().hasHeightForWidth())
        self.button_input.setSizePolicy(sizePolicy)
        self.button_input.setObjectName("button_input")
        self.bottons.addWidget(self.button_input)
        self.button_check = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_check.sizePolicy().hasHeightForWidth())
        self.button_check.setSizePolicy(sizePolicy)
        self.button_check.setObjectName("button_check")
        self.bottons.addWidget(self.button_check)
        self.button_exit = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_exit.sizePolicy().hasHeightForWidth())
        self.button_exit.setSizePolicy(sizePolicy)
        self.button_exit.setObjectName("button_exit")
        self.button_exit.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.button_check.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.button_input.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.bottons.addWidget(self.button_exit)
        # face_recog.setCentralWidget(self.centralwidget)
        self.retranslateUi(face_recog)
        QtCore.QMetaObject.connectSlotsByName(face_recog)
        self.button_exit.clicked.connect(self.on_ExitEvent)

    def on_ExitEvent(self):
        QCoreApplication.instance().quit()

    def retranslateUi(self, face_recog):
        _translate = QtCore.QCoreApplication.translate
        face_recog.setWindowTitle(_translate("face_recog", "人脸识别"))
        self.button_input.setText(_translate("face_recog", "录入"))
        self.button_check.setText(_translate("face_recog", "识别"))
        self.button_exit.setText(_translate("face_recog", "退出"))
