#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example of an image viewer with zoom
#
# Created: Thu Feb 25 19:54:49 2010
#      by: PyQt4 UI code generator 4.4.4
#
# Author: Vincent Vande Vyvre <vins@swing.be>
#
# Note: before use, change the line 63

import os
import time
import glob

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(900, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.verticalLayout.addWidget(self.view)
        self.horizontalLayout = QtGui.QHBoxLayout()
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toolButton_3 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_3.setIconSize(QtCore.QSize(48, 24))
        self.toolButton_3.setText("Previous")
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.toolButton_4 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_4.setIconSize(QtCore.QSize(48, 24))
        self.toolButton_4.setText("Next")
        self.horizontalLayout.addWidget(self.toolButton_4)
        spacerItem1 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.toolButton_6 = QtGui.QToolButton(self.centralwidget)
        self.toolButton_6.setText("Quit")
        self.horizontalLayout.addWidget(self.toolButton_6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("speedyView")
        MainWindow.show()
        QtCore.QCoreApplication.processEvents()

        QtCore.QObject.connect(ui.toolButton_3, QtCore.SIGNAL("clicked()"), self.prec)
        QtCore.QObject.connect(ui.toolButton_4, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(ui.toolButton_6, QtCore.SIGNAL("clicked()"), exit)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.centralwidget.wheelEvent = self.wheel_event

        self.set_view()

    def set_view(self):
        in_folder = "D:/Users/Simon/git/WorldEngine/worldengine/"
        chain = in_folder + "*.png"
        self.images = glob.glob(chain)
        self.images.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
        self.zoom_step = 0.04
        self.w_vsize = self.view.size().width()
        self.h_vsize = self.view.size().height()
        if self.w_vsize <= self.h_vsize:
            self.max_vsize = self.w_vsize
        else:
            self.max_vsize = self.h_vsize
        self.l_pix = ["", "", ""]

        self.i_pointer = 0
        self.p_pointer = 0
        self.load_current()
        self.p_pointer = 1
        self.load_next()
        self.p_pointer = 2
        self.load_prec()
        self.p_pointer = 0

    def next(self):
        self.i_pointer += 1
        if self.i_pointer == len(self.images):
            self.i_pointer = 0
        self.p_view = self.c_view
        self.c_view = self.n_view
        self.view_current()
        if self.p_pointer == 0:
            self.p_pointer = 2
            self.load_next()
            self.p_pointer = 1
        elif self.p_pointer == 1:
            self.p_pointer = 0
            self.load_next()
            self.p_pointer = 2
        else:
            self.p_pointer = 1
            self.load_next()
            self.p_pointer = 0

    def prec(self):
        self.i_pointer -= 1
        if self.i_pointer <= 0:
            self.i_pointer = len(self.images)-1
        self.n_view = self.c_view
        self.c_view = self.p_view
        self.view_current()
        if self.p_pointer == 0:
            self.p_pointer = 1
            self.load_prec()
            self.p_pointer = 2
        elif self.p_pointer == 1:
            self.p_pointer = 2
            self.load_prec()
            self.p_pointer = 0
        else:
            self.p_pointer = 0
            self.load_prec()
            self.p_pointer = 1

       
    def view_current(self):
        size_img = self.c_view.size()
        wth, hgt = QtCore.QSize.width(size_img), QtCore.QSize.height(size_img)
        self.scene.clear()
        self.scene.setSceneRect(0, 0, wth, hgt)
        self.scene.addPixmap(self.c_view)
        QtCore.QCoreApplication.processEvents()

    def load_current(self):
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[self.i_pointer])
        self.c_view = self.l_pix[self.p_pointer].scaled(self.max_vsize, self.max_vsize, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation)
        #change the previous line with QtCore.Qt.SmoothTransformation eventually
        self.view_current()

    def load_next(self):
        if self.i_pointer == len(self.images)-1:
            p = 0
        else:
            p = self.i_pointer + 1
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[p])
        self.n_view = self.l_pix[self.p_pointer].scaled(self.max_vsize, 
                                            self.max_vsize, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation)

    def load_prec(self):
        if self.i_pointer == 0:
            p = len(self.images)-1
        else:
            p = self.i_pointer - 1
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[p])
        self.p_view = self.l_pix[self.p_pointer].scaled(self.max_vsize, 
                                            self.max_vsize, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation)

    def wheel_event (self, event):
        numDegrees = event.delta() / 8
        numSteps = numDegrees / 15.0
        self.zoom(numSteps)
        event.accept()

    def zoom(self, step):
        self.scene.clear()
        w = self.c_view.size().width()
        h = self.c_view.size().height()
        w, h = w * (1 + self.zoom_step*step), h * (1 + self.zoom_step*step)
        self.c_view = self.l_pix[self.p_pointer].scaled(w, h, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation)
        self.view_current()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
