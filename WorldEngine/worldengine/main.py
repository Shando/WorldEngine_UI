import sys
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

from PyQt4  import QtGui
from PyQt4  import QtCore
from PyQt4  import uic

FORM_1, BASE_1 = uic.loadUiType("worldengine.ui")
FORM_2, BASE_2 = uic.loadUiType("popup.ui")
FORM_3, BASE_3 = uic.loadUiType("dialog.ui")

class MyApp(FORM_1, BASE_1):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        
        global iMsg
        iMsg = 0
        
        self.popup = FORM2()
        self.dialog = FORM3()

        self.connect(self.btnWorld, QtCore.SIGNAL("released()"), self.btnWorld_Clicked)
        self.connect(self.btnRandomise, QtCore.SIGNAL("released()"), self.btnRandomise_Clicked)
        self.connect(self.btnAncWorld, QtCore.SIGNAL("released()"), self.btnAncientOpen_Clicked)
        self.connect(self.btnAncMap, QtCore.SIGNAL("released()"), self.btnAncient_Clicked)
        self.connect(self.btnBM, QtCore.SIGNAL("released()"), self.btnBiome_Clicked)
        self.connect(self.btnEM, QtCore.SIGNAL("released()"), self.btnElevation_Clicked)
        self.connect(self.btnGH, QtCore.SIGNAL("released()"), self.btnGrayscale_Clicked)
        self.connect(self.btnICM, QtCore.SIGNAL("released()"), self.btnIceCaps_Clicked)
        self.connect(self.btnOM, QtCore.SIGNAL("released()"), self.btnOcean_Clicked)
        self.connect(self.btnPM, QtCore.SIGNAL("released()"), self.btnPrecipitation_Clicked)
        self.connect(self.btnRM, QtCore.SIGNAL("released()"), self.btnRivers_Clicked)
        self.connect(self.btnSM, QtCore.SIGNAL("released()"), self.btnSatellite_Clicked)
        self.connect(self.btnSP, QtCore.SIGNAL("released()"), self.btnScatter_Clicked)
        self.connect(self.btnTM, QtCore.SIGNAL("released()"), self.btnTemperature_Clicked)
        self.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.onActionNew)
        self.connect(self.actionClose, QtCore.SIGNAL("triggered()"), self.onActionClose)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.onActionAbout)
        self.connect(self.actionHelp_File, QtCore.SIGNAL("triggered()"), self.onActionHelp)
        self.connect(self.actionSet_Output_Directory, QtCore.SIGNAL("triggered()"), self.onActionSetOutputDirectory)
        self.connect(self.actionVersion_Information, QtCore.SIGNAL("triggered()"), self.onActionVersionInformation)
        self.connect(self.dialog.btnCentre, QtCore.SIGNAL("released()"), self.btnCentre_Clicked)
        self.connect(self.dialog.btnRight, QtCore.SIGNAL("released()"), self.btnRight_Clicked)
        
        self.setDefaults()

    def btnWorld_Clicked(self):
        self.getValues()
        self.cli_main(sStep)
        self.updatePopup('World Generated')
        self.update_Buttons(False)

    def update_Buttons(self, bAncient):
        if (sFormat == "png" or sFormat == "bmp"):
            if bAncient:
                self.btnBM.setEnabled(False)
                self.btnBM.hide()
                self.btnEM.setEnabled(False)
                self.btnEM.hide()
                self.btnOM.setEnabled(False)
                self.btnOM.hide()
                self.btnPM.setEnabled(False)
                self.btnPM.hide()
                self.btnTM.setEnabled(False)
                self.btnTM.hide()
                self.btnICM.setEnabled(False)
                self.btnICM.hide()
                self.btnGH.setEnabled(False)
                self.btnGH.hide()
                self.btnSP.setEnabled(False)
                self.btnSP.hide()
                self.btnSM.setEnabled(False)
                self.btnSM.hide()
                self.btnRM.setEnabled(False)
                self.btnRM.hide()
                self.label_5.hide()
                self.label_15.hide()
                self.label_16.hide()
                self.label_17.hide()
                self.label_44.hide()
                self.label_45.hide()
                self.label_46.hide()
                self.label_47.hide()
                self.label_48.hide()
                self.label_49.hide()
    
                tPix = QtGui.QPixmap(sOutputDirectory + "/" + sAncFile)
                self.lblImage.setPixmap(tPix)                
            else:
                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_biome." + sFormat)
                self.btnBM.setEnabled(True)
                self.btnBM.show()
                self.btnBM.setIcon(tIcon)
                self.label_5.show()
                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_elevation." + sFormat)
                self.btnEM.setEnabled(True)
                self.btnEM.show()
                self.btnEM.setIcon(tIcon)
                self.label_15.show()
                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_ocean." + sFormat)
                self.btnOM.setEnabled(True)
                self.btnOM.show()
                self.btnOM.setIcon(tIcon)
                self.label_17.show()
                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_precipitation." + sFormat)
                self.btnPM.setEnabled(True)
                self.btnPM.show()
                self.btnPM.setIcon(tIcon)
                self.label_45.show()
                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_temperature." + sFormat)
                self.btnTM.setEnabled(True)
                self.btnTM.show()
                self.btnTM.setIcon(tIcon)
                self.label_48.show()
    
                tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_biome." + sFormat)
                self.lblImage.setPixmap(tPix)
                
    #TODO: CHECK IF ICE CAP MAPS WORK
    #            if bICM:
    #                tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_ice." + sFormat)
    #                self.btnICM.setEnabled(True)
    #                self.btnICM.show()
    #                self.btnICM.setIcon(tIcon)
    #                self.label_46.show()
    #            else:
    #                self.btnICM.setEnabled(False)
    #                self.btnICM.hide()
    #                self.label_46.hide()
    
                if bGH:
                    tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_grayscale." + sFormat)
                    self.btnGH.setEnabled(True)
                    self.btnGH.show()
                    self.btnGH.setIcon(tIcon)
                    self.label_16.show()
                else:
                    self.btnGH.setEnabled(False)
                    self.btnGH.hide()
                    self.label_16.hide()
    
                if bSP:
                    tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_scatter." + sFormat)
                    self.btnSP.setEnabled(True)
                    self.btnSP.show()
                    self.btnSP.setIcon(tIcon)
                    self.label_49.show()
                else:
                    self.btnSP.setEnabled(False)
                    self.btnSP.hide()
                    self.label_49.hide()
    
                if bSM:
                    tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_satellite." + sFormat)
                    self.btnSM.setEnabled(True)
                    self.btnSM.show()
                    self.btnSM.setIcon(tIcon)
                    self.label_47.show()
                else:
                    self.btnSM.setEnabled(False)
                    self.btnSM.hide()
                    self.label_47.hide()
                    
                if bRM:
                    tIcon = QtGui.QIcon(sOutputDirectory + "/" + sWorld + "_rivers." + sFormat)
                    self.btnRM.setEnabled(True)
                    self.btnRM.show()
                    self.btnRM.setIcon(tIcon)
                    self.label_44.show()
                else:
                    self.btnRM.setEnabled(False)
                    self.btnRM.hide()
                    self.label_44.hide()
        else:
            QtGui.QMessageBox.information(self, "WorldEngine", "Unfortunately, you will not be able to view the created Image(s) due to the selected format: %s " % sFormat)

    def btnRandomise_Clicked(self):
        from random import randint
        
        global iSeed
        global sWorld
        
        iSeed = randint(1, 65535)
        self.spnSeed.setValue(iSeed)
        sWorld = "seed_" + str(iSeed)
        self.txtWorld.setText(sWorld)


    def btnAncientOpen_Clicked(self):
        global sAncWorld
        global sAncFile
        global sAncFilePath
        
        sAncWorld = QtGui.QFileDialog.getOpenFileName(self, "Open World File", ".", "World Files (*.world)");
        
        from PyQt4.QtCore import QFileInfo
        
        sFile = QFileInfo(sAncWorld).completeBaseName()
        sAncFilePath = QFileInfo(sAncWorld).absolutePath()
        
        sAncFile = "ancient_world_" + sFile + "." + sAncFormat
        
        sAncWorld = sFile
        
        self.txtAncWorld.setText(sAncWorld)
        self.txtAncFile.setText(sAncFile)

    def btnAncient_Clicked(self):
        self.getValues()
        self.cli_main('ancient_map')
        self.updatePopup("Ancient Map Generated")
        self.update_Buttons(True)
                
    def btnBiome_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_biome." + sFormat)
        self.lblImage.setPixmap(tPix)
    
    def btnElevation_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_elevation." + sFormat)
        self.lblImage.setPixmap(tPix)
    
    def btnGrayscale_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_grayscale." + sFormat)
        self.lblImage.setPixmap(tPix)
        
    def btnOcean_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_ocean." + sFormat)
        self.lblImage.setPixmap(tPix)
    
    def btnPrecipitation_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_precipitation." + sFormat)
        self.lblImage.setPixmap(tPix)
        
    def btnRivers_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_rivers." + sFormat)
        self.lblImage.setPixmap(tPix)

