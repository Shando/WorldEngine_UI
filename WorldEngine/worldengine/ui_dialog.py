# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
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
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(469, 300)
        font = QFont()
        font.setFamily(u"Open Sans")
        font.setPointSize(12)
        Dialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Images/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet(u"")
        Dialog.setModal(True)
        self.btnCentre = QPushButton(Dialog)
        self.btnCentre.setObjectName(u"btnCentre")
        self.btnCentre.setGeometry(QRect(180, 230, 111, 41))
        font1 = QFont()
        font1.setFamily(u"Open Sans")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.btnCentre.setFont(font1)
        self.lblIcon = QLabel(Dialog)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setGeometry(QRect(0, 40, 141, 141))
        self.lblIcon.setPixmap(QPixmap(u":/Images/error.png"))
        self.lblIcon.setAlignment(Qt.AlignCenter)
        self.lblMsg = QLabel(Dialog)
        self.lblMsg.setObjectName(u"lblMsg")
        self.lblMsg.setGeometry(QRect(156, 32, 291, 171))
        self.lblMsg.setFont(font1)
        self.lblMsg.setAlignment(Qt.AlignCenter)
        self.lblMsg.setWordWrap(True)
        self.btnRight = QPushButton(Dialog)
        self.btnRight.setObjectName(u"btnRight")
        self.btnRight.setGeometry(QRect(340, 230, 111, 41))
        self.btnRight.setFont(font1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Worldengine Dialog", None))
        self.btnCentre.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.lblIcon.setText("")
        self.lblMsg.setText(QCoreApplication.translate("Dialog", u"Message Text goes here", None))
        self.btnRight.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

