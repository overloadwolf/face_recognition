# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
import face_recognition
import cv2
from PyQt5.QtCore import pyqtSlot, QCoreApplication

process_this_frame = True


class Ui_Check(object):
    def setupUi(self, Dialog):
        self.known_face_encodings = [ ]
        self.known_face_names = [ ]
        self.known_face_numbers = [ ]
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: rgb(235, 230, 210);")
        # Create arrays of known face encodings and their names
        self.encode()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.photoarea = QtWidgets.QLabel(Dialog)
        self.photoarea.setGeometry(QtCore.QRect(70, 50, 300, 400))
        self.photoarea.setObjectName("photoarea")
        self.photoarea.setStyleSheet("background-color:gray;")
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
        self.namebar.setObjectName("nameline")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.numberbar = QtWidgets.QLabel(self.splitter_3)
        self.numberbar.setObjectName("numberline")
        self.buttonframe = QtWidgets.QFrame(Dialog)
        self.buttonframe.setGeometry(QtCore.QRect(0, 480, 801, 101))
        self.buttonframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonframe.setObjectName("buttonframe")
        self.splitter = QtWidgets.QSplitter(self.buttonframe)
        self.splitter.setGeometry(QtCore.QRect(120, 20, 561, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.retrybutton = QtWidgets.QPushButton(self.splitter)
        self.retrybutton.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.retrybutton.setObjectName("retrybutton")
        self.exitbutton = QtWidgets.QPushButton(self.splitter)
        self.exitbutton.setStyleSheet(
            "QPushButton{\nbackground-color:rgb(183, 145, 82);\ncolor: black; \nborder-radius: 10px;\nborder-style:outset;}")
        self.exitbutton.setObjectName("exitbutton")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.timer_camera = QtCore.QTimer()
        self.slot_init()
        self.__flag_work = 0
        self.label_move = QtWidgets.QLabel()
        self.label_move.raise_()

    def slot_init(self):
        self.retrybutton.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.exitbutton.clicked.connect(self.on_ExitEvent)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):
        temp = ""
        self.namebar.setText(temp + "姓名:")
        temp = ""
        self.numberbar.setText(temp + "卡号:")
        flag, frame = self.cap.read()
        show = cv2.resize(frame, (300, 400))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.photoarea.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                currname = self.known_face_names[first_match_index]
                currnumber = self.known_face_numbers[first_match_index]
                temp = ""
                self.namebar.setText(temp + "姓名:" + currname)
                temp = ""
                self.numberbar.setText(temp + "卡号:" + currnumber)
                self.timer_camera.stop()

    def on_ExitEvent(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == True:
            self.namebar.setText("姓名:")
            self.numberbar.setText("卡号:")
            self.timer_camera.stop()
            self.cap.release()
            self.photoarea.clear()
        self.close()

    def encode(self):
        for file in os.listdir("recorded\\"):
            image = face_recognition.load_image_file("recorded\\" + file)
            image_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(image_encoding)
            filename = str(file).split(".")[0]
            currname = filename.split("+", 1)[0]
            currnumber = filename.split("+", 1)[1]
            self.known_face_names.append(currname)
            self.known_face_numbers.append(currnumber)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "识别"))
        self.namebar.setText(_translate("Dialog", "姓名："))
        self.numberbar.setText(_translate("Dialog", "卡号："))
        self.retrybutton.setText(_translate("Dialog", "识别"))
        self.exitbutton.setText(_translate("Dialog", "退出"))