#TODO: CHECK IF ICE CAP MAPS WORK
    def btnIceCaps_Clicked(self):
#        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_ice." + sFormat)
#        self.lblImage.setPixmap(tPix)
        tPix = ""
        
    def btnSatellite_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_satellite." + sFormat)
        self.lblImage.setPixmap(tPix)

    def btnScatter_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_scatter." + sFormat)
        self.lblImage.setPixmap(tPix)

    def btnTemperature_Clicked(self):
        tPix = QtGui.QPixmap(sOutputDirectory + "/" + sWorld + "_temperature." + sFormat)
        self.lblImage.setPixmap(tPix)

    def setDefaults(self):        
        global sWorld
        global sFormat
        global sStep
        global sDataType
        global sAncWorld
        global sAncFile
        global sAncFilePath
        global sAncFormat
        global sAncDataType
        global sOutputDirectory
    
        global iSeed
        global iWidth
        global iHeight
        global iPlates
        global iRecursion
        global iMsg
    
        global dSea
        global dTemp1
        global dTemp2
        global dTemp3
        global dTemp4
        global dTemp5
        global dTemp6
        global dPrecip1
        global dPrecip2
        global dPrecip3
        global dPrecip4
        global dPrecip5
        global dPrecip6
        global dPrecip7
        global dGammaVal
        global dGammaOff
        global dAncResize
    
        global bBW
        global bVM
        global bGH
        global bSM
        global bPB
        global bRM
        global bSP
        global bICM
        global bFB
        global bAncSeaColour
        global bAncBiomes
        global bAncMountains
        global bAncRivers
        global bAncBorders

        iMsg = 0
        sOutputDirectory = "."
        sWorld = "seed_11111"
        iSeed = 11111
        iWidth = 1024
        iHeight = 1024
        iPlates = 10
        iRecursion = 2000
        sFormat = "png"
        sStep = "full"
        sDataType = "uint16"
        bBW = False
        bVM = False
        bGH = False
        bSM = False
        
        if (HDF5_AVAILABLE):
            bPB = True
            self.rdoPBYes.setEnabled(True)
            self.rdoPBNo.setEnabled(True)
            self.rdoPBYes.setChecked(True)
        else:
            bPB = False
            self.rdoPBNo.setChecked(True)
            self.rdoPBYes.setEnabled(False)
            self.rdoPBNo.setEnabled(False)
                        
        bRM = False
        bSP = False
        bICM = False
        bFB = True
        dSea = 1.0
        dTemp1 = 0.126
        dTemp2 = 0.235
        dTemp3 = 0.406
        dTemp4 = 0.561
        dTemp5 = 0.634
        dTemp6 = 0.876
        dPrecip1 = 0.059
        dPrecip2 = 0.222
        dPrecip3 = 0.491
        dPrecip4 = 0.764
        dPrecip5 = 0.927
        dPrecip6 = 0.986
        dPrecip7 = 0.998
        dGammaVal = 1.25
        dGammaOff = 0.2
        sAncWorld = "seed_11111"
        sAncFile = "seed_11111_ancient"
        sAncFilePath = "."
        dAncResize = 1.0
        bAncSeaColour = False
