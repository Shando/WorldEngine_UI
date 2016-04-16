import sys
import os
import numpy
import json

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
from os import path

FORM_1, BASE_1 = uic.loadUiType("new_gui.ui")
FORM_2, BASE_2 = uic.loadUiType("popup.ui")
FORM_3, BASE_3 = uic.loadUiType("dialog.ui")

class FORM2(BASE_2, FORM_2):
    def __init__(self, parent=None):
        super(FORM2, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/Icon.png'))
        self.setModal(QtCore.Qt.ApplicationModal)

class FORM3(BASE_3, FORM_3):
    def __init__(self, parent=None):
        super(FORM3, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/Icon.png'))
        self.setModal(QtCore.Qt.ApplicationModal)

class MyApp(FORM_1, BASE_1):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)

        self.sDrag = None

        self.iMsg = 0        
        self.mapDict = dict()

        self.sWorld = ""
        self.world = None
        self.sOutputDirectory, _ = os.path.split(sys.argv[0])
        self.sDefaultDirectory, _ = os.path.split(sys.argv[0])
        self.sSeed = ""

        self.toolBox.setCurrentIndex(0)

        self.popup = FORM2()
        self.dialog = FORM3()
        self.dialog.closeEvent = self.closeEvent

        self.connect(self.btnDown, QtCore.SIGNAL("released()"), self.btnDown_Clicked)
        self.connect(self.btnGH, QtCore.SIGNAL("released()"), self.btnHeightmap_Clicked)
        self.connect(self.btnSM, QtCore.SIGNAL("released()"), self.btnSatellite_Clicked)
        self.connect(self.btnSP, QtCore.SIGNAL("released()"), self.btnScatter_Clicked)
        self.connect(self.btnUp, QtCore.SIGNAL("released()"), self.btnUp_Clicked)
        self.connect(self.btnUpdate, QtCore.SIGNAL("released()"), self.btnUpdate_Clicked)

        self.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.onActionNew)
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.onActionOpen)
        self.connect(self.action_Save, QtCore.SIGNAL("triggered()"), self.onActionSave)
        self.connect(self.actionSave_Selected_Map_As, QtCore.SIGNAL("triggered()"), self.onActionSaveSelectedAs)
        self.connect(self.actionSave_All_Maps_As, QtCore.SIGNAL("triggered()"), self.onActionSaveAllAs)
        self.connect(self.actionSet_Output_Directory, QtCore.SIGNAL("triggered()"), self.onActionSetOutputDirectory)
        self.connect(self.action_Print_Current_Map_View, QtCore.SIGNAL("triggered()"), self.onActionPrint)
        self.connect(self.actionSave_Current_Map_View, QtCore.SIGNAL("triggered()"), self.onActionSaveCurrentView)
        self.connect(self.action_Quit, QtCore.SIGNAL("triggered()"), self.onActionQuit)
        self.connect(self.actionZoom_In, QtCore.SIGNAL("triggered()"), self.onActionZoomIn)
        self.connect(self.actionZoom_Out, QtCore.SIGNAL("triggered()"), self.onActionZoomOut)
        self.connect(self.actionFit_to_Width, QtCore.SIGNAL("triggered()"), self.onActionFitWidth)
        self.connect(self.actionFit_to_Height, QtCore.SIGNAL("triggered()"), self.onActionFitHeight)
        self.connect(self.actionActual_Size, QtCore.SIGNAL("triggered()"), self.onActionFitActual)
        self.connect(self.actionFit_to_Window, QtCore.SIGNAL("triggered()"), self.onActionFitWindow)
        self.connect(self.action_Help, QtCore.SIGNAL("triggered()"), self.onActionHelp)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.onActionAbout)
        self.connect(self.actionGenerate_World, QtCore.SIGNAL("triggered()"), self.onActionGenerate)
        self.connect(self.actionGenerate_All_Maps, QtCore.SIGNAL("triggered()"), self.onActionMapsAll)
        self.connect(self.actionBiome, QtCore.SIGNAL("triggered()"), self.onActionMapsBiome)
        self.connect(self.actionElevation, QtCore.SIGNAL("triggered()"), self.onActionMapsElevation)
        self.connect(self.actionGrayscale_Heightmap, QtCore.SIGNAL("triggered()"), self.onActionMapsGrayscale)
        self.connect(self.actionIce_Cap, QtCore.SIGNAL("triggered()"), self.onActionMapsIceCaps)
        self.connect(self.actionOcean, QtCore.SIGNAL("triggered()"), self.onActionMapsOcean)
        self.connect(self.actionPrecipitation, QtCore.SIGNAL("triggered()"), self.onActionMapsPrecipitation)
        self.connect(self.actionRivers, QtCore.SIGNAL("triggered()"), self.onActionMapsRivers)
        self.connect(self.actionScatter_Plot, QtCore.SIGNAL("triggered()"), self.onActionMapsScatter)
        self.connect(self.actionSatellite_View, QtCore.SIGNAL("triggered()"), self.onActionMapsSatellite)
        self.connect(self.actionTemperature, QtCore.SIGNAL("triggered()"), self.onActionMapsTemperature)
        self.connect(self.actionWinds, QtCore.SIGNAL("triggered()"), self.onActionMapsWinds)
        self.connect(self.action3D_View, QtCore.SIGNAL("triggered()"), self.onAction3DView)
        
        self.connect(self.dialog.btnCentre, QtCore.SIGNAL("released()"), self.btnCentre_Clicked)
        self.connect(self.dialog.btnRight, QtCore.SIGNAL("released()"), self.btnRight_Clicked)

        self.tblAvailable.setDragEnabled(True)
        self.tblAvailable.setDragDropOverwriteMode(False)
        self.tblAvailable.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.tblAvailable.setDefaultDropAction(QtCore.Qt.ActionMask)
        self.tblAvailable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblAvailable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.tblMapList.setDragEnabled(True)
        self.tblMapList.setDragDropOverwriteMode(False)
        self.tblMapList.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.tblMapList.setDefaultDropAction(QtCore.Qt.ActionMask)
        self.tblMapList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblMapList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.tblMapList.viewport().installEventFilter(self)
        self.tblAvailable.viewport().installEventFilter(self)

        self.connect(self.tblMapList, QtCore.SIGNAL("itemSelectionChanged()"), self.tblMapListChanged)
        self.connect(self.spnOpacity, QtCore.SIGNAL("valueChanged"), self.spnOpacityChanged)

        self.connect(self.gvLarge.horizontalScrollBar(), QtCore.SIGNAL("valueChanged(int)"), self.gvLargeSBHorChanged)
        self.connect(self.gvLarge.verticalScrollBar(), QtCore.SIGNAL("valueChanged(int)"), self.gvLargeSBVertChanged)
        
        self.changeScene("No World loaded")

    def gvLargeSBVertChanged(self, int):        
        self.updateBox()
    
    def gvLargeSBHorChanged(self, int):
        self.updateBox()
        
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Drop):
            mimeData = event.mimeData()
 
            for mimeFormat in mimeData.formats():
                if mimeFormat != "application/x-qabstractitemmodeldatalist":
                    continue

                data = self.decodeMimeData(mimeData.data(mimeFormat))

                if self.sDrag != source and self.sDrag != None:
                    self.sDrag = None

                    if source == self.tblMapList.viewport():
                        curRowCount = self.tblMapList.rowCount()
                        self.tblMapList.insertRow(curRowCount)
                        iTemp = QtGui.QTableWidgetItem(data)
                        self.tblMapList.setItem(curRowCount, 0, iTemp)
                        self.tblMapList.setCurrentCell(curRowCount, 0)

                        sTemp = self.tblMapList.item(curRowCount, 0).text()
                        
                        if not sTemp in self.mapDict:
                            self.mapDict[sTemp] = 127

                        self.lblCurrentMap.setEnabled(True)
                        self.spnOpacity.setEnabled(True)

                        self.tblAvailable.removeRow(self.tblAvailable.currentRow())
                        self.tblAvailable.setCurrentCell(0,0)

                        self.btnUpdate.setEnabled(True)

                        if curRowCount > 0:
                            self.btnUp.setEnabled(True)
                            self.btnDown.setEnabled(True)
                        else:
                            self.btnUp.setEnabled(False)
                            self.btnDown.setEnabled(False)

                        self.spnOpacity.setValue(self.mapDict[sTemp])
                    elif source == self.tblAvailable.viewport():
                        curRowCount = self.tblAvailable.rowCount()
                        self.tblAvailable.insertRow(curRowCount)
                        iTemp = QtGui.QTableWidgetItem(data)
                        self.tblAvailable.setItem(curRowCount, 0, QtGui.QTableWidgetItem(iTemp))
                        self.tblAvailable.setCurrentCell(curRowCount, 0)

                        self.tblMapList.removeRow(self.tblMapList.currentRow())
                        self.tblMapList.setCurrentCell(0,0)

                        curRowCount = self.tblMapList.rowCount()

                        if curRowCount > 0:
                            self.btnUpdate.setEnabled(True)
                            
                            sTemp = self.tblMapList.item(0, 0).text()                            
                            self.spnOpacity.setValue(self.mapDict[sTemp])
                        else:
                            self.btnUpdate.setEnabled(False)
                            self.lblCurrentMap.setText("None")
                            self.lblCurrentMap.setEnabled(False)
                            self.spnOpacity.setValue(127)
                            self.spnOpacity.setEnabled(False)

                            self.actionZoom_In.setEnabled(False)
                            self.actionZoom_Out.setEnabled(False)
                            self.actionFit_to_Width.setEnabled(False)
                            self.actionFit_to_Height.setEnabled(False)
                            self.actionActual_Size.setEnabled(False)
                            self.actionFit_to_Window.setEnabled(False)
                            self.action_Save.setEnabled(False)
                            self.actionSave_Selected_Map_As.setEnabled(False)
                            self.actionSave_All_Maps_As.setEnabled(False)
                            self.action_Print_Current_Map_View.setEnabled(False)
                            self.actionSave_Current_Map_View.setEnabled(False)

                        if curRowCount > 1:
                            self.btnUp.setEnabled(True)
                            self.btnDown.setEnabled(True)
                        else:
                            self.btnUp.setEnabled(False)
                            self.btnDown.setEnabled(False)
        elif (event.type() == QtCore.QEvent.DragEnter):
            if self.sDrag == None:
                self.sDrag = source
            print("Drag Enter")
        elif (event.type() == QtCore.QEvent.DragLeave):
            self.sDrag = source
            print("Drag Leave")

        return QtGui.QMainWindow.eventFilter(self, source, event)

    def decodeMimeData(self, mimeData):
        result = {}
        value = QtCore.QVariant()
        stream = QtCore.QDataStream(mimeData)

        while not stream.atEnd():
            row = stream.readInt32()
            col = stream.readInt32()
            item = result.setdefault(col, {})

            for role in range(stream.readInt32()):
                key = QtCore.Qt.ItemDataRole(stream.readInt32())
                stream >> value
                item[key] = value.toPyObject()

            return result[0][QtCore.Qt.DisplayRole]

    def tblMapListChanged(self):
        iRow = self.tblMapList.currentRow()
        sTmp = self.tblMapList.item(iRow, 0).text()
        self.lblCurrentMap.setText(sTmp)

    def spnOpacityChanged(self):
        iRow = self.tblMapList.currentRow()
        sTmp = self.tblMapList.item(iRow, 0).text()
        self.mapDict[sTmp] = self.spnOpacity.value()

    def btnDown_Clicked(self):
        iRow = self.tblMapList.currentRow()

        if iRow == None:
            iRow = 0

        iRowCount = self.tblMapList.rowCount() - 1

        if iRow < iRowCount:
            item1 = self.tblMapList.item(iRow, 0)
            item2 = self.tblMapList.item(iRow + 1, 0)
            sText = item1.text()
            sText1 = item2.text()

            item1.setText(sText1)
            item2.setText(sText)

            self.tblMapList.setCurrentCell(iRow + 1, 0)

            m1 = self.mapDict[sText]
            m2 = self.mapDict[sText1]
            self.mapDict[sText] = m2
            self.mapDict[sText1] = m1

    def btnHeightmap_Clicked(self):
        pass

    def btnSatellite_Clicked(self):
        pass

    def btnScatter_Clicked(self):
        pass

    def btnUp_Clicked(self):
        iRow = self.tblMapList.currentRow()

        if iRow == None:
            iRow = self.tblMapList.rowCount() - 1

        if iRow > 0:
            item1 = self.tblMapList.item(iRow, 0)
            item2 = self.tblMapList.item(iRow - 1, 0)
            sText = item1.text()
            sText1 = item2.text()

            item1.setText(sText1)
            item2.setText(sText)

            self.tblMapList.setCurrentCell(iRow - 1, 0)
            
            m1 = self.mapDict[sText]
            m2 = self.mapDict[sText1]
            self.mapDict[sText] = m2
            self.mapDict[sText1] = m1
            
    def btnUpdate_Clicked(self):
        self.gvSceneSm = QtGui.QGraphicsScene()
        self.gvSceneLg = QtGui.QGraphicsScene()

        bFirst = True

        self.actionZoom_In.setEnabled(True)
        self.actionZoom_Out.setEnabled(True)
        self.actionFit_to_Width.setEnabled(True)
        self.actionFit_to_Height.setEnabled(True)
        self.actionActual_Size.setEnabled(True)
        self.actionFit_to_Window.setEnabled(True)
        self.action_Save.setEnabled(True)
        self.actionSave_Selected_Map_As.setEnabled(True)
        self.actionSave_All_Maps_As.setEnabled(True)
        self.action_Print_Current_Map_View.setEnabled(True)
        self.actionSave_Current_Map_View.setEnabled(True)

        for index in reversed(xrange(self.tblMapList.rowCount())):
            sTmp = self.sDefaultDirectory + "/" + "seed_" + self.sSeed + '_' + self.tblMapList.item(index, 0).text() + '.png'
            self.pixmap = QtGui.QPixmap(sTmp)
            piPixItemLg = QtGui.QGraphicsPixmapItem()
            piPixItemLg.setPixmap(self.pixmap)
            piPixItemLg.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)
            piPixItemSm = QtGui.QGraphicsPixmapItem()
            piPixItemSm.setPixmap(self.pixmap)
            piPixItemSm.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)

            if not bFirst:
                sTemp = self.tblMapList.item(index, 0).text()
                dOpacity = float(self.mapDict[sTemp]) / 255
                piPixItemLg.setOpacity(dOpacity)
                piPixItemSm.setOpacity(dOpacity)
            else:
                piPixItemLg.setOpacity(1)
                piPixItemSm.setOpacity(1)
                bFirst = False

            self.gvSceneLg.addItem(piPixItemLg)
            self.gvSceneSm.addItem(piPixItemSm)

        self.gvSmall.setScene(self.gvSceneSm)
        self.gvSmall.setRenderHint(QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        self.gvLarge.setScene(self.gvSceneLg)
        self.gvLarge.setRenderHint(QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvSmall.centerOn(0, 0)
        self.gvSmall.fitInView(bounds, QtCore.Qt.KeepAspectRatio)        
        
        self.onActionFitWindow()

        self.updateBox()

    def addRedBox(self, x1, y1, x2, y2):
        items = [i for i in self.gvSceneSm.items() if issubclass(i.__class__, QtGui.QGraphicsLineItem)]
        
        for x in items:
            self.gvSceneSm.removeItem(x)

        lin1 = QtGui.QGraphicsLineItem(x1, y1, x2, y1)
        lin2 = QtGui.QGraphicsLineItem(x2, y1, x2, y2)
        lin3 = QtGui.QGraphicsLineItem(x2, y2, x1, y2)
        lin4 = QtGui.QGraphicsLineItem(x1, y2, x1, y1)

        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtCore.Qt.red)

        lin1.setPen(pen)
        lin2.setPen(pen)
        lin3.setPen(pen)
        lin4.setPen(pen)

        self.gvSceneSm.addItem(lin1)
        self.gvSceneSm.addItem(lin2)
        self.gvSceneSm.addItem(lin3)
        self.gvSceneSm.addItem(lin4)

    def onActionNew(self):
        self.showDialog("Are you sure you want to reset all the Data?", "Yes", "No", True, 1, "Images\question.png")

    def onActionOpen(self):
        tDialog = QtGui.QFileDialog()
        tDialog.setDirectory(self.sDefaultDirectory)
        self.sWorld = tDialog.getOpenFileName(self, "Open World File", ".", "World Files (*.world)");

        if self.sWorld:
            self.popup.show()
            self.popup.textBrowser.setText('')
            self.popup.label.setText('Please wait while the World is being created...')

            self.updatePopup('World Loading....\n\nPlease Wait! This will take a while!')
            APP.processEvents()
#            self.world = self.load_world(self.sWorld)
            self.updatePopup('World Loaded!')
            self.updatePopup('')
#            self.print_world_info(self.world)
            self.updatePopup('')
            self.updatePopup('Please close this Window to return to the main UI.')

            self.tblMapList.clear()
            self.tblMapList.setRowCount(0)
            self.tblAvailable.clear()
            self.tblAvailable.setRowCount(0)

            sTmp = os.path.basename(str(self.sWorld)).split('.')
            self.sSeed = QtCore.QString(sTmp[0])
            self.sSeed = self.sSeed.right(5)

            iCount = 0

            for file_name in os.listdir(self.sDefaultDirectory):
                if str(self.sSeed) in file_name:
                    if '.png' in file_name:
                        if not 'ancient' in file_name:
                            print("Filename " + str(iCount) + " = " + file_name)
                            curRowCount = self.tblAvailable.rowCount()
                            self.tblAvailable.insertRow(curRowCount)
                            sTmp = file_name.split('_')
                            sTmp = sTmp[2].split('.')
                            iTemp = QtGui.QTableWidgetItem(sTmp[0])
                            self.tblAvailable.setItem(curRowCount , 0, iTemp)

                            iCount = iCount + 1

            if iCount > 0:
                self.tblAvailable.setEnabled(True)
                self.tblMapList.setEnabled(True)
                
                self.changeScene("No Image(s) currently selected")
            else:
                self.tblAvailable.setRowCount(0)
                self.tblAvailable.setColumnCount(0)
                self.tblAvailable.setEnabled(False)
                
                self.changeScene("No Images currently exist for the loaded World")
        else:
            self.showDialog("You have selected an invalid file!\n\nPlease try again.", "OK", "", False, 0, "Images\error.png")

    def changeScene(self, inTxt):
        self.gvSceneSm = QtGui.QGraphicsScene()
        self.gvSceneLg = QtGui.QGraphicsScene()
        
        font = QtGui.QFont("Open Sans")

        self.gvSceneSm.addText(inTxt, font)
        self.gvSceneLg.addText(inTxt, font)

        self.gvSmall.setScene(self.gvSceneSm)
        self.gvSmall.setRenderHint(QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        self.gvLarge.setScene(self.gvSceneLg)
        self.gvLarge.setRenderHint(QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)

        bounds = QtCore.QRectF(self.gvSceneSm.itemsBoundingRect())
        self.gvSmall.centerOn(0, 0)
        self.gvSmall.fitInView(bounds, QtCore.Qt.KeepAspectRatio)
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvLarge.centerOn(0, 0)
        self.gvLarge.fitInView(bounds, QtCore.Qt.KeepAspectRatio)

    def showDialog(self, sText, sCentre, sRight, bRight, iMessage, sPix):
        self.dialog.lblMsg.setText(sText)
        self.dialog.btnCentre.setText(sCentre)
        self.dialog.btnRight.setText(sRight)
        self.iMsg = iMessage

        if bRight:
            self.dialog.btnRight.setVisible(True)
            self.dialog.btnRight.setEnabled(True)
        else:
            self.dialog.btnRight.setVisible(False)
            self.dialog.btnRight.setEnabled(False)

        tPix = QtGui.QPixmap(sPix)
        self.dialog.lblIcon.setPixmap(tPix)

        self.dialog.show()

    def print_world_info(self, world):
        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('WorldEngine World Information')

        self.updatePopup(" name               : %s" % world.name)
        self.updatePopup(" width              : %i" % world.width)
        self.updatePopup(" height             : %i" % world.height)
        self.updatePopup(" seed               : %i" % world.seed)
        self.updatePopup(" no plates          : %i" % world.n_plates)
        self.updatePopup(" ocean level        : %f" % world.ocean_level)
        self.updatePopup(" step               : %s" % world.step.name)
        self.updatePopup(" has biome          : %s" % world.has_biome())
        self.updatePopup(" has humidity       : %s" % world.has_humidity())
        self.updatePopup(" has irrigation     : %s" % world.has_irrigation())
        self.updatePopup(" has permeability   : %s" % world.has_permeability())
        self.updatePopup(" has watermap       : %s" % world.has_watermap())
        self.updatePopup(" has precipitations : %s" % world.has_precipitations())
        self.updatePopup(" has temperature    : %s" % world.has_temperature())

    def onActionSave(self):
        pass

    def onActionSaveSelectedAs(self):
        pass

    def onActionSaveAllAs(self):
        pass

    def onActionPrint(self):
        pass

    def onActionSaveCurrentView(self):
        import operator
        
        items = self.gvSceneLg.items()
        totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))
        
        pixMap = QtGui.QPixmap(totalRect.width(), totalRect.height())
        
        painter = QtGui.QPainter(pixMap)
        self.gvSceneLg.render(painter, totalRect)
        del painter
        
