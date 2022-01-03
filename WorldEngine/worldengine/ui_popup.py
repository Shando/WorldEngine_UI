# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'popup.ui'
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
        Dialog.resize(654, 603)
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
        self.label.setGeometry(QRect(10, 80, 631, 51))
        font1 = QFont()
        font1.setFamily(u"Open Sans")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignCenter)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 140, 611, 441))
        font2 = QFont()
        font2.setFamily(u"Consolas")
        font2.setPointSize(10)
        self.textBrowser.setFont(font2)
        self.textBrowser.setStyleSheet(u"")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 64, 64))
        self.label_2.setPixmap(QPixmap(u":/Images/seed_48791_elevation.png"))
        self.label_2.setScaledContents(True)
        self.label_52 = QLabel(Dialog)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setGeometry(QRect(580, 10, 64, 64))
        self.label_52.setPixmap(QPixmap(u":/Images/seed_48791_elevation.png"))
        self.label_52.setScaledContents(True)
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(80, 10, 491, 61))
        font3 = QFont()
        font3.setFamily(u"Open Sans")
        font3.setPointSize(24)
        font3.setBold(True)
        font3.setWeight(75)
        self.label_6.setFont(font3)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"WorldEngine Information Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Please wait while the World is being created.....", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Consolas'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">01234567890</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">abcdefghijk</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">lmnopqrstuv</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">wxyz-</p></body></html>", None))
        self.label_2.setText("")
        self.label_52.setText("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>WorldEngine</p></body></html>", None))
    # retranslateUi

