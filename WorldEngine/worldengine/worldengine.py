# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Users\Simon\Documents\Monkey Studio\Projects\worldengine.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import worldengine_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WorldEngine(object):
    def setupUi(self, WorldEngine):
        WorldEngine.setObjectName(_fromUtf8("WorldEngine"))
        WorldEngine.resize(1158, 837)
        WorldEngine.setStyleSheet(_fromUtf8("QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #FF9930;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #FFE6B1;\n"
"    background-color: #376E77;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #942610);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #FFE6B1;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #498089;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #265D66,\n"
"        stop:0.4 #397079/*,\n"
"        stop:0.2 #397079,\n"
"        stop:0.1 #FFE6B1*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #457C85;\n"
"    background-color: #376E77;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #528992, stop: 0.1 #689FA8, stop: 1 #6299A2);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #528992, stop: 0 #689FA8, stop: 1 #6299A2);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #235A63;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #FFE6B1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5B929B, stop: 0.1 #578E97, stop: 0.5 #538A93, stop: 0.9 #4F868F, stop: 1 #4B828B);\n"
"    border-width: 1px;\n"
"    border-color: #235A63;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #326972, stop: 0.1 #306770, stop: 0.5 #2E656E, stop: 0.9 #2D646D, stop: 1 #2A616A);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #FFE6B1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5B929B, stop: 0.1 #578E97, stop: 0.5 #538A93, stop: 0.9 #4F868F, stop: 1 #4B828B);\n"
"    border-style: solid;\n"
"    border: 1px solid #235A63;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"/*    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);*/\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #942610);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #326972, stop: 0.1 #306770, stop: 0.5 #2E656E, stop: 0.9 #2D646D, stop: 1 #2A616A);\n"
"    selection-background-color: #FFE6B1;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #275E67;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #174E57, stop: 0.2 #2D646D, stop: 1 #4D828D);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FF9930, stop: 0.5 #452102, stop: 1 #FF9930);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #20575E;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FF9930, stop: 1 #452102);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #20575E;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FF9930, stop: 1 #452102);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #174E57, stop: 0.2 #2D646D, stop: 1 #4D828D);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #275E67;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 0.5 #452102, stop: 1 #FF9930);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #20575E;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FF9930, stop: 1 #452102);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #20575E;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #452102, stop: 1 #FF9930);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #296069;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #296069;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #669DA6, stop: 0.5 #558C95, stop: 0.6 #487F88, stop:1 #69A0A9);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #70A7B0;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #467D86;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #376E77, stop: 0.5 #296069, stop:1 #376E77);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #376E77, stop: 0.5 #296069, stop:1 #376E77);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #296069;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1B525B, stop: 0.5 #1A515A, stop: 0.6 #265D66, stop:1 #397079);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #518891;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #452102, stop:0.5 #b56c17 stop:1 #FF9930);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #70A7B0;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1B525B, stop: 0.5 #1A515A, stop: 0.6 #265D66, stop:1 #397079);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #452102;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #452102;\n"
"    border: 1px solid #498089;\n"
"    border-bottom-style: none;\n"
"    background-color: #376E77;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #498089;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #452102;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #265D66, stop:.4 #397079);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #FFE6B1;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #265D66, stop:0.4 #397079, stop:0.2 #397079, stop:0.1 #FFE6B1);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #452102;\n"
"    background-color: #376E77;\n"
"    border: 1px solid #452102;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #FFE6B1,\n"
"        stop: 0.3 #376E77\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #452102;\n"
"    background-color: #376E77;\n"
"    border: 1px solid #452102;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #FFE6B1;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #498089;\n"
"}\n"
""))
        self.centralWidget = QtGui.QWidget(WorldEngine)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(10, 80, 1141, 711))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        self.frame.setFont(font)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.tabWidget = QtGui.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1121, 691))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.txtWorld = QtGui.QLineEdit(self.tab)
        self.txtWorld.setGeometry(QtCore.QRect(350, 20, 421, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.txtWorld.setFont(font)
        self.txtWorld.setMaxLength(128)
        self.txtWorld.setObjectName(_fromUtf8("txtWorld"))
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.spnWidth = QtGui.QSpinBox(self.tab)
        self.spnWidth.setGeometry(QtCore.QRect(350, 100, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.spnWidth.setFont(font)
        self.spnWidth.setMinimum(256)
        self.spnWidth.setMaximum(8192)
        self.spnWidth.setSingleStep(256)
        self.spnWidth.setProperty("value", 1024)
        self.spnWidth.setObjectName(_fromUtf8("spnWidth"))
        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(10, 100, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(460, 100, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.spnHeight = QtGui.QSpinBox(self.tab)
        self.spnHeight.setGeometry(QtCore.QRect(680, 100, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.spnHeight.setFont(font)
        self.spnHeight.setMinimum(256)
        self.spnHeight.setMaximum(8192)
        self.spnHeight.setSingleStep(256)
        self.spnHeight.setProperty("value", 1024)
        self.spnHeight.setObjectName(_fromUtf8("spnHeight"))
        self.label_12 = QtGui.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(10, 140, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.spnPlates = QtGui.QSpinBox(self.tab)
        self.spnPlates.setGeometry(QtCore.QRect(350, 140, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.spnPlates.setFont(font)
        self.spnPlates.setMinimum(1)
        self.spnPlates.setMaximum(100)
        self.spnPlates.setSingleStep(10)
        self.spnPlates.setProperty("value", 10)
        self.spnPlates.setObjectName(_fromUtf8("spnPlates"))
        self.label_14 = QtGui.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(10, 620, 291, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_31 = QtGui.QLabel(self.tab)
        self.label_31.setGeometry(QtCore.QRect(10, 220, 161, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.cboData = QtGui.QComboBox(self.tab)
        self.cboData.setGeometry(QtCore.QRect(1010, 220, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.cboData.setFont(font)
        self.cboData.setObjectName(_fromUtf8("cboData"))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboData.addItem(_fromUtf8(""))
        self.cboFormat = QtGui.QComboBox(self.tab)
        self.cboFormat.setGeometry(QtCore.QRect(350, 220, 331, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.cboFormat.setFont(font)
        self.cboFormat.setObjectName(_fromUtf8("cboFormat"))
        self.cboFormat.addItem(_fromUtf8(""))
        self.cboFormat.addItem(_fromUtf8(""))
        self.cboFormat.addItem(_fromUtf8(""))
        self.cboFormat.addItem(_fromUtf8(""))
        self.label_32 = QtGui.QLabel(self.tab)
        self.label_32.setGeometry(QtCore.QRect(790, 220, 161, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.btnWorld = QtGui.QPushButton(self.tab)
        self.btnWorld.setGeometry(QtCore.QRect(790, 20, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnWorld.setFont(font)
        self.btnWorld.setObjectName(_fromUtf8("btnWorld"))
        self.line = QtGui.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(-4, 260, 1131, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_22 = QtGui.QLabel(self.tab)
        self.label_22.setGeometry(QtCore.QRect(10, 380, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.spnOffset = QtGui.QDoubleSpinBox(self.tab)
        self.spnOffset.setGeometry(QtCore.QRect(900, 580, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnOffset.setFont(font)
        self.spnOffset.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnOffset.setDecimals(3)
        self.spnOffset.setMaximum(0.999)
        self.spnOffset.setSingleStep(0.1)
        self.spnOffset.setProperty("value", 0.2)
        self.spnOffset.setObjectName(_fromUtf8("spnOffset"))
        self.spnTemp5 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp5.setGeometry(QtCore.QRect(790, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp5.setFont(font)
        self.spnTemp5.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp5.setDecimals(3)
        self.spnTemp5.setMaximum(1.0)
        self.spnTemp5.setSingleStep(0.1)
        self.spnTemp5.setProperty("value", 0.634)
        self.spnTemp5.setObjectName(_fromUtf8("spnTemp5"))
        self.label_43 = QtGui.QLabel(self.tab)
        self.label_43.setGeometry(QtCore.QRect(10, 280, 1091, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.label_43.setFont(font)
        self.label_43.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.label_43.setAlignment(QtCore.Qt.AlignCenter)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.label_24 = QtGui.QLabel(self.tab)
        self.label_24.setGeometry(QtCore.QRect(10, 500, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.spnPrecip1 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip1.setGeometry(QtCore.QRect(350, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip1.setFont(font)
        self.spnPrecip1.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip1.setDecimals(3)
        self.spnPrecip1.setMaximum(1.0)
        self.spnPrecip1.setSingleStep(0.1)
        self.spnPrecip1.setProperty("value", 0.059)
        self.spnPrecip1.setObjectName(_fromUtf8("spnPrecip1"))
        self.label_25 = QtGui.QLabel(self.tab)
        self.label_25.setGeometry(QtCore.QRect(10, 540, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.spnGamma = QtGui.QDoubleSpinBox(self.tab)
        self.spnGamma.setGeometry(QtCore.QRect(350, 580, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnGamma.setFont(font)
        self.spnGamma.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnGamma.setDecimals(3)
        self.spnGamma.setProperty("value", 1.25)
        self.spnGamma.setObjectName(_fromUtf8("spnGamma"))
        self.spnPrecip6 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip6.setGeometry(QtCore.QRect(900, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip6.setFont(font)
        self.spnPrecip6.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip6.setDecimals(3)
        self.spnPrecip6.setMaximum(1.0)
        self.spnPrecip6.setSingleStep(0.1)
        self.spnPrecip6.setProperty("value", 0.986)
        self.spnPrecip6.setObjectName(_fromUtf8("spnPrecip6"))
        self.label_27 = QtGui.QLabel(self.tab)
        self.label_27.setGeometry(QtCore.QRect(570, 580, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.spnSea = QtGui.QDoubleSpinBox(self.tab)
        self.spnSea.setGeometry(QtCore.QRect(350, 460, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnSea.setFont(font)
        self.spnSea.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnSea.setDecimals(3)
        self.spnSea.setMinimum(1.0)
        self.spnSea.setObjectName(_fromUtf8("spnSea"))
        self.label_26 = QtGui.QLabel(self.tab)
        self.label_26.setGeometry(QtCore.QRect(10, 580, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.label_30 = QtGui.QLabel(self.tab)
        self.label_30.setGeometry(QtCore.QRect(570, 420, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.label_21 = QtGui.QLabel(self.tab)
        self.label_21.setGeometry(QtCore.QRect(570, 340, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_20 = QtGui.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(10, 340, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.spnTemp2 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp2.setGeometry(QtCore.QRect(460, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp2.setFont(font)
        self.spnTemp2.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp2.setDecimals(3)
        self.spnTemp2.setMaximum(1.0)
        self.spnTemp2.setSingleStep(0.1)
        self.spnTemp2.setProperty("value", 0.235)
        self.spnTemp2.setObjectName(_fromUtf8("spnTemp2"))
        self.label_19 = QtGui.QLabel(self.tab)
        self.label_19.setGeometry(QtCore.QRect(570, 300, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.spnPrecip5 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip5.setGeometry(QtCore.QRect(790, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip5.setFont(font)
        self.spnPrecip5.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip5.setDecimals(3)
        self.spnPrecip5.setMaximum(1.0)
        self.spnPrecip5.setSingleStep(0.1)
        self.spnPrecip5.setProperty("value", 0.927)
        self.spnPrecip5.setObjectName(_fromUtf8("spnPrecip5"))
        self.spnPrecip7 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip7.setGeometry(QtCore.QRect(1010, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip7.setFont(font)
        self.spnPrecip7.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip7.setDecimals(3)
        self.spnPrecip7.setMaximum(1.0)
        self.spnPrecip7.setSingleStep(0.1)
        self.spnPrecip7.setProperty("value", 0.998)
        self.spnPrecip7.setObjectName(_fromUtf8("spnPrecip7"))
        self.spnPrecip2 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip2.setGeometry(QtCore.QRect(460, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip2.setFont(font)
        self.spnPrecip2.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip2.setDecimals(3)
        self.spnPrecip2.setMaximum(1.0)
        self.spnPrecip2.setSingleStep(0.1)
        self.spnPrecip2.setProperty("value", 0.222)
        self.spnPrecip2.setObjectName(_fromUtf8("spnPrecip2"))
        self.spnTemp1 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp1.setGeometry(QtCore.QRect(350, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp1.setFont(font)
        self.spnTemp1.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp1.setDecimals(3)
        self.spnTemp1.setMaximum(1.0)
        self.spnTemp1.setSingleStep(0.1)
        self.spnTemp1.setProperty("value", 0.126)
        self.spnTemp1.setObjectName(_fromUtf8("spnTemp1"))
        self.label_28 = QtGui.QLabel(self.tab)
        self.label_28.setGeometry(QtCore.QRect(570, 380, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.cboStep = QtGui.QComboBox(self.tab)
        self.cboStep.setGeometry(QtCore.QRect(350, 180, 241, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.cboStep.setFont(font)
        self.cboStep.setObjectName(_fromUtf8("cboStep"))
        self.cboStep.addItem(_fromUtf8(""))
        self.cboStep.addItem(_fromUtf8(""))
        self.cboStep.addItem(_fromUtf8(""))
        self.spnTemp6 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp6.setGeometry(QtCore.QRect(900, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp6.setFont(font)
        self.spnTemp6.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp6.setDecimals(3)
        self.spnTemp6.setMaximum(1.0)
        self.spnTemp6.setSingleStep(0.1)
        self.spnTemp6.setProperty("value", 0.876)
        self.spnTemp6.setObjectName(_fromUtf8("spnTemp6"))
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(10, 180, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.spnTemp3 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp3.setGeometry(QtCore.QRect(570, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp3.setFont(font)
        self.spnTemp3.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp3.setDecimals(3)
        self.spnTemp3.setMaximum(1.0)
        self.spnTemp3.setSingleStep(0.1)
        self.spnTemp3.setProperty("value", 0.406)
        self.spnTemp3.setObjectName(_fromUtf8("spnTemp3"))
        self.spnPrecip4 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip4.setGeometry(QtCore.QRect(680, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip4.setFont(font)
        self.spnPrecip4.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip4.setDecimals(3)
        self.spnPrecip4.setMaximum(1.0)
        self.spnPrecip4.setSingleStep(0.1)
        self.spnPrecip4.setProperty("value", 0.764)
        self.spnPrecip4.setObjectName(_fromUtf8("spnPrecip4"))
        self.label_23 = QtGui.QLabel(self.tab)
        self.label_23.setGeometry(QtCore.QRect(10, 460, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.spnTemp4 = QtGui.QDoubleSpinBox(self.tab)
        self.spnTemp4.setGeometry(QtCore.QRect(680, 500, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnTemp4.setFont(font)
        self.spnTemp4.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnTemp4.setDecimals(3)
        self.spnTemp4.setMaximum(1.0)
        self.spnTemp4.setSingleStep(0.1)
        self.spnTemp4.setProperty("value", 0.561)
        self.spnTemp4.setObjectName(_fromUtf8("spnTemp4"))
        self.label_29 = QtGui.QLabel(self.tab)
        self.label_29.setGeometry(QtCore.QRect(10, 420, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.spnPrecip3 = QtGui.QDoubleSpinBox(self.tab)
        self.spnPrecip3.setGeometry(QtCore.QRect(570, 540, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnPrecip3.setFont(font)
        self.spnPrecip3.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnPrecip3.setDecimals(3)
        self.spnPrecip3.setMaximum(1.0)
        self.spnPrecip3.setSingleStep(0.1)
        self.spnPrecip3.setProperty("value", 0.493)
        self.spnPrecip3.setObjectName(_fromUtf8("spnPrecip3"))
        self.label_13 = QtGui.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(10, 300, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.btnRandomise = QtGui.QPushButton(self.tab)
        self.btnRandomise.setGeometry(QtCore.QRect(450, 60, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnRandomise.setFont(font)
        self.btnRandomise.setObjectName(_fromUtf8("btnRandomise"))
        self.spnSeed = QtGui.QSpinBox(self.tab)
        self.spnSeed.setGeometry(QtCore.QRect(350, 60, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.spnSeed.setFont(font)
        self.spnSeed.setMinimum(0)
        self.spnSeed.setMaximum(999999)
        self.spnSeed.setSingleStep(111111)
        self.spnSeed.setProperty("value", 111111)
        self.spnSeed.setObjectName(_fromUtf8("spnSeed"))
        self.grpBW = QtGui.QGroupBox(self.tab)
        self.grpBW.setGeometry(QtCore.QRect(350, 300, 171, 31))
        self.grpBW.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpBW.setTitle(_fromUtf8(""))
        self.grpBW.setObjectName(_fromUtf8("grpBW"))
        self.rdoBWYes = QtGui.QRadioButton(self.grpBW)
        self.rdoBWYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoBWYes.setObjectName(_fromUtf8("rdoBWYes"))
        self.rdoBWNo = QtGui.QRadioButton(self.grpBW)
        self.rdoBWNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoBWNo.setChecked(True)
        self.rdoBWNo.setObjectName(_fromUtf8("rdoBWNo"))
        self.grpVerbose = QtGui.QGroupBox(self.tab)
        self.grpVerbose.setGeometry(QtCore.QRect(350, 340, 171, 31))
        self.grpVerbose.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpVerbose.setTitle(_fromUtf8(""))
        self.grpVerbose.setObjectName(_fromUtf8("grpVerbose"))
        self.rdoVMYes = QtGui.QRadioButton(self.grpVerbose)
        self.rdoVMYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoVMYes.setObjectName(_fromUtf8("rdoVMYes"))
        self.rdoVMNo = QtGui.QRadioButton(self.grpVerbose)
        self.rdoVMNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoVMNo.setChecked(True)
        self.rdoVMNo.setObjectName(_fromUtf8("rdoVMNo"))
        self.grpGrayscale = QtGui.QGroupBox(self.tab)
        self.grpGrayscale.setGeometry(QtCore.QRect(350, 380, 171, 31))
        self.grpGrayscale.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpGrayscale.setTitle(_fromUtf8(""))
        self.grpGrayscale.setObjectName(_fromUtf8("grpGrayscale"))
        self.rdoGHYes = QtGui.QRadioButton(self.grpGrayscale)
        self.rdoGHYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoGHYes.setObjectName(_fromUtf8("rdoGHYes"))
        self.rdoGHNo = QtGui.QRadioButton(self.grpGrayscale)
        self.rdoGHNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoGHNo.setChecked(True)
        self.rdoGHNo.setObjectName(_fromUtf8("rdoGHNo"))
        self.grpSatellite = QtGui.QGroupBox(self.tab)
        self.grpSatellite.setGeometry(QtCore.QRect(350, 420, 171, 31))
        self.grpSatellite.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpSatellite.setTitle(_fromUtf8(""))
        self.grpSatellite.setObjectName(_fromUtf8("grpSatellite"))
        self.rdoSMYes = QtGui.QRadioButton(self.grpSatellite)
        self.rdoSMYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoSMYes.setObjectName(_fromUtf8("rdoSMYes"))
        self.rdoSMNo = QtGui.QRadioButton(self.grpSatellite)
        self.rdoSMNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoSMNo.setChecked(True)
        self.rdoSMNo.setObjectName(_fromUtf8("rdoSMNo"))
        self.grpRiver = QtGui.QGroupBox(self.tab)
        self.grpRiver.setGeometry(QtCore.QRect(790, 340, 171, 31))
        self.grpRiver.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpRiver.setTitle(_fromUtf8(""))
        self.grpRiver.setObjectName(_fromUtf8("grpRiver"))
        self.rdoRMYes = QtGui.QRadioButton(self.grpRiver)
        self.rdoRMYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoRMYes.setObjectName(_fromUtf8("rdoRMYes"))
        self.rdoRMNo = QtGui.QRadioButton(self.grpRiver)
        self.rdoRMNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoRMNo.setChecked(True)
        self.rdoRMNo.setObjectName(_fromUtf8("rdoRMNo"))
        self.grpScatter = QtGui.QGroupBox(self.tab)
        self.grpScatter.setGeometry(QtCore.QRect(790, 380, 171, 31))
        self.grpScatter.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpScatter.setTitle(_fromUtf8(""))
        self.grpScatter.setObjectName(_fromUtf8("grpScatter"))
        self.rdoSPYes = QtGui.QRadioButton(self.grpScatter)
        self.rdoSPYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoSPYes.setObjectName(_fromUtf8("rdoSPYes"))
        self.rdoSPNo = QtGui.QRadioButton(self.grpScatter)
        self.rdoSPNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoSPNo.setChecked(True)
        self.rdoSPNo.setObjectName(_fromUtf8("rdoSPNo"))
        self.grpProtocol = QtGui.QGroupBox(self.tab)
        self.grpProtocol.setGeometry(QtCore.QRect(790, 300, 171, 31))
        self.grpProtocol.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpProtocol.setTitle(_fromUtf8(""))
        self.grpProtocol.setObjectName(_fromUtf8("grpProtocol"))
        self.rdoPBYes = QtGui.QRadioButton(self.grpProtocol)
        self.rdoPBYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoPBYes.setChecked(True)
        self.rdoPBYes.setObjectName(_fromUtf8("rdoPBYes"))
        self.rdoPBNo = QtGui.QRadioButton(self.grpProtocol)
        self.rdoPBNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoPBNo.setChecked(False)
        self.rdoPBNo.setObjectName(_fromUtf8("rdoPBNo"))
        self.grpIce = QtGui.QGroupBox(self.tab)
        self.grpIce.setGeometry(QtCore.QRect(790, 420, 171, 31))
        self.grpIce.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpIce.setTitle(_fromUtf8(""))
        self.grpIce.setObjectName(_fromUtf8("grpIce"))
        self.rdoICMYes = QtGui.QRadioButton(self.grpIce)
        self.rdoICMYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoICMYes.setObjectName(_fromUtf8("rdoICMYes"))
        self.rdoICMNo = QtGui.QRadioButton(self.grpIce)
        self.rdoICMNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoICMNo.setChecked(True)
        self.rdoICMNo.setObjectName(_fromUtf8("rdoICMNo"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(-4, -8, 1121, 661))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_48791_biome_2.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spnRecursion = QtGui.QSpinBox(self.tab)
        self.spnRecursion.setGeometry(QtCore.QRect(680, 140, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.spnRecursion.setFont(font)
        self.spnRecursion.setMinimum(1000)
        self.spnRecursion.setMaximum(10000)
        self.spnRecursion.setSingleStep(500)
        self.spnRecursion.setProperty("value", 2000)
        self.spnRecursion.setObjectName(_fromUtf8("spnRecursion"))
        self.label_51 = QtGui.QLabel(self.tab)
        self.label_51.setGeometry(QtCore.QRect(460, 140, 151, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_51.setFont(font)
        self.label_51.setObjectName(_fromUtf8("label_51"))
        self.label_50 = QtGui.QLabel(self.tab)
        self.label_50.setGeometry(QtCore.QRect(570, 460, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_50.setFont(font)
        self.label_50.setObjectName(_fromUtf8("label_50"))
        self.grpIce_2 = QtGui.QGroupBox(self.tab)
        self.grpIce_2.setGeometry(QtCore.QRect(790, 460, 171, 31))
        self.grpIce_2.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpIce_2.setTitle(_fromUtf8(""))
        self.grpIce_2.setObjectName(_fromUtf8("grpIce_2"))
        self.rdoFadeYes = QtGui.QRadioButton(self.grpIce_2)
        self.rdoFadeYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoFadeYes.setChecked(True)
        self.rdoFadeYes.setObjectName(_fromUtf8("rdoFadeYes"))
        self.rdoFadeNo = QtGui.QRadioButton(self.grpIce_2)
        self.rdoFadeNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoFadeNo.setChecked(False)
        self.rdoFadeNo.setObjectName(_fromUtf8("rdoFadeNo"))
        self.label_2.raise_()
        self.txtWorld.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.spnWidth.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.spnHeight.raise_()
        self.label_12.raise_()
        self.spnPlates.raise_()
        self.label_14.raise_()
        self.label_31.raise_()
        self.cboData.raise_()
        self.cboFormat.raise_()
        self.label_32.raise_()
        self.btnWorld.raise_()
        self.line.raise_()
        self.label_22.raise_()
        self.spnOffset.raise_()
        self.spnTemp5.raise_()
        self.label_43.raise_()
        self.label_24.raise_()
        self.spnPrecip1.raise_()
        self.label_25.raise_()
        self.spnGamma.raise_()
        self.spnPrecip6.raise_()
        self.label_27.raise_()
        self.spnSea.raise_()
        self.label_26.raise_()
        self.label_30.raise_()
        self.label_21.raise_()
        self.label_20.raise_()
        self.spnTemp2.raise_()
        self.label_19.raise_()
        self.spnPrecip5.raise_()
        self.spnPrecip7.raise_()
        self.spnPrecip2.raise_()
        self.spnTemp1.raise_()
        self.label_28.raise_()
        self.cboStep.raise_()
        self.spnTemp6.raise_()
        self.label_9.raise_()
        self.spnTemp3.raise_()
        self.spnPrecip4.raise_()
        self.label_23.raise_()
        self.spnTemp4.raise_()
        self.label_29.raise_()
        self.spnPrecip3.raise_()
        self.label_13.raise_()
        self.btnRandomise.raise_()
        self.spnSeed.raise_()
        self.grpBW.raise_()
        self.grpVerbose.raise_()
        self.grpGrayscale.raise_()
        self.grpSatellite.raise_()
        self.grpRiver.raise_()
        self.grpScatter.raise_()
        self.grpProtocol.raise_()
        self.grpIce.raise_()
        self.spnRecursion.raise_()
        self.label_51.raise_()
        self.label_50.raise_()
        self.grpIce_2.raise_()
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tbAncient = QtGui.QWidget()
        self.tbAncient.setObjectName(_fromUtf8("tbAncient"))
        self.label_33 = QtGui.QLabel(self.tbAncient)
        self.label_33.setGeometry(QtCore.QRect(10, 20, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.label_34 = QtGui.QLabel(self.tbAncient)
        self.label_34.setGeometry(QtCore.QRect(10, 60, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.txtAncWorld = QtGui.QLineEdit(self.tbAncient)
        self.txtAncWorld.setGeometry(QtCore.QRect(350, 20, 331, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.txtAncWorld.setFont(font)
        self.txtAncWorld.setObjectName(_fromUtf8("txtAncWorld"))
        self.txtAncFile = QtGui.QLineEdit(self.tbAncient)
        self.txtAncFile.setGeometry(QtCore.QRect(350, 60, 331, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.txtAncFile.setFont(font)
        self.txtAncFile.setObjectName(_fromUtf8("txtAncFile"))
        self.btnAncWorld = QtGui.QPushButton(self.tbAncient)
        self.btnAncWorld.setGeometry(QtCore.QRect(690, 20, 89, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnAncWorld.setFont(font)
        self.btnAncWorld.setObjectName(_fromUtf8("btnAncWorld"))
        self.label_35 = QtGui.QLabel(self.tbAncient)
        self.label_35.setGeometry(QtCore.QRect(10, 100, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.spnResize = QtGui.QDoubleSpinBox(self.tbAncient)
        self.spnResize.setGeometry(QtCore.QRect(350, 100, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.spnResize.setFont(font)
        self.spnResize.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.spnResize.setMinimum(1.0)
        self.spnResize.setProperty("value", 1.0)
        self.spnResize.setObjectName(_fromUtf8("spnResize"))
        self.label_36 = QtGui.QLabel(self.tbAncient)
        self.label_36.setGeometry(QtCore.QRect(10, 140, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.label_37 = QtGui.QLabel(self.tbAncient)
        self.label_37.setGeometry(QtCore.QRect(10, 180, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.label_38 = QtGui.QLabel(self.tbAncient)
        self.label_38.setGeometry(QtCore.QRect(10, 220, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.label_39 = QtGui.QLabel(self.tbAncient)
        self.label_39.setGeometry(QtCore.QRect(10, 260, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.label_40 = QtGui.QLabel(self.tbAncient)
        self.label_40.setGeometry(QtCore.QRect(10, 300, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.label_41 = QtGui.QLabel(self.tbAncient)
        self.label_41.setGeometry(QtCore.QRect(10, 380, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_41.setFont(font)
        self.label_41.setObjectName(_fromUtf8("label_41"))
        self.label_42 = QtGui.QLabel(self.tbAncient)
        self.label_42.setGeometry(QtCore.QRect(10, 340, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_42.setFont(font)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.btnAncMap = QtGui.QPushButton(self.tbAncient)
        self.btnAncMap.setGeometry(QtCore.QRect(790, 20, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnAncMap.setFont(font)
        self.btnAncMap.setObjectName(_fromUtf8("btnAncMap"))
        self.cboAncData = QtGui.QComboBox(self.tbAncient)
        self.cboAncData.setGeometry(QtCore.QRect(350, 380, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.cboAncData.setFont(font)
        self.cboAncData.setObjectName(_fromUtf8("cboAncData"))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncData.addItem(_fromUtf8(""))
        self.cboAncFormat = QtGui.QComboBox(self.tbAncient)
        self.cboAncFormat.setGeometry(QtCore.QRect(350, 340, 331, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(12)
        self.cboAncFormat.setFont(font)
        self.cboAncFormat.setObjectName(_fromUtf8("cboAncFormat"))
        self.cboAncFormat.addItem(_fromUtf8(""))
        self.cboAncFormat.addItem(_fromUtf8(""))
        self.cboAncFormat.addItem(_fromUtf8(""))
        self.cboAncFormat.addItem(_fromUtf8(""))
        self.grpSea = QtGui.QGroupBox(self.tbAncient)
        self.grpSea.setGeometry(QtCore.QRect(350, 140, 201, 31))
        self.grpSea.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpSea.setTitle(_fromUtf8(""))
        self.grpSea.setObjectName(_fromUtf8("grpSea"))
        self.rdoSeaBlue = QtGui.QRadioButton(self.grpSea)
        self.rdoSeaBlue.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoSeaBlue.setObjectName(_fromUtf8("rdoSeaBlue"))
        self.rdoSeaBrown = QtGui.QRadioButton(self.grpSea)
        self.rdoSeaBrown.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoSeaBrown.setChecked(True)
        self.rdoSeaBrown.setObjectName(_fromUtf8("rdoSeaBrown"))
        self.grpBiomes = QtGui.QGroupBox(self.tbAncient)
        self.grpBiomes.setGeometry(QtCore.QRect(350, 180, 201, 31))
        self.grpBiomes.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpBiomes.setTitle(_fromUtf8(""))
        self.grpBiomes.setObjectName(_fromUtf8("grpBiomes"))
        self.rdoBiomesYes = QtGui.QRadioButton(self.grpBiomes)
        self.rdoBiomesYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoBiomesYes.setChecked(True)
        self.rdoBiomesYes.setObjectName(_fromUtf8("rdoBiomesYes"))
        self.rdoBiomesNo = QtGui.QRadioButton(self.grpBiomes)
        self.rdoBiomesNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoBiomesNo.setChecked(False)
        self.rdoBiomesNo.setObjectName(_fromUtf8("rdoBiomesNo"))
        self.grpMountains = QtGui.QGroupBox(self.tbAncient)
        self.grpMountains.setGeometry(QtCore.QRect(350, 220, 201, 31))
        self.grpMountains.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpMountains.setTitle(_fromUtf8(""))
        self.grpMountains.setObjectName(_fromUtf8("grpMountains"))
        self.rdoMountYes = QtGui.QRadioButton(self.grpMountains)
        self.rdoMountYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoMountYes.setChecked(True)
        self.rdoMountYes.setObjectName(_fromUtf8("rdoMountYes"))
        self.rdoMountNo = QtGui.QRadioButton(self.grpMountains)
        self.rdoMountNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoMountNo.setChecked(False)
        self.rdoMountNo.setObjectName(_fromUtf8("rdoMountNo"))
        self.grpRivers = QtGui.QGroupBox(self.tbAncient)
        self.grpRivers.setGeometry(QtCore.QRect(350, 260, 201, 31))
        self.grpRivers.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpRivers.setTitle(_fromUtf8(""))
        self.grpRivers.setObjectName(_fromUtf8("grpRivers"))
        self.rdoRiverYes = QtGui.QRadioButton(self.grpRivers)
        self.rdoRiverYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoRiverYes.setChecked(True)
        self.rdoRiverYes.setObjectName(_fromUtf8("rdoRiverYes"))
        self.rdoRiverNo = QtGui.QRadioButton(self.grpRivers)
        self.rdoRiverNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoRiverNo.setChecked(False)
        self.rdoRiverNo.setObjectName(_fromUtf8("rdoRiverNo"))
        self.grpBorder = QtGui.QGroupBox(self.tbAncient)
        self.grpBorder.setGeometry(QtCore.QRect(350, 300, 201, 31))
        self.grpBorder.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"font-weight: 500;\n"
"border:0;"))
        self.grpBorder.setTitle(_fromUtf8(""))
        self.grpBorder.setObjectName(_fromUtf8("grpBorder"))
        self.rdoLandYes = QtGui.QRadioButton(self.grpBorder)
        self.rdoLandYes.setGeometry(QtCore.QRect(10, 0, 86, 31))
        self.rdoLandYes.setChecked(True)
        self.rdoLandYes.setObjectName(_fromUtf8("rdoLandYes"))
        self.rdoLandNo = QtGui.QRadioButton(self.grpBorder)
        self.rdoLandNo.setGeometry(QtCore.QRect(120, 0, 86, 31))
        self.rdoLandNo.setChecked(False)
        self.rdoLandNo.setObjectName(_fromUtf8("rdoLandNo"))
        self.label_3 = QtGui.QLabel(self.tbAncient)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 1121, 661))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/ancient_map_seed_48791.png")))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_3.raise_()
        self.label_33.raise_()
        self.label_34.raise_()
        self.txtAncWorld.raise_()
        self.txtAncFile.raise_()
        self.btnAncWorld.raise_()
        self.label_35.raise_()
        self.spnResize.raise_()
        self.label_36.raise_()
        self.label_37.raise_()
        self.label_38.raise_()
        self.label_39.raise_()
        self.label_40.raise_()
        self.label_41.raise_()
        self.label_42.raise_()
        self.btnAncMap.raise_()
        self.cboAncData.raise_()
        self.cboAncFormat.raise_()
        self.grpSea.raise_()
        self.grpBiomes.raise_()
        self.grpMountains.raise_()
        self.grpRivers.raise_()
        self.grpBorder.raise_()
        self.tabWidget.addTab(self.tbAncient, _fromUtf8(""))
        self.tbMaps = QtGui.QWidget()
        self.tbMaps.setObjectName(_fromUtf8("tbMaps"))
        self.label_18 = QtGui.QLabel(self.tbMaps)
        self.label_18.setGeometry(QtCore.QRect(30, 20, 541, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_18.setWordWrap(True)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.lblImage = QtGui.QLabel(self.tbMaps)
        self.lblImage.setGeometry(QtCore.QRect(590, 90, 512, 512))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        self.lblImage.setFont(font)
        self.lblImage.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.lblImage.setFrameShape(QtGui.QFrame.Box)
        self.lblImage.setText(_fromUtf8(""))
        self.lblImage.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_48791_biome.png")))
        self.lblImage.setAlignment(QtCore.Qt.AlignCenter)
        self.lblImage.setWordWrap(True)
        self.lblImage.setObjectName(_fromUtf8("lblImage"))
        self.btnEM = QtGui.QPushButton(self.tbMaps)
        self.btnEM.setGeometry(QtCore.QRect(170, 90, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnEM.setFont(font)
        self.btnEM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnEM.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_elevation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEM.setIcon(icon)
        self.btnEM.setIconSize(QtCore.QSize(112, 112))
        self.btnEM.setObjectName(_fromUtf8("btnEM"))
        self.btnPM = QtGui.QPushButton(self.tbMaps)
        self.btnPM.setGeometry(QtCore.QRect(170, 280, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnPM.setFont(font)
        self.btnPM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnPM.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_precipitation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPM.setIcon(icon1)
        self.btnPM.setIconSize(QtCore.QSize(112, 112))
        self.btnPM.setFlat(True)
        self.btnPM.setObjectName(_fromUtf8("btnPM"))
        self.btnTM = QtGui.QPushButton(self.tbMaps)
        self.btnTM.setGeometry(QtCore.QRect(310, 470, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnTM.setFont(font)
        self.btnTM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnTM.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_temperature.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTM.setIcon(icon2)
        self.btnTM.setIconSize(QtCore.QSize(112, 112))
        self.btnTM.setFlat(True)
        self.btnTM.setObjectName(_fromUtf8("btnTM"))
        self.btnBM = QtGui.QPushButton(self.tbMaps)
        self.btnBM.setGeometry(QtCore.QRect(30, 90, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnBM.setFont(font)
        self.btnBM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnBM.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_biome.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBM.setIcon(icon3)
        self.btnBM.setIconSize(QtCore.QSize(112, 112))
        self.btnBM.setFlat(True)
        self.btnBM.setObjectName(_fromUtf8("btnBM"))
        self.btnOM = QtGui.QPushButton(self.tbMaps)
        self.btnOM.setGeometry(QtCore.QRect(30, 280, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnOM.setFont(font)
        self.btnOM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnOM.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_ocean.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOM.setIcon(icon4)
        self.btnOM.setIconSize(QtCore.QSize(112, 112))
        self.btnOM.setFlat(True)
        self.btnOM.setObjectName(_fromUtf8("btnOM"))
        self.btnRM = QtGui.QPushButton(self.tbMaps)
        self.btnRM.setGeometry(QtCore.QRect(310, 280, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnRM.setFont(font)
        self.btnRM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnRM.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_rivers.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRM.setIcon(icon5)
        self.btnRM.setIconSize(QtCore.QSize(112, 112))
        self.btnRM.setFlat(True)
        self.btnRM.setObjectName(_fromUtf8("btnRM"))
        self.btnGH = QtGui.QPushButton(self.tbMaps)
        self.btnGH.setGeometry(QtCore.QRect(310, 90, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnGH.setFont(font)
        self.btnGH.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnGH.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_grayscale.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnGH.setIcon(icon6)
        self.btnGH.setIconSize(QtCore.QSize(112, 112))
        self.btnGH.setFlat(True)
        self.btnGH.setObjectName(_fromUtf8("btnGH"))
        self.btnSP = QtGui.QPushButton(self.tbMaps)
        self.btnSP.setGeometry(QtCore.QRect(170, 470, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnSP.setFont(font)
        self.btnSP.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnSP.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_scatter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSP.setIcon(icon7)
        self.btnSP.setIconSize(QtCore.QSize(112, 112))
        self.btnSP.setFlat(True)
        self.btnSP.setObjectName(_fromUtf8("btnSP"))
        self.btnSM = QtGui.QPushButton(self.tbMaps)
        self.btnSM.setGeometry(QtCore.QRect(30, 470, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnSM.setFont(font)
        self.btnSM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnSM.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_57829_satellite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSM.setIcon(icon8)
        self.btnSM.setIconSize(QtCore.QSize(112, 112))
        self.btnSM.setFlat(True)
        self.btnSM.setObjectName(_fromUtf8("btnSM"))
        self.btnICM = QtGui.QPushButton(self.tbMaps)
        self.btnICM.setGeometry(QtCore.QRect(450, 280, 128, 128))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.btnICM.setFont(font)
        self.btnICM.setStyleSheet(_fromUtf8("font-family: Open Sans;\n"
"font-size: 16px;"))
        self.btnICM.setFlat(True)
        self.btnICM.setObjectName(_fromUtf8("btnICM"))
        self.label_4 = QtGui.QLabel(self.tbMaps)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1121, 661))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_48791_elevation.png")))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tbMaps)
        self.label_5.setGeometry(QtCore.QRect(30, 70, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_15 = QtGui.QLabel(self.tbMaps)
        self.label_15.setGeometry(QtCore.QRect(170, 70, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(self.tbMaps)
        self.label_16.setGeometry(QtCore.QRect(310, 70, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(self.tbMaps)
        self.label_17.setGeometry(QtCore.QRect(30, 260, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_44 = QtGui.QLabel(self.tbMaps)
        self.label_44.setGeometry(QtCore.QRect(310, 260, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_44.setFont(font)
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName(_fromUtf8("label_44"))
        self.label_45 = QtGui.QLabel(self.tbMaps)
        self.label_45.setGeometry(QtCore.QRect(170, 260, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_45.setFont(font)
        self.label_45.setAlignment(QtCore.Qt.AlignCenter)
        self.label_45.setObjectName(_fromUtf8("label_45"))
        self.label_46 = QtGui.QLabel(self.tbMaps)
        self.label_46.setGeometry(QtCore.QRect(450, 260, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_46.setFont(font)
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName(_fromUtf8("label_46"))
        self.label_47 = QtGui.QLabel(self.tbMaps)
        self.label_47.setGeometry(QtCore.QRect(30, 450, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_47.setFont(font)
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName(_fromUtf8("label_47"))
        self.label_48 = QtGui.QLabel(self.tbMaps)
        self.label_48.setGeometry(QtCore.QRect(310, 450, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_48.setFont(font)
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setObjectName(_fromUtf8("label_48"))
        self.label_49 = QtGui.QLabel(self.tbMaps)
        self.label_49.setGeometry(QtCore.QRect(170, 450, 131, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label_49.setFont(font)
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName(_fromUtf8("label_49"))
        self.label_4.raise_()
        self.label_18.raise_()
        self.lblImage.raise_()
        self.btnEM.raise_()
        self.btnPM.raise_()
        self.btnTM.raise_()
        self.btnBM.raise_()
        self.btnOM.raise_()
        self.btnRM.raise_()
        self.btnGH.raise_()
        self.btnSP.raise_()
        self.btnSM.raise_()
        self.btnICM.raise_()
        self.label_5.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_44.raise_()
        self.label_45.raise_()
        self.label_46.raise_()
        self.label_47.raise_()
        self.label_48.raise_()
        self.label_49.raise_()
        self.tabWidget.addTab(self.tbMaps, _fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(10, 0, 1141, 81))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Open Sans"))
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 64, 64))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_48791_elevation.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_52 = QtGui.QLabel(self.centralWidget)
        self.label_52.setGeometry(QtCore.QRect(1080, 10, 64, 64))
        self.label_52.setText(_fromUtf8(""))
        self.label_52.setPixmap(QtGui.QPixmap(_fromUtf8(":/Images/seed_48791_elevation.png")))
        self.label_52.setScaledContents(True)
        self.label_52.setObjectName(_fromUtf8("label_52"))
        WorldEngine.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(WorldEngine)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1158, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        WorldEngine.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(WorldEngine)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        WorldEngine.setStatusBar(self.statusBar)
        self.actionNew = QtGui.QAction(WorldEngine)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(WorldEngine)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(WorldEngine)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionClose = QtGui.QAction(WorldEngine)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionSave_World_Map = QtGui.QAction(WorldEngine)
        self.actionSave_World_Map.setObjectName(_fromUtf8("actionSave_World_Map"))
        self.actionSave_Rivers_Map = QtGui.QAction(WorldEngine)
        self.actionSave_Rivers_Map.setObjectName(_fromUtf8("actionSave_Rivers_Map"))
        self.actionSave_Heightmap = QtGui.QAction(WorldEngine)
        self.actionSave_Heightmap.setObjectName(_fromUtf8("actionSave_Heightmap"))
        self.actionSave_Scatter_Plot = QtGui.QAction(WorldEngine)
        self.actionSave_Scatter_Plot.setObjectName(_fromUtf8("actionSave_Scatter_Plot"))
        self.actionHelp_File = QtGui.QAction(WorldEngine)
        self.actionHelp_File.setObjectName(_fromUtf8("actionHelp_File"))
        self.actionAbout = QtGui.QAction(WorldEngine)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionSet_Output_Directory = QtGui.QAction(WorldEngine)
        self.actionSet_Output_Directory.setObjectName(_fromUtf8("actionSet_Output_Directory"))
        self.actionVersion_Information = QtGui.QAction(WorldEngine)
        self.actionVersion_Information.setObjectName(_fromUtf8("actionVersion_Information"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSet_Output_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp_File)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionVersion_Information)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(WorldEngine)
        self.tabWidget.setCurrentIndex(0)
        self.cboData.setCurrentIndex(3)
        self.cboFormat.setCurrentIndex(3)
        self.cboAncData.setCurrentIndex(3)
        self.cboAncFormat.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(WorldEngine)
        WorldEngine.setTabOrder(self.tabWidget, self.txtWorld)
        WorldEngine.setTabOrder(self.txtWorld, self.spnSeed)
        WorldEngine.setTabOrder(self.spnSeed, self.btnRandomise)
        WorldEngine.setTabOrder(self.btnRandomise, self.spnWidth)
        WorldEngine.setTabOrder(self.spnWidth, self.spnHeight)
        WorldEngine.setTabOrder(self.spnHeight, self.spnPlates)
        WorldEngine.setTabOrder(self.spnPlates, self.spnRecursion)
        WorldEngine.setTabOrder(self.spnRecursion, self.cboStep)
        WorldEngine.setTabOrder(self.cboStep, self.cboFormat)
        WorldEngine.setTabOrder(self.cboFormat, self.cboData)
        WorldEngine.setTabOrder(self.cboData, self.rdoBWYes)
        WorldEngine.setTabOrder(self.rdoBWYes, self.rdoBWNo)
        WorldEngine.setTabOrder(self.rdoBWNo, self.rdoPBYes)
        WorldEngine.setTabOrder(self.rdoPBYes, self.rdoPBNo)
        WorldEngine.setTabOrder(self.rdoPBNo, self.rdoVMYes)
        WorldEngine.setTabOrder(self.rdoVMYes, self.rdoVMNo)
        WorldEngine.setTabOrder(self.rdoVMNo, self.rdoRMYes)
        WorldEngine.setTabOrder(self.rdoRMYes, self.rdoRMNo)
        WorldEngine.setTabOrder(self.rdoRMNo, self.rdoGHYes)
        WorldEngine.setTabOrder(self.rdoGHYes, self.rdoGHNo)
        WorldEngine.setTabOrder(self.rdoGHNo, self.rdoSPYes)
        WorldEngine.setTabOrder(self.rdoSPYes, self.rdoSPNo)
        WorldEngine.setTabOrder(self.rdoSPNo, self.rdoSMYes)
        WorldEngine.setTabOrder(self.rdoSMYes, self.rdoSMNo)
        WorldEngine.setTabOrder(self.rdoSMNo, self.rdoICMYes)
        WorldEngine.setTabOrder(self.rdoICMYes, self.rdoICMNo)
        WorldEngine.setTabOrder(self.rdoICMNo, self.spnSea)
        WorldEngine.setTabOrder(self.spnSea, self.rdoFadeYes)
        WorldEngine.setTabOrder(self.rdoFadeYes, self.rdoFadeNo)
        WorldEngine.setTabOrder(self.rdoFadeNo, self.spnTemp1)
        WorldEngine.setTabOrder(self.spnTemp1, self.spnTemp2)
        WorldEngine.setTabOrder(self.spnTemp2, self.spnTemp3)
        WorldEngine.setTabOrder(self.spnTemp3, self.spnTemp4)
        WorldEngine.setTabOrder(self.spnTemp4, self.spnTemp5)
        WorldEngine.setTabOrder(self.spnTemp5, self.spnTemp6)
        WorldEngine.setTabOrder(self.spnTemp6, self.spnPrecip1)
        WorldEngine.setTabOrder(self.spnPrecip1, self.spnPrecip2)
        WorldEngine.setTabOrder(self.spnPrecip2, self.spnPrecip3)
        WorldEngine.setTabOrder(self.spnPrecip3, self.spnPrecip4)
        WorldEngine.setTabOrder(self.spnPrecip4, self.spnPrecip5)
        WorldEngine.setTabOrder(self.spnPrecip5, self.spnPrecip6)
        WorldEngine.setTabOrder(self.spnPrecip6, self.spnPrecip7)
        WorldEngine.setTabOrder(self.spnPrecip7, self.spnGamma)
        WorldEngine.setTabOrder(self.spnGamma, self.spnOffset)
        WorldEngine.setTabOrder(self.spnOffset, self.btnWorld)
        WorldEngine.setTabOrder(self.btnWorld, self.txtAncWorld)
        WorldEngine.setTabOrder(self.txtAncWorld, self.btnAncWorld)
        WorldEngine.setTabOrder(self.btnAncWorld, self.txtAncFile)
        WorldEngine.setTabOrder(self.txtAncFile, self.spnResize)
        WorldEngine.setTabOrder(self.spnResize, self.rdoSeaBlue)
        WorldEngine.setTabOrder(self.rdoSeaBlue, self.rdoSeaBrown)
        WorldEngine.setTabOrder(self.rdoSeaBrown, self.rdoBiomesYes)
        WorldEngine.setTabOrder(self.rdoBiomesYes, self.rdoBiomesNo)
        WorldEngine.setTabOrder(self.rdoBiomesNo, self.rdoMountYes)
        WorldEngine.setTabOrder(self.rdoMountYes, self.rdoMountNo)
        WorldEngine.setTabOrder(self.rdoMountNo, self.rdoRiverYes)
        WorldEngine.setTabOrder(self.rdoRiverYes, self.rdoRiverNo)
        WorldEngine.setTabOrder(self.rdoRiverNo, self.rdoLandYes)
        WorldEngine.setTabOrder(self.rdoLandYes, self.rdoLandNo)
        WorldEngine.setTabOrder(self.rdoLandNo, self.cboAncFormat)
        WorldEngine.setTabOrder(self.cboAncFormat, self.cboAncData)
        WorldEngine.setTabOrder(self.cboAncData, self.btnAncMap)
        WorldEngine.setTabOrder(self.btnAncMap, self.btnBM)
        WorldEngine.setTabOrder(self.btnBM, self.btnEM)
        WorldEngine.setTabOrder(self.btnEM, self.btnGH)
        WorldEngine.setTabOrder(self.btnGH, self.btnOM)
        WorldEngine.setTabOrder(self.btnOM, self.btnPM)
        WorldEngine.setTabOrder(self.btnPM, self.btnRM)
        WorldEngine.setTabOrder(self.btnRM, self.btnICM)
        WorldEngine.setTabOrder(self.btnICM, self.btnSM)
        WorldEngine.setTabOrder(self.btnSM, self.btnSP)
        WorldEngine.setTabOrder(self.btnSP, self.btnTM)

    def retranslateUi(self, WorldEngine):
        WorldEngine.setWindowTitle(_translate("WorldEngine", "WorldEngine", None))
        self.txtWorld.setText(_translate("WorldEngine", "Test_World", None))
        self.label_7.setText(_translate("WorldEngine", "World Name:", None))
        self.label_8.setText(_translate("WorldEngine", "World Seed:", None))
        self.label_10.setText(_translate("WorldEngine", "Width:", None))
        self.label_11.setText(_translate("WorldEngine", "Height:", None))
        self.label_12.setText(_translate("WorldEngine", "No. of Plates:", None))
        self.label_14.setText(_translate("WorldEngine", "*GCC = Gamma Correction Curve", None))
        self.label_31.setText(_translate("WorldEngine", "Export Format:", None))
        self.cboData.setItemText(0, _translate("WorldEngine", "int8", None))
        self.cboData.setItemText(1, _translate("WorldEngine", "uint8", None))
        self.cboData.setItemText(2, _translate("WorldEngine", "int16", None))
        self.cboData.setItemText(3, _translate("WorldEngine", "uint16", None))
        self.cboData.setItemText(4, _translate("WorldEngine", "int32", None))
        self.cboData.setItemText(5, _translate("WorldEngine", "uint32", None))
        self.cboData.setItemText(6, _translate("WorldEngine", "int64", None))
        self.cboData.setItemText(7, _translate("WorldEngine", "uint64", None))
        self.cboData.setItemText(8, _translate("WorldEngine", "float16", None))
        self.cboData.setItemText(9, _translate("WorldEngine", "float32", None))
        self.cboData.setItemText(10, _translate("WorldEngine", "float64", None))
        self.cboFormat.setItemText(0, _translate("WorldEngine", "Arc/Info ASCII Grid", None))
        self.cboFormat.setItemText(1, _translate("WorldEngine", "ACE2", None))
        self.cboFormat.setItemText(2, _translate("WorldEngine", "ADRG/ARC Digitilized Raster Graphics (.gen/.thf)", None))
        self.cboFormat.setItemText(3, _translate("WorldEngine", "png", None))
        self.label_32.setText(_translate("WorldEngine", "Export Data Type:", None))
        self.btnWorld.setText(_translate("WorldEngine", "Generate World", None))
        self.label_22.setText(_translate("WorldEngine", "Generate Grayscale Heightmap?", None))
        self.label_43.setText(_translate("WorldEngine", "<html><head/><body><p><span style=\" font-weight:600; color:#ff9930;\">NOTE:</span><span style=\" color:#ff9930;\"> The options in this Section are </span><span style=\" font-weight:600; color:#ff9930;\">NOT</span><span style=\" color:#ff9930;\"> required if </span><span style=\" font-weight:600; color:#ff9930;\">Step</span><span style=\" color:#ff9930;\"> is set to </span><span style=\" font-weight:600; color:#ff9930;\">Plates</span></p></body></html>", None))
        self.label_24.setText(_translate("WorldEngine", "Temperature Range:", None))
        self.label_25.setText(_translate("WorldEngine", "Precipitation Range:", None))
        self.label_27.setText(_translate("WorldEngine", "GCC* Offset:", None))
        self.label_26.setText(_translate("WorldEngine", "GCC* Gamma Value:", None))
        self.label_30.setText(_translate("WorldEngine", "Generate Ice Caps Map?", None))
        self.label_21.setText(_translate("WorldEngine", "Generate River Map?", None))
        self.label_20.setText(_translate("WorldEngine", "Enable Verbose Messages?", None))
        self.label_19.setText(_translate("WorldEngine", "Use Protocol Buffer?", None))
        self.label_28.setText(_translate("WorldEngine", "Generate Scatter Plot?", None))
        self.cboStep.setItemText(0, _translate("WorldEngine", "full", None))
        self.cboStep.setItemText(1, _translate("WorldEngine", "plates", None))
        self.cboStep.setItemText(2, _translate("WorldEngine", "precipitations", None))
        self.label_9.setText(_translate("WorldEngine", "Step:", None))
        self.label_23.setText(_translate("WorldEngine", "Sea Level Elevation Cut Off:", None))
        self.label_29.setText(_translate("WorldEngine", "Generate Satellite Map?", None))
        self.label_13.setText(_translate("WorldEngine", "Create Black & White Images?", None))
        self.btnRandomise.setText(_translate("WorldEngine", "Randomise", None))
        self.rdoBWYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoBWNo.setText(_translate("WorldEngine", "No", None))
        self.rdoVMYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoVMNo.setText(_translate("WorldEngine", "No", None))
        self.rdoGHYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoGHNo.setText(_translate("WorldEngine", "No", None))
        self.rdoSMYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoSMNo.setText(_translate("WorldEngine", "No", None))
        self.rdoRMYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoRMNo.setText(_translate("WorldEngine", "No", None))
        self.rdoSPYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoSPNo.setText(_translate("WorldEngine", "No", None))
        self.rdoPBYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoPBNo.setText(_translate("WorldEngine", "No", None))
        self.rdoICMYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoICMNo.setText(_translate("WorldEngine", "No", None))
        self.label_51.setText(_translate("WorldEngine", "Recursion Limit:", None))
        self.label_50.setText(_translate("WorldEngine", "Fade Borders?", None))
        self.rdoFadeYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoFadeNo.setText(_translate("WorldEngine", "No", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("WorldEngine", "World Generator", None))
        self.label_33.setText(_translate("WorldEngine", "World File:", None))
        self.label_34.setText(_translate("WorldEngine", "File Name:", None))
        self.txtAncWorld.setText(_translate("WorldEngine", "Test_World", None))
        self.txtAncFile.setText(_translate("WorldEngine", "Ancient_World_1", None))
        self.btnAncWorld.setText(_translate("WorldEngine", "...", None))
        self.label_35.setText(_translate("WorldEngine", "Resize Factor:", None))
        self.label_36.setText(_translate("WorldEngine", "Sea Colour:", None))
        self.label_37.setText(_translate("WorldEngine", "Draw Biomes?", None))
        self.label_38.setText(_translate("WorldEngine", "Draw Mountains?", None))
        self.label_39.setText(_translate("WorldEngine", "Draw Rivers?", None))
        self.label_40.setText(_translate("WorldEngine", "Draw Outer Land Border?", None))
        self.label_41.setText(_translate("WorldEngine", "Export Data Type:", None))
        self.label_42.setText(_translate("WorldEngine", "Export Format:", None))
        self.btnAncMap.setText(_translate("WorldEngine", "Generate Map", None))
        self.cboAncData.setItemText(0, _translate("WorldEngine", "int8", None))
        self.cboAncData.setItemText(1, _translate("WorldEngine", "uint8", None))
        self.cboAncData.setItemText(2, _translate("WorldEngine", "int16", None))
        self.cboAncData.setItemText(3, _translate("WorldEngine", "uint16", None))
        self.cboAncData.setItemText(4, _translate("WorldEngine", "int32", None))
        self.cboAncData.setItemText(5, _translate("WorldEngine", "uint32", None))
        self.cboAncData.setItemText(6, _translate("WorldEngine", "int64", None))
        self.cboAncData.setItemText(7, _translate("WorldEngine", "uint64", None))
        self.cboAncData.setItemText(8, _translate("WorldEngine", "float16", None))
        self.cboAncData.setItemText(9, _translate("WorldEngine", "float32", None))
        self.cboAncData.setItemText(10, _translate("WorldEngine", "float64", None))
        self.cboAncFormat.setItemText(0, _translate("WorldEngine", "Arc/Info ASCII Grid", None))
        self.cboAncFormat.setItemText(1, _translate("WorldEngine", "ACE2", None))
        self.cboAncFormat.setItemText(2, _translate("WorldEngine", "ADRG/ARC Digitilized Raster Graphics (.gen/.thf)", None))
        self.cboAncFormat.setItemText(3, _translate("WorldEngine", "png", None))
        self.rdoSeaBlue.setText(_translate("WorldEngine", "Blue", None))
        self.rdoSeaBrown.setText(_translate("WorldEngine", "Brown", None))
        self.rdoBiomesYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoBiomesNo.setText(_translate("WorldEngine", "No", None))
        self.rdoMountYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoMountNo.setText(_translate("WorldEngine", "No", None))
        self.rdoRiverYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoRiverNo.setText(_translate("WorldEngine", "No", None))
        self.rdoLandYes.setText(_translate("WorldEngine", "Yes", None))
        self.rdoLandNo.setText(_translate("WorldEngine", "No", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbAncient), _translate("WorldEngine", "Ancient Map Generator", None))
        self.label_18.setText(_translate("WorldEngine", "Click on one of the generated Maps below to view a larger version", None))
        self.btnEM.setToolTip(_translate("WorldEngine", "Elevation Map", None))
        self.btnPM.setToolTip(_translate("WorldEngine", "Precipitation Map", None))
        self.btnTM.setToolTip(_translate("WorldEngine", "Temperature Map", None))
        self.btnBM.setToolTip(_translate("WorldEngine", "Biome Map", None))
        self.btnOM.setToolTip(_translate("WorldEngine", "Ocean Map", None))
        self.btnRM.setToolTip(_translate("WorldEngine", "Rivers Map", None))
        self.btnGH.setToolTip(_translate("WorldEngine", "Grayscale Heightmap", None))
        self.btnSP.setToolTip(_translate("WorldEngine", "Scatter Plot", None))
        self.btnSM.setToolTip(_translate("WorldEngine", "Satellite Map", None))
        self.btnICM.setToolTip(_translate("WorldEngine", "Ice Caps Map", None))
        self.btnICM.setText(_translate("WorldEngine", "Ice Caps\n"
"Map", None))
        self.label_5.setText(_translate("WorldEngine", "Biome Map", None))
        self.label_15.setText(_translate("WorldEngine", "Elevation Map", None))
        self.label_16.setText(_translate("WorldEngine", "Grayscale Heightmap", None))
        self.label_17.setText(_translate("WorldEngine", "Ocean Map", None))
        self.label_44.setText(_translate("WorldEngine", "Rivers Map", None))
        self.label_45.setText(_translate("WorldEngine", "Precipitation Map", None))
        self.label_46.setText(_translate("WorldEngine", "Ice Caps Map", None))
        self.label_47.setText(_translate("WorldEngine", "Satellite Map", None))
        self.label_48.setText(_translate("WorldEngine", "Temperature Map", None))
        self.label_49.setText(_translate("WorldEngine", "Scatter Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbMaps), _translate("WorldEngine", "Generated Maps", None))
        self.label_6.setText(_translate("WorldEngine", "<html><head/><body><p>WorldEngine - a World Generator <span style=\" font-size:12pt;\">by Bret Curtis and Federico Tomassetti</span></p></body></html>", None))
        self.menuFile.setTitle(_translate("WorldEngine", "File", None))
        self.menuHelp.setTitle(_translate("WorldEngine", "Help", None))
        self.actionNew.setText(_translate("WorldEngine", "New", None))
        self.actionOpen.setText(_translate("WorldEngine", "Open", None))
        self.actionSave.setText(_translate("WorldEngine", "Save", None))
        self.actionClose.setText(_translate("WorldEngine", "Close", None))
        self.actionSave_World_Map.setText(_translate("WorldEngine", "Save World Map", None))
        self.actionSave_Rivers_Map.setText(_translate("WorldEngine", "Save Rivers Map", None))
        self.actionSave_Heightmap.setText(_translate("WorldEngine", "Save Heightmap", None))
        self.actionSave_Scatter_Plot.setText(_translate("WorldEngine", "Save Scatter Plot", None))
        self.actionHelp_File.setText(_translate("WorldEngine", "Help File", None))
        self.actionAbout.setText(_translate("WorldEngine", "About", None))
        self.actionSet_Output_Directory.setText(_translate("WorldEngine", "Set Output Directory", None))
        self.actionVersion_Information.setText(_translate("WorldEngine", "Version Information", None))