#        self.imageManipulation(pixMap, totalRect.width(), totalRect.height())
#        byte_array = QtCore.QByteArray()
#        tBuffer = QtCore.QBuffer(byte_array)
#        tBuffer.open(QtCore.QIODevice.WriteOnly)
#        pixMap.save(tBuffer, 'PNG')
#        tBuffer.close()

#        with open("image.json", "w") as outfile:
#            json.dumps(byte_array.toBase64(), outfile)

#Test code to see if I can extract Colours from Pixmap (WORKS!!)
    def imageManipulation(self, pTmp, iWidth, iHeight):
        tImage = pTmp.toImage()
        
        with open('test.csv', 'w') as yourFile:
            for x in range(int(iWidth)):
                for y in range(int(iHeight)):
                    c = tImage.pixel(x, y)
                    colors = QtGui.QColor(c).getRgbF()
#                    print "(%s,%s) = %s" % (x, y, colors)
                    yourFile.write("%s,%s,%s,%s,%s,%s," % (x, y, colors[0], colors[1], colors[2], colors[3]))

        tImage = QtGui.QPixmap()
        
    def onActionQuit(self):
        self.showDialog("Are you sure you want to Quit?", "Yes", "No", True, 2, "Images\question.png")

    def onActionZoomIn(self):
        self.gvLarge.scale(1.25, 1.25)
        self.updateBox()

    def onActionZoomOut(self):
        self.gvLarge.scale(0.75, 0.75)
        self.updateBox()

    def onActionFitWidth(self):
        margin = 2

        viewRect = self.gvLarge.viewport().rect().adjusted(margin, margin, -margin, -margin)
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        x2 = bounds.width()

        scaleX = viewRect.width() / x2
        self.gvLarge.resetTransform()
        self.gvLarge.scale(scaleX, scaleX)

        self.updateBox()

    def onActionFitHeight(self):
        margin = 2

        viewRect = self.gvLarge.viewport().rect().adjusted(margin, margin, -margin, -margin)
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        y2 = bounds.height()

        scaleY = viewRect.height() / y2
        self.gvLarge.resetTransform()
        self.gvLarge.scale(scaleY, scaleY)

        self.updateBox()

    def onActionFitActual(self):
        self.gvLarge.resetTransform()
        self.updateBox()

    def onActionFitWindow(self):
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvLarge.centerOn(0, 0)
        self.gvLarge.fitInView(bounds, QtCore.Qt.KeepAspectRatio)

        self.updateBox()

    def updateBox(self):
        vRect = QtCore.QRect(0, 0, self.gvLarge.viewport().width(), self.gvLarge.viewport().height())
        visRect = self.gvLarge.mapToScene(vRect).boundingRect();

        x1 = visRect.x()
        x2 = x1 + visRect.width()
        y1 = visRect.y()
        y2 = y1 + visRect.height()

        self.addRedBox(x1, y1, x2, y2)
        
    def onActionHelp(self):
        self.print_help()

    def onActionAbout(self):
        self.print_version()

    def onActionGenerate(self):
        pass

    def onActionMapsAll(self):
        pass
    
    def onActionMapsBiome(self):
        pass
    
    def onActionMapsElevation(self):
        pass
    
    def onActionMapsGrayscale(self):
        pass
    
    def onActionMapsIceCaps(self):
        pass
    
    def onActionMapsOcean(self):
        pass
    
    def onActionMapsPrecipitation(self):
        pass
    
    def onActionMapsRivers(self):
        pass
    
    def onActionMapsScatter(self):
        pass
    
    def onActionMapsSatellite(self):
        pass
    
    def onActionMapsTemperature(self):
        pass
    
    def onActionMapsWinds(self):
        pass
    
    def onAction3DView(self):
        pass
    
    def __get_last_byte__(self, filename):
        with open(filename, 'rb') as input_file:
            data = tmp_data = input_file.read(1024 * 1024)
            while tmp_data:
                tmp_data = input_file.read(1024 * 1024)
                if tmp_data:
                    data = tmp_data
        return data[len(data) - 1]

    def __varint_to_value__(self, varint):
        if len(varint) == 1:
            return varint[0]
        else:
            return varint[0] + 128 * self.__varint_to_value__(varint[1:])

    def __get_tag__(self, filename):
        with open(filename, 'rb') as ifile:
            data = ifile.read(1)

            if not data:
                return None

            done = False
            tag_bytes = []

            while data and not done:
                data = ifile.read(1)

                if not data:
                    return None

                value = ord(data)
                tag_bytes.append(value % 128)

                if value < 128:
                    done = True

            return self.__varint_to_value__(tag_bytes)

    def __seems_protobuf_worldfile__(self, world_filename):
        worldengine_tag = self.__get_tag__(world_filename)
        return worldengine_tag == World.worldengine_tag()

    def load_world(self, world_filename):
        pb = self.__seems_protobuf_worldfile__(world_filename)
        if pb:
            try:
                return World.open_protobuf(world_filename)
            except Exception:
                raise Exception("Unable to load the worldfile as protobuf file")
        else:
            raise Exception("The given worldfile does not seem to be a protobuf file")

    def onActionSetOutputDirectory(self):
        self.sOutputDirectory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")

        if not self.sOutputDirectory:
            self.sOutputDirectory, _ = os.path.split(sys.argv[0])

    def print_help(self):
        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('WorldEngine Help')

        self.updatePopup(' ---------------------------------------------------------------------')
        self.updatePopup(' ')
        self.updatePopup(' The GUI for WorldEngine should be fairly easy to understand, but')
        self.updatePopup(' there are a few things to be wary of:')
        self.updatePopup(' ')
        self.updatePopup(' 1. The GUI will ONLY display Images (in the Generated Maps tab) that')
        self.updatePopup('    are saved in either BMP or PNG format.')
        self.updatePopup(' ')
        self.updatePopup(' 2. When you select PLATES for the STEP option, the rest of the')
        self.updatePopup('    options below the line will have no effect.')
        self.updatePopup(' ')
        self.updatePopup(' 3. The values in TEMPERATURE RANGE and PRECIPITATION RANGE MUST be')
        self.updatePopup('    in ASCENDING order.')
        self.updatePopup(' ')
        self.updatePopup(' 4. The value in RECURSION LIMIT should only be changed if you are')
        self.updatePopup('    creating a large map.')
        self.updatePopup(' ')
        self.updatePopup(' 5. Selecting NO for the USE PROTOCOL BUFFER OPTION will use the HDF5')
        self.updatePopup('    encoding which will result in a smaller World File being generated')
        self.updatePopup(' ')
        self.updatePopup(' Thats about it, but please read the Manual for a full description')
        self.updatePopup(' of all the options available.')
        self.updatePopup(' ')
        self.updatePopup(' ')
        self.updatePopup(' Please close this Window to return to the main UI')
        self.updatePopup(' ')
        self.updatePopup(' ---------------------------------------------------------------------')

    def print_version(self):
        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('WorldEngine Version Information')

        self.updatePopup(' -------------------------------------------------------------------')
        self.updatePopup(' ')
        self.updatePopup(' ')
        self.updatePopup(' Federico Tomassetti and Bret Curtis, 2011-2016')
        self.updatePopup(' WorldEngine - a world generator (v. %s)' % VERSION)
        self.updatePopup(' ')
        self.updatePopup(' ')
        self.updatePopup(' Please close this Window to return to the main UI')
        self.updatePopup(' ')
        self.updatePopup(' -------------------------------------------------------------------')

# 1 = New
# 2 = Quit
# 0 = No Action
    def btnCentre_Clicked(self):
        self.dialog.close()

        if self.iMsg == 1:
            self.setDefaults()
        elif self.iMsg == 2:
            sys.exit(APP.exec_())

    def btnRight_Clicked(self):
        self.dialog.close()
        self.iMsg = 0

    @pyqtSlot('QString')
    def updatePopup(self, sText):
        self.popup.textBrowser.append(sText)

if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    FORM = MyApp()
    APP.setWindowIcon(QtGui.QIcon(':/Images/icon.png'))
    FORM.show()
    APP.exec_()
