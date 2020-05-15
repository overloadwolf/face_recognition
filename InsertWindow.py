# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMessageBox
import face_recognition
import cv2
from PIL import Image, ImageDraw

buttonstats = 0


class Ui_Insert(object):
    def setupUi(self, Dialog):
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: rgb(235, 230, 210);")
        self.photoarea = QtWidgets.QLabel(Dialog)
        self.photoarea.setGeometry(QtCore.QRect(70, 50, 300, 400))
        self.photoarea.setStyleSheet("background-color:gray;")
        self.photoarea.setObjectName("photoarea")
        self.photoarea.clear()
        self.infoframe = QtWidgets.QFrame(Dialog)
        self.infoframe.setGeometry(QtCore.QRect(410, 60, 321, 391))
        self.infoframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.infoframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.infoframe.setObjectName("infoframe")
        self.splitter_4 = QtWidgets.QSplitter(self.infoframe)
        self.splitter_4.setGeometry(QtCore.QRect(0, 180, 310, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.splitter_4.sizePolicy().hasHeightForWidth())
        self.splitter_4.setSizePolicy(sizePolicy)
        self.splitter_4.setTabletTracking(False)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.namebar = QtWidgets.QLabel(self.splitter_2)
        self.namebar.setObjectName("namebar")
        self.nameinsert = QtWidgets.QTextEdit(self.splitter_2)
        self.nameinsert.setObjectName("nameinsert")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.numberbar = QtWidgets.QLabel(self.splitter_3)
        self.numberbar.setObjectName("numberbar")
        self.numberinsert = QtWidgets.QTextEdit(self.splitter_3)
        self.numberinsert.setObjectName("numberinsert")
        self.buttonframe = QtWidgets.QFrame(Dialog)
        self.buttonframe.setGeometry(QtCore.QRect(60, 470, 801, 101))
        self.buttonframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonframe.setObjectName("buttonframe")
        self.splitter = QtWidgets.QSplitter(self.buttonframe)
        self.splitter.setGeometry(QtCore.QRect(70, 10, 531, 81))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.insertbutton = QtWidgets.QPushButton(self.splitter)
        self.insertbutton.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.insertbutton.setObjectName("insertbutton")
        self.confirmbutton = QtWidgets.QPushButton(self.splitter)
        self.confirmbutton.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.confirmbutton.setObjectName("confirmbutton")
        self.exitbutton = QtWidgets.QPushButton(self.splitter)
        self.exitbutton.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.exitbutton.setObjectName("exitbutton")
        self.retranslateUi(Dialog)
        self.face_locations = [ ]
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.timer_camera = QtCore.QTimer()
        self.slot_init()
        self.__flag_work = 0
        self.label_move = QtWidgets.QLabel()
        self.label_move.raise_()

    def slot_init(self):
        self.insertbutton.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.exitbutton.clicked.connect(self.on_ExitEvent)
        self.confirmbutton.clicked.connect(self.setinfo)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (300, 400))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.photoarea.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.face_locations = face_recognition.face_locations(show)
        if len(self.face_locations) == 1:
            for face_location in self.face_locations:
                # Print the location of each face in this image
                top, right, bottom, left = face_location
                face_image = show[top:bottom, left:right]
                self.pil_image = Image.fromarray(face_image)
            self.timer_camera.stop()
            self.cap.release()

    def on_ExitEvent(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == True:
            self.timer_camera.stop()
            self.cap.release()
            self.photoarea.clear()
        self.close()

    def setinfo(self):
        setname = self.nameinsert.toPlainText()
        setnumber = self.numberinsert.toPlainText()
        if len(self.face_locations) == 1:
            dir = "recorded\\" + setname + "+" + setnumber + ".jpg"
            cv2.imwrite(dir, self.image)
            QMessageBox.information(self, "成功", "录入成功", QMessageBox.Yes)
            self.nameinsert.clear()
            self.numberinsert.clear()
            self.on_ExitEvent()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "录入"))
        self.namebar.setText(_translate("Dialog", "姓名"))
        self.numberbar.setText(_translate("Dialog", "卡号"))
        self.insertbutton.setText(_translate("Dialog", "开始录入"))
        self.confirmbutton.setText(_translate("Dialog", "确认"))
        self.exitbutton.setText(_translate("Dialog", "退出"))