#True = blue, False = brown
        bAncBiomes = True
        bAncMountains = True
        bAncRivers = True
        bAncBorders = True
        sAncFormat = "png"
        sAncDataType = "uint16"
    
        self.txtWorld.setText(sWorld)
        self.spnSeed.setValue(iSeed)
        self.spnHeight.setValue(iHeight)
        self.spnWidth.setValue(iWidth)
        self.spnPlates.setValue(iPlates)
        self.spnRecursion.setValue(iRecursion)

        index = self.cboStep.findText(sStep, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.cboStep.setCurrentIndex(index)
        else:
            self.cboStep.setCurrentIndex(0)

        index = self.cboFormat.findText(sFormat, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.cboFormat.setCurrentIndex(index)
        else:
            self.cboFormat.setCurrentIndex(0)

        index = self.cboData.findText(sDataType, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.cboData.setCurrentIndex(index)
        else:
            self.cboData.setCurrentIndex(0)

        self.rdoBWNo.setChecked(True)
        self.rdoVMNo.setChecked(True)
        self.rdoGHNo.setChecked(True)
        self.rdoSMNo.setChecked(True)
        self.rdoSPNo.setChecked(True)
        self.rdoICMNo.setChecked(True)
        self.rdoFadeYes.setChecked(True)
        self.spnSea.setValue(dSea)
        self.spnTemp1.setValue(dTemp1)
        self.spnTemp2.setValue(dTemp2)
        self.spnTemp3.setValue(dTemp3)
        self.spnTemp4.setValue(dTemp4)
        self.spnTemp5.setValue(dTemp5)
        self.spnTemp6.setValue(dTemp6)
        self.spnPrecip1.setValue(dPrecip1)
        self.spnPrecip2.setValue(dPrecip2)
        self.spnPrecip3.setValue(dPrecip3)
        self.spnPrecip4.setValue(dPrecip4)
        self.spnPrecip5.setValue(dPrecip5)
        self.spnPrecip6.setValue(dPrecip6)
        self.spnPrecip7.setValue(dPrecip7)
        self.spnGamma.setValue(dGammaVal)
        self.spnOffset.setValue(dGammaOff)
        self.txtAncWorld.setText(sAncWorld)
        self.txtAncFile.setText(sAncFile)
        self.spnResize.setValue(dAncResize)
        self.rdoSeaBrown.setChecked(True)
        self.rdoBiomesYes.setChecked(True)
        self.rdoRiverYes.setChecked(True)
        self.rdoMountYes.setChecked(True)
        self.rdoLandYes.setChecked(True)

        index = self.cboAncFormat.findText(sAncFormat, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.cboAncFormat.setCurrentIndex(index)
        else:
            self.cboAncFormat.setCurrentIndex(0)

        index = self.cboAncData.findText(sAncDataType, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.cboAncData.setCurrentIndex(index)
        else:
            self.cboAncData.setCurrentIndex(0)

        self.btnBM.setIcon(QtGui.QIcon())
        self.btnEM.setIcon(QtGui.QIcon())
        self.btnGH.setIcon(QtGui.QIcon())
        self.btnOM.setIcon(QtGui.QIcon())
        self.btnPM.setIcon(QtGui.QIcon())
        self.btnICM.setIcon(QtGui.QIcon())
        self.btnSP.setIcon(QtGui.QIcon())
        self.btnSM.setIcon(QtGui.QIcon())
        self.btnTM.setIcon(QtGui.QIcon())
        self.btnRM.setIcon(QtGui.QIcon())
        self.lblImage.setPixmap(QtGui.QPixmap())
        self.tabWidget.setCurrentIndex(0)
        
    def getValues(self):
        global sDataType
        global sAncWorld
        global sAncFile
        global sAncFormat
        global sAncDataType
        global sOutputDirectory
    
        global iSeed
        global iWidth
        global iHeight
        global iPlates
        global iRecursion

        global dSea
        global dTemp1
        global dTemp2
        global dTemp3
        global dTemp4
        global dTemp5
        global dTemp6
        global dPrecip1
        global dPrecip2
        global dPrecip3
        global dPrecip4
        global dPrecip5
        global dPrecip6
        global dPrecip7
        global dGammaVal
        global dGammaOff
        global dAncResize
    
        global bBW
        global bVM
        global bGH
        global bSM
        global bPB
        global bRM
        global bSP
        global bICM
        global bFB
        global bAncSeaColour
        global bAncBiomes
        global bAncMountains
        global bAncRivers
        global bAncBorders

        sWorld = self.txtWorld.text()
        iSeed = self.spnSeed.value()
        iHeight = self.spnHeight.value()
        iWidth = self.spnWidth.value()
        iPlates = self.spnPlates.value()
        iRecursion = self.spnRecursion.value()
        sStep = self.cboStep.currentText()
        sFormat = self.cboFormat.currentText()
        sDataType = self.cboData.currentText()
        bBW = self.rdoBWYes.isChecked()
        bVM = self.rdoVMYes.isChecked()
        bGH = self.rdoGHYes.isChecked()
        bSM = self.rdoSMYes.isChecked()
        bPB = self.rdoPBYes.isChecked()
        bSP = self.rdoSPYes.isChecked()
        bICM = self.rdoICMYes.isChecked()
        bFB = self.rdoFadeYes.isChecked()
        dSea = self.spnSea.value()
        dTemp1 = self.spnTemp1.value()
        dTemp2 = self.spnTemp2.value()
        dTemp3 = self.spnTemp3.value()
        dTemp4 = self.spnTemp4.value()
        dTemp5 = self.spnTemp5.value()
        dTemp6 = self.spnTemp6.value()
        dPrecip1 = self.spnPrecip1.value()
        dPrecip2 = self.spnPrecip2.value()
        dPrecip3 = self.spnPrecip3.value()
        dPrecip4 = self.spnPrecip4.value()
        dPrecip5 = self.spnPrecip5.value()
        dPrecip6 = self.spnPrecip6.value()
        dPrecip7 = self.spnPrecip7.value()
        dGammaVal = self.spnGamma.value()
        dGammaOff = self.spnOffset.value()
        sAncWorld = self.txtAncWorld.text()
        sAncFile = self.txtAncFile.text()
        dAncResize = self.spnResize.value()
        bAncSeaColour = self.rdoSeaBlue.isChecked()
        bAncBiomes = self.rdoBiomesYes.isChecked()
        bAncRivers = self.rdoRiverYes.isChecked()
        bAncMountains = self.rdoMountYes.isChecked()
        bAncBorders = self.rdoLandYes.isChecked()
        sAncFormat = self.cboAncFormat.currentText()
        sAncDataType = self.cboAncData.currentText()
    
    def onActionNew(self):
        global iMsg
        
        self.dialog.lblMsg.setText("Are you sure you want to reset all the Data?")
        self.dialog.btnCentre.setText("Yes")
        self.dialog.btnRight.setText("No")
        self.dialog.btnRight.setVisible(True)
        
        tPix = QtGui.QPixmap('Images\question.png')
        self.dialog.lblIcon.setPixmap(tPix)
        
        self.dialog.show()
        iMsg = 1
        
    def onActionClose(self):
        global iMsg
        
        self.dialog.lblMsg.setText("Are you sure you want to Quit?")
        self.dialog.btnCentre.setText("Yes")
        self.dialog.btnRight.setText("No")
        self.dialog.btnRight.setVisible(True)
        
        tPix = QtGui.QPixmap('Images\question.png')
        self.dialog.lblIcon.setPixmap(tPix)
        
        self.dialog.show()
        iMsg = 2
        
    def onActionHelp(self):
        self.cli_main('help')
    
    def onActionAbout(self):
        self.cli_main('about')
    
#TODO: File -> Set Output Directory
    def onActionSetOutputDirectory(self):
        global sOutputDirectory
        
        sOutputDirectory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if not sOutputDirectory:
            sOutputDirectory = "."
        
    def onActionVersionInformation(self):
        self.cli_main('version')

    def generateWorld(self, step):
        w, myMsg = world_gen(sWorld, iWidth, iHeight, iSeed, [dTemp1, dTemp2, dTemp3, dTemp4, dTemp5, dTemp6],
        [dPrecip1, dPrecip2, dPrecip3, dPrecip4, dPrecip5, dPrecip6, dPrecip7], iPlates, dSea,
        step, dGammaVal, dGammaOff, bFB, bVM)
        
        if myMsg:
            self.updatePopup(myMsg)

        filename = "%s/%s.world" % (sOutputDirectory, sWorld)
        
        if bPB:
            with open(filename, "wb") as f:
                f.write(w.protobuf_serialize())
        else:
            save_world_to_hdf5(w, filename)

        self.updatePopup("* world data saved in '%s'" % filename)
    
        # Generate images
        filename = '%s/%s_ocean.png' % (sOutputDirectory, sWorld)
        draw_ocean_on_file(w.layers['ocean'].data, filename)
        
        self.updatePopup("* ocean map generated in '%s'" % filename)
    
        if step.include_precipitations:
            filename = '%s/%s_precipitation.png' % (sOutputDirectory, sWorld)
            draw_precipitation_on_file(w, filename, bBW)
            
            self.updatePopup("* precipitation map generated in '%s'" % filename)
            
            filename = '%s/%s_temperature.png' % (sOutputDirectory, sWorld)
            draw_temperature_levels_on_file(w, filename, bBW)
            
            self.updatePopup("* temperature image generated in '%s'" % filename)
    
        if step.include_biome:
            filename = '%s/%s_biome.png' % (sOutputDirectory, sWorld)
            draw_biome_on_file(w, filename)
        
        self.updatePopup("* biome image generated in '%s'" % filename)
    
        filename = '%s/%s_elevation.png' % (sOutputDirectory, sWorld)
        draw_simple_elevation_on_file(w, filename, sea_level=dSea)
        
        self.updatePopup("* elevation image generated in '%s'" % filename)
        
        return w
    
    def generate_grayscale_heightmap(self, world, filename):
        draw_grayscale_heightmap_on_file(world, filename)
        self.updatePopup("+ grayscale heightmap generated in '%s'" % filename)
    
    def generate_rivers_map(self, world, filename):
        draw_riversmap_on_file(world, filename)
        self.updatePopup("+ rivers map generated in '%s'" % filename)
    
    def draw_scatter_plot(self, world, filename):
        draw_scatter_plot_on_file(world, filename)
        self.updatePopup("+ scatter plot generated in '%s'" % filename)
    
    def draw_satellite_map(self, world, filename):
        draw_satellite_on_file(world, filename)
        self.updatePopup("+ satellite map generated in '%s'" % filename)
    
    def draw_icecaps_map(self, world, filename):
        draw_icecaps_on_file(world, filename)
        self.updatePopup("+ icecap map generated in '%s'" % filename)
    
    def generate_plates(self):
        elevation, plates, myMsg = generate_plates_simulation(iSeed, iWidth, iHeight, iPlates)
    
        if myMsg:
            self.updatePopup(myMsg)
            
        world = World(sWorld, Size(iWidth, iHeight), iSeed, GenerationParameters(iPlates, -1.0, "plates"))
        world.set_elevation(numpy.array(elevation).reshape(iHeight, iWidth), None)
        world.set_plates(numpy.array(plates, dtype=numpy.uint16).reshape(iHeight, iWidth))
    
        # Generate images
        filename = '%s/plates_%s.png' % (sOutputDirectory, sWorld)
        draw_simple_elevation_on_file(world, filename, None)
        
        self.updatePopup("+ plates image generated in '%s'" % filename)
        
        myMsg = geo.center_land(world)
        
        if myMsg:
            self.updatePopup(myMsg)
            
        filename = '%s/centered_plates_%s.png' % (sOutputDirectory, sWorld)
        draw_simple_elevation_on_file(world, filename, None)
        
        self.updatePopup("+ centered plates image generated in '%s'" % filename)
        
    def check_step(self, step_name):
        step = Step.get_by_name(step_name)
        
        if step is None:
            return Step.get_by_name('full')
        else:
            return step
        
    def operation_ancient_map(self, world):
        if bAncSeaColour == True:
            sea_colour = (142, 162, 179, 255)
        else:
            sea_colour = (212, 198, 169, 255)
            
        myMsg = draw_ancientmap_on_file(world, sAncFile, dAncResize, sea_colour,
        bAncBiomes, bAncRivers, bAncMountains, bAncBorders)
        
        if myMsg:
            self.updatePopup(myMsg)
            
        self.updatePopup("+ ancient map generated in '%s'" % sAncFile)
    
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
    
    def print_world_info(self, world):
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
    
    def cli_main(self, operation):
        sys.setrecursionlimit(iRecursion)
    
        numpy.random.seed(iSeed)
    
        step = self.check_step(sStep)
        
        self.popup.show()
        self.popup.textBrowser.setText("")

        self.updatePopup('Worldengine - a world generator (v. %s)' % VERSION)
        self.updatePopup('-----------------------')
        APP.processEvents()

        if (operation == 'full' or operation == 'precipitations' or operation == 'plates'):
            self.updatePopup(' operation            : %s generation' % sStep)
            self.updatePopup(' seed                 : %i' % iSeed)
            self.updatePopup(' name                 : %s' % sWorld)
            self.updatePopup(' width                : %i' % iWidth)
            self.updatePopup(' height               : %i' % iHeight)
            self.updatePopup(' number of plates     : %i' % iPlates)
            self.updatePopup(' world format         : %s' % sFormat)
            self.updatePopup(' black and white maps : %s' % bBW)
            self.updatePopup(' step                 : %s' % sStep)
            self.updatePopup(' greyscale heightmap  : %s' % bGH)
            self.updatePopup(' icecaps heightmap    : %s' % bICM)
            self.updatePopup(' rivers map           : %s' % bRM)
            self.updatePopup(' scatter plot         : %s' % bSP)
            self.updatePopup(' satellite map        : %s' % bSM)
            self.updatePopup(' fade borders         : %s' % bFB)
            self.updatePopup(' temperature ranges   : %s' % [dTemp1, dTemp2, dTemp3, dTemp4, dTemp5, dTemp6])
            self.updatePopup(' humidity ranges      : %s' % [dPrecip1, dPrecip2, dPrecip3, dPrecip4, dPrecip5, dPrecip6, dPrecip7])
            self.updatePopup(' gamma value          : %s' % dGammaVal)
            self.updatePopup(' gamma offset         : %s' % dGammaOff)
            APP.processEvents()

        if operation == 'ancient_map':
            self.updatePopup(' operation              : %s generation' % operation)
            self.updatePopup(' resize factor          : %i' % dAncResize)
            self.updatePopup(' world file             : %s' % sAncWorld)
            
            if (bAncSeaColour):
                self.updatePopup(' sea color              : blue')
            else:
                self.updatePopup(' sea color              : brown')

            self.updatePopup(' draw biome             : %s' % bAncBiomes)
            self.updatePopup(' draw rivers            : %s' % bAncRivers)
            self.updatePopup(' draw mountains         : %s' % bAncMountains)
            self.updatePopup(' draw land outer border : %s' % bAncBorders)
            APP.processEvents()

        if operation == 'full':
            self.updatePopup('')  # empty line
            self.updatePopup('starting (this will take a few minutes and the UI will become unresponsive) ...')
    
            APP.processEvents()
            world = self.generateWorld(step)
            
            self.updatePopup("Producing Output:")
            APP.processEvents()
            
            if bGH:
                self.generate_grayscale_heightmap(world, '%s/%s_grayscale.png' % (sOutputDirectory, sWorld))
            
            if bRM:
                self.generate_rivers_map(world, '%s/%s_rivers.png' % (sOutputDirectory, sWorld))
            
            if bSP:
                self.draw_scatter_plot(world, '%s/%s_scatter.png' % (sOutputDirectory, sWorld))    
            
            if bSM:
                self.draw_satellite_map(world, '%s/%s_satellite.png' % (sOutputDirectory, sWorld))
            
            if bICM:
                self.draw_icecaps_map(world, '%s/%s_icecaps.png' % (sOutputDirectory, sWorld))
    
        elif operation == 'plates':
            self.updatePopup('')  # empty line
            self.updatePopup('starting (this will take a few minutes and the UI will become unresponsive) ...')
            APP.processEvents()

            self.generate_plates()
    
        elif operation == 'ancient_map':
            self.updatePopup('')  # empty line
            self.updatePopup('starting (this will take a few minutes and the UI will become unresponsive) ...')
            APP.processEvents()
            
            # First, some error checking
            if bAncSeaColour:
                sea_color = (142, 162, 179, 255)
            else:
                sea_color = (212, 198, 169, 255)

            sTmp = sAncFilePath + "/" + sAncWorld + ".world"
            
            world = self.load_world(sTmp)
    
            self.updatePopup(" * world loaded")
    
            generated_file = "ancient_map_%s.png" % world.name
            APP.processEvents()
            
            self.operation_ancient_map(world)

            self.updatePopup("ancient map generated")
        elif operation == 'info':
            world = self.load_world(sOutputDirectory + '/' + sWorld + '.world')
            self.print_world_info(world)
        elif operation == 'export':
            world = self.load_world(sOutputDirectory + '/' + sWorld + '.world')
            self.print_world_info(world)
            export(world, sFormat, sDataType, path = '%s/%s_elevation' % (sOutputDirectory, sWorld))
        elif operation == 'version':
            self.print_version()
        else:
            self.print_help()

        self.updatePopup(' ')
        self.updatePopup('...all done!')
        self.updatePopup(' ')
        self.updatePopup('Please close this Window to return to the main UI.')
    
    def print_help(self):
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
        self.updatePopup(' -------------------------------------------------------------------')
        self.updatePopup(' ')
        self.updatePopup(' ')
        self.updatePopup(' Federico Tomassetti and Bret Curtis, 2011-2016')
        self.updatePopup(' Worldengine - a world generator (v. %s)' % VERSION)
        self.updatePopup(' ')
        self.updatePopup(' ')
        self.updatePopup(' Please close this Window to return to the main UI')
        self.updatePopup(' ')
        self.updatePopup(' -------------------------------------------------------------------')
    
    def btnCentre_Clicked(self):
        global iMsg
        
        if iMsg == 1:
            self.setDefaults()
        elif iMsg == 2:
            sys.exit(APP.exec_())
            
    def btnRight_Clicked(self):
        global iMsg
        
        iMsg = 0
        
    @pyqtSlot('QString')
    def updatePopup(self, sText):
        self.popup.textBrowser.append(sText)
        
class FORM2(BASE_2, FORM_2):
    def __init__(self, parent=None):
        super(FORM2, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/Icon.png'))

class FORM3(BASE_3, FORM_3):
    def __init__(self, parent=None):
        super(FORM3, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/Icon.png'))

if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    FORM = MyApp()
    APP.setWindowIcon(QtGui.QIcon(':/Images/icon.png'))
    FORM.show()
    APP.exec_()
