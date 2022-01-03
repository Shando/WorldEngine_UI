# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '3d.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import new_gui_4_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1280, 1024)
        font = QFont()
        font.setFamily(u"Open Sans")
        font.setPointSize(12)
        Dialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Images/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet(u"")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 80, 1261, 51))
        font1 = QFont()
        font1.setFamily(u"Open Sans")
        font1.setPointSize(24)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 64, 64))
        self.label_2.setPixmap(QPixmap(u":/Images/seed_48791_elevation.png"))
        self.label_2.setScaledContents(True)
        self.label_52 = QLabel(Dialog)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setGeometry(QRect(1210, 10, 64, 64))
        self.label_52.setPixmap(QPixmap(u":/Images/seed_48791_elevation.png"))
        self.label_52.setScaledContents(True)
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(80, 10, 1121, 61))
        font2 = QFont()
        font2.setFamily(u"Open Sans")
        font2.setPointSize(24)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_6.setFont(font2)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"WorldEngine 3D Viewer", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"WASD to move, F toggles flying", None))
        self.label_2.setText("")
        self.label_52.setText("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>WorldEngine</p></body></html>", None))
    # retranslateUi