''' import sys
import numpy

import generation as geo
from draw import draw_ancientmap_on_file, draw_biome_on_file, draw_ocean_on_file, \
    draw_precipitation_on_file, draw_grayscale_heightmap_on_file, draw_simple_elevation_on_file, \
    draw_temperature_levels_on_file, draw_riversmap_on_file, draw_scatter_plot_on_file, \
    draw_satellite_on_file, draw_icecaps_on_file
from plates import world_gen, generate_plates_simulation
from imex import export
from step import Step
from model.world import World, Size, GenerationParameters
from version import __version__
import world
from PyQt4.QtCore import pyqtSlot

try:
    from hdf5_serialization import save_world_to_hdf5
    HDF5_AVAILABLE = True
except:
    HDF5_AVAILABLE = False

VERSION = __version__

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4 import QtOpenGL

FORM_1, BASE_1 = uic.loadUiType("worldengine.ui")
FORM_2, BASE_2 = uic.loadUiType("popup.ui")
FORM_3, BASE_3 = uic.loadUiType("dialog.ui")
FORM_4, BASE_4 = uic.loadUiType("test_river.ui")

class MyApp(FORM_4, BASE_4):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        
        self.connect(self.btnRiver, QtCore.SIGNAL("released()"), self.btnRiver_Clicked)
        self.connect(self.spnZoom, QtCore.SIGNAL("valueChanged(int)"), self.spnZoom_Changed)

        self.grView = self.gvMain
        self.grView.setViewport(QtOpenGL.QGLWidget())
        self.grScene = QtGui.QGraphicsScene()
        self.tPix = QtGui.QPixmap('seed_11111_elevation.png')
        
        self.iHeight = self.tPix.height()
        self.iWidth = self.tPix.width()
        
        self.tPix = self.tPix.scaled(768, 768, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.spnZoom.setValue(75)

        self.grView.centerOn(0, 0)

        self.tPixItem = QtGui.QGraphicsPixmapItem(self.tPix)        
        self.grScene.addItem(self.tPixItem)
        self.grView.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.grView.setScene(self.grScene)
        self.grView.show()
        
    def btnRiver_Clicked(self):
        from random import randint

    def spnZoom_Changed(self, inVal):       
        iScaleX = self.iWidth * inVal / 100
        iScaleY = self.iHeight * inVal / 100
        
        if inVal == 75:
            self.tPix = QtGui.QPixmap('seed_11111_elevation.png')
            self.grScene.clear()
            self.grScene.setSceneRect(0, 0, iScaleX, iScaleY)
            self.grScene.addPixmap(self.tPix)
        else:
            self.tPix = self.tPix.scaled(iScaleX, iScaleY, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.grScene.clear()
            self.grScene.setSceneRect(0, 0, iScaleX, iScaleY)
            self.grScene.addPixmap(self.tPix)

if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    FORM = MyApp()
    FORM.show()
    APP.exec_()
'''