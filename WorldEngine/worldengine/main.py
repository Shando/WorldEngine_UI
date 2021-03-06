import time
from shutil import copy

import configparser2
import numpy
import os.path

import common
from draw import draw_ancientmap_on_file, draw_biome_on_file, draw_ocean_on_file, \
    draw_precipitation_on_file, draw_grayscale_heightmap_on_file, draw_simple_elevation_on_file, \
    draw_temperature_levels_on_file, draw_riversmap_on_file, draw_scatter_plot_on_file, \
    draw_satellite_on_file, draw_icecaps_on_file, draw_wind_on_file, draw_permeability_on_file, \
    draw_humidity_on_file, draw_plates_on_file
from imex import export
from model.world import World
from plates import world_gen
from version import __version__
from PyQt4.QtCore import pyqtSlot
from step import Step
from world3d import world3dA

try:
    from hdf5_serialization import save_world_to_hdf5

    HDF5_AVAILABLE = True
except:
    HDF5_AVAILABLE = False

VERSION = __version__

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from OpenGL.GLUT import *

# import new_gui_4_rc

from height2bump import readHeight2Bump

FORM_1, BASE_1 = uic.loadUiType('new_gui_6.ui')
FORM_2, BASE_2 = uic.loadUiType('popup.ui')
FORM_3, BASE_3 = uic.loadUiType('dialog.ui')
FORM_4, BASE_4 = uic.loadUiType('3d.ui')


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


class FORM4(BASE_4, FORM_4):
    def __init__(self, parent=None):
        super(FORM4, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/Icon.png'))
        self.setModal(QtCore.Qt.ApplicationModal)


class MyApp(FORM_1, BASE_1):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.sshFile = ''

        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.cboFormat.view().setMinimumWidth(430)
        self.cboAncFormat.view().setMinimumWidth(430)

        self.popup = FORM2()
        self.dialog = FORM3()
        self.dialog.closeEvent = self.closeEvent
        self._3d = FORM4()
        self.sAll = 'all'

        self.connect(self.btnDown, QtCore.SIGNAL('released()'), self.btnDown_Clicked)
        self.connect(self.btnAW, QtCore.SIGNAL('released()'), self.btnAncient_Clicked)
        self.connect(self.btnGH, QtCore.SIGNAL('released()'), self.btnHeightmap_Clicked)
        self.connect(self.btnSM, QtCore.SIGNAL('released()'), self.btnSatellite_Clicked)
        self.connect(self.btnSP, QtCore.SIGNAL('released()'), self.btnScatter_Clicked)
        self.connect(self.btnUp, QtCore.SIGNAL('released()'), self.btnUp_Clicked)
        self.connect(self.btnUpdate, QtCore.SIGNAL('released()'), self.btnUpdate_Clicked)
        self.connect(self.btnRandomise, QtCore.SIGNAL('released()'), self.btnRandomise_Clicked)
        self.connect(self.btnGenWorld, QtCore.SIGNAL('released()'), self.onActionGenerate)
        self.connect(self.btnGenWorld_3, QtCore.SIGNAL('released()'), self.onActionAncient)
        self.connect(self.btnExport, QtCore.SIGNAL('released()'), self.onActionExportWorld)

        self.connect(self.actionNew, QtCore.SIGNAL('triggered()'), self.onActionNew)
        self.connect(self.actionOpen, QtCore.SIGNAL('triggered()'), self.onActionOpen)
        self.connect(self.action_Save, QtCore.SIGNAL('triggered()'), self.onActionSave)
        self.connect(self.actionSave_All_Maps_As, QtCore.SIGNAL('triggered()'), self.onActionSaveAllAs)
        self.connect(self.actionSet_Output_Directory, QtCore.SIGNAL('triggered()'), self.onActionSetOutputDirectory)
        self.connect(self.action_Print_Current_Map_View, QtCore.SIGNAL('triggered()'), self.onActionPrint)
        self.connect(self.actionSave_Current_Map_View, QtCore.SIGNAL('triggered()'), self.onActionSaveCurrentView)
        self.connect(self.action_Quit, QtCore.SIGNAL('triggered()'), self.onActionQuit)
        self.connect(self.actionZoom_In, QtCore.SIGNAL('triggered()'), self.onActionZoomIn)
        self.connect(self.actionZoom_Out, QtCore.SIGNAL('triggered()'), self.onActionZoomOut)
        self.connect(self.actionFit_to_Width, QtCore.SIGNAL('triggered()'), self.onActionFitWidth)
        self.connect(self.actionFit_to_Height, QtCore.SIGNAL('triggered()'), self.onActionFitHeight)
        self.connect(self.actionActual_Size, QtCore.SIGNAL('triggered()'), self.onActionFitActual)
        self.connect(self.actionFit_to_Window, QtCore.SIGNAL('triggered()'), self.onActionFitWindow)
        self.connect(self.action_Help, QtCore.SIGNAL('triggered()'), self.onActionHelp)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.onActionAbout)
        self.connect(self.actionGenerate_World, QtCore.SIGNAL('triggered()'), self.onActionGenerate)
        self.connect(self.actionGrayscale_Heightmap, QtCore.SIGNAL('triggered()'), self.onActionMapsGrayscale1)
        self.connect(self.actionScatter_Plot, QtCore.SIGNAL('triggered()'), self.onActionMapsScatter1)
        self.connect(self.actionSatellite_View, QtCore.SIGNAL('triggered()'), self.onActionMapsSatellite1)
        self.connect(self.actionGenerate_Ancient_World, QtCore.SIGNAL('triggered()'), self.onActionAncient)
        self.connect(self.actionExport_World, QtCore.SIGNAL('triggered()'), self.onActionExportWorld)
        self.connect(self.action3D_View, QtCore.SIGNAL('triggered()'), self.onAction3DView)

        self.connect(self.actionWindows, QtCore.SIGNAL('triggered()'), self.onActionWindows)
        self.connect(self.actionWindows_XP, QtCore.SIGNAL('triggered()'), self.onActionWindowsXP)
        self.connect(self.actionWindows_Vista, QtCore.SIGNAL('triggered()'), self.onActionWindowsVista)
        self.connect(self.actionMotif, QtCore.SIGNAL('triggered()'), self.onActionMotif)
        self.connect(self.actionCDE, QtCore.SIGNAL('triggered()'), self.onActionCDE)
        self.connect(self.actionPlastique, QtCore.SIGNAL('triggered()'), self.onActionPlastique)
        self.connect(self.actionClean_Looks, QtCore.SIGNAL('triggered()'), self.onActionCleanLooks)
        self.connect(self.actionDark_Orange, QtCore.SIGNAL('triggered()'), self.onActionDarkOrange)

        self.connect(self.dialog.btnCentre, QtCore.SIGNAL('released()'), self.btnCentre_Clicked)
        self.connect(self.dialog.btnRight, QtCore.SIGNAL('released()'), self.btnRight_Clicked)

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

        self.connect(self.tblMapList, QtCore.SIGNAL('itemSelectionChanged()'), self.tblMapListChanged)
        self.connect(self.spnOpacity, QtCore.SIGNAL('valueChanged(int)'), self.spnOpacityChanged)

        self.connect(self.gvLarge.horizontalScrollBar(), QtCore.SIGNAL('valueChanged(int)'), self.gvLargeSBHorChanged)
        self.connect(self.gvLarge.verticalScrollBar(), QtCore.SIGNAL('valueChanged(int)'), self.gvLargeSBVertChanged)

        self.connect(self.spnWidth, QtCore.SIGNAL('valueChanged(int)'), self.spnWidthChanged)
        self.connect(self.spnHeight, QtCore.SIGNAL('valueChanged(int)'), self.spnHeightChanged)

        self.changeScene('No World loaded')

        self.setDefaults()

        self.clearLists()

    def setDefaults(self):
        self.setBlankStylesheet()
        self.sWorld = ''
        self.world = None
        self.sOutputDirectory, _ = os.path.split(sys.argv[0])

        if self.sOutputDirectory == "":
            self.sOutputDirectory = "."

        self.sDefaultDirectory = self.sOutputDirectory
        self.sSeed = ''
        self.iSeed = 11111
        self.iDrag = 0
        self.iMsg = 0
        self.mapDict = dict()
        self.bBW = False
        self.lblCurrentMap.setText('No Maps Available')
        self.bPNG = False

        self.actionGenerate_World.setEnabled(True)
        self.enableButtons(False)

        # These are the Ancient Map Options
        self.spnResize.setValue(1.0)
        self.rdoSeaBrown_3.setChecked(True)
        self.rdoLandBrown.setChecked(True)
        self.rdoBiomesYes_3.setChecked(True)
        self.rdoMountYes_3.setChecked(True)
        self.rdoRiverYes_3.setChecked(True)
        self.rdoLandYes_3.setChecked(True)
        self.cboAncData.setCurrentIndex(0)
        self.cboAncFormat.setCurrentIndex(1)

        self.spnResize.setEnabled(False)
        self.grpSea.setEnabled(False)
        self.grpLand.setEnabled(False)
        self.grpBiomes.setEnabled(False)
        self.grpMountains.setEnabled(False)
        self.grpRivers.setEnabled(False)
        self.grpBorder.setEnabled(False)
        self.grpVerbose_2.setEnabled(False)
        self.cboAncData.setEnabled(False)
        self.cboAncFormat.setEnabled(False)
        self.btnGenWorld_3.setEnabled(False)

        self.bAncSeaColour = True
        self.bAncLandColour = True
        self.bAncBiomes = True
        self.bAncRivers = True
        self.bAncMountains = True
        self.bAncBorders = True
        self.sAncFormat = self.cboAncFormat.currentText()
        self.sAncDataType = self.cboAncData.currentText()

        self.sAncFormat = self.sAncFormat[-5:]

        if self.sAncFormat[:1] == '(':
            self.sAncFormat = self.sAncFormat[1:4]
        elif self.sAncFormat[:1] == ' ':
            self.sAncFormat = self.sAncFormat[2:4]
        else:
            self.sAncFormat = self.sAncFormat[:4]

        # These are the World Options
        self.spnSeed.setValue(11111)
        self.spnWidth.setValue(1024)
        self.spnHeight.setValue(1024)
        self.spnPlates.setValue(10)
        self.spnRecursion.setValue(2000)
        self.cboFormat.setCurrentIndex(1)
        self.cboData.setCurrentIndex(0)

        self.sFormat = self.cboFormat.currentText()

        self.sFormat = self.sFormat[-5:]

        if self.sFormat[:1] == '(':
            self.sFormat = self.sFormat[1:4]
        elif self.sFormat[:1] == ' ':
            self.sFormat = self.sFormat[2:4]
        else:
            self.sFormat = self.sFormat[:4]

        self.rdoBWNo.setChecked(True)
        self.rdoVMNo.setChecked(True)
        self.rdoPBYes.setChecked(True)
        self.rdoFadeYes.setChecked(True)
        self.spnSea.setValue(1.000)
        self.spnTemp1.setValue(0.126)
        self.spnTemp2.setValue(0.235)
        self.spnTemp3.setValue(0.406)
        self.spnTemp4.setValue(0.561)
        self.spnTemp5.setValue(0.634)
        self.spnTemp6.setValue(0.876)
        self.spnPrecip1.setValue(0.059)
        self.spnPrecip2.setValue(0.222)
        self.spnPrecip3.setValue(0.493)
        self.spnPrecip4.setValue(0.764)
        self.spnPrecip5.setValue(0.927)
        self.spnPrecip6.setValue(0.986)
        self.spnPrecip7.setValue(0.998)
        self.spnGamma.setValue(1.250)
        self.spnOffset.setValue(0.200)
        self.spnSeaLevel.setValue(0.65)
        self.spnErosionPeriod.setValue(60)
        self.spnFoldingRatio.setValue(0.02)
        self.spnAggAbs.setValue(1000000)
        self.spnAggRel.setValue(0.33)
        self.spnNumCycles.setValue(2)
        self.spnExportWidth.setValue(1024)
        self.spnExportHeight.setValue(1024)
        self.spnExportNormMin.setValue(0)
        self.spnExportNormMax.setValue(1024)
        self.spnExportSubStartW.setValue(0)
        self.spnExportSubStartH.setValue(0)
        self.spnExportSubOffW.setValue(1024)
        self.spnExportSubOffH.setValue(1024)
        self.cboExportResample.setCurrentIndex(3)

        self.spnSeed.setEnabled(True)
        self.btnRandomise.setEnabled(True)
        self.spnWidth.setEnabled(True)
        self.spnHeight.setEnabled(True)
        self.spnPlates.setEnabled(True)
        self.spnRecursion.setEnabled(True)
        self.cboFormat.setEnabled(True)
        self.cboData.setEnabled(True)

        self.grpBW.setEnabled(True)
        self.grpVerbose.setEnabled(True)
        self.grpProtocol.setEnabled(True)
        self.grpFade.setEnabled(True)
        self.spnSea.setEnabled(True)
        self.spnTemp1.setEnabled(True)
        self.spnTemp2.setEnabled(True)
        self.spnTemp3.setEnabled(True)
        self.spnTemp4.setEnabled(True)
        self.spnTemp5.setEnabled(True)
        self.spnTemp6.setEnabled(True)
        self.spnPrecip1.setEnabled(True)
        self.spnPrecip2.setEnabled(True)
        self.spnPrecip3.setEnabled(True)
        self.spnPrecip4.setEnabled(True)
        self.spnPrecip5.setEnabled(True)
        self.spnPrecip6.setEnabled(True)
        self.spnPrecip7.setEnabled(True)
        self.spnGamma.setEnabled(True)
        self.spnOffset.setEnabled(True)
        self.spnSeaLevel.setEnabled(True)
        self.spnErosionPeriod.setEnabled(True)
        self.spnFoldingRatio.setEnabled(True)
        self.spnAggAbs.setEnabled(True)
        self.spnAggRel.setEnabled(True)
        self.spnNumCycles.setEnabled(True)

        self.spnExportWidth.setEnabled(True)
        self.spnExportHeight.setEnabled(True)
        self.spnExportNormMin.setEnabled(True)
        self.spnExportNormMax.setEnabled(True)
        self.spnExportSubStartW.setEnabled(True)
        self.spnExportSubStartH.setEnabled(True)
        self.spnExportSubOffW.setEnabled(True)
        self.spnExportSubOffH.setEnabled(True)
        self.cboExportResample.setEnabled(True)

        self.defaultMapOptions()

    def enableWorldOptions(self):
        fName = '%s/%s.cfg' % (self.sDefaultDirectory, self.iSeed)

        if os.path.isfile(fName):
            config = configparser2.ConfigParser()
            config.read(fName)

            sResize = config.get('ancient', 'spnResize')
            sSea = config.get('ancient', 'rdoSea')
            sLandCol = config.get('ancient', 'rdoLandCol')
            sBiomes = config.get('ancient', 'rdoBiomes')
            sMount = config.get('ancient', 'rdoMount')
            sRivers = config.get('ancient', 'rdoRivers')
            sLand = config.get('ancient', 'rdoLand')
            sAncData = config.get('ancient', 'cboAncData')
            sAncFormat1 = config.get('ancient', 'cboAncFormat')

            sWidth = config.get('world', 'spnWidth')
            sHeight = config.get('world', 'spnHeight')
            sPlates = config.get('world', 'spnPlates')
            sRecursion = config.get('world', 'spnRecursion')
            sFormat1 = config.get('world', 'cboFormat')
            sData = config.get('world', 'cboData')
            sBW = config.get('world', 'rdoBW')
            sVM = config.get('world', 'rdoVM')
            sPB = config.get('world', 'rdoPB')
            sFade = config.get('world', 'rdoFade')
            sSeaLevel = config.get('world', 'spnSea')
            sTemp1 = config.get('world', 'spnTemp1')
            sTemp2 = config.get('world', 'spnTemp2')
            sTemp3 = config.get('world', 'spnTemp3')
            sTemp4 = config.get('world', 'spnTemp4')
            sTemp5 = config.get('world', 'spnTemp5')
            sTemp6 = config.get('world', 'spnTemp6')
            sPrecip1 = config.get('world', 'spnPrecip1')
            sPrecip2 = config.get('world', 'spnPrecip2')
            sPrecip3 = config.get('world', 'spnPrecip3')
            sPrecip4 = config.get('world', 'spnPrecip4')
            sPrecip5 = config.get('world', 'spnPrecip5')
            sPrecip6 = config.get('world', 'spnPrecip6')
            sPrecip7 = config.get('world', 'spnPrecip7')
            sGamma = config.get('world', 'spnGamma')
            sOffset = config.get('world', 'spnOffset')
            sOceanLevel = config.get('world', 'spnSeaLevel')
            sErosionPeriod = config.get('world', 'spnErosionPeriod')
            sFoldingRatio = config.get('world', 'spnFoldingRatio')
            sAggAbs = config.get('world', 'spnAggAbs')
            sAggRel = config.get('world', 'spnAggRel')
            sNumCycles = config.get('world', 'spnNumCycles')
            sExportWidth = config.get('world', 'spnExportWidth')
            sExportHeight = config.get('world', 'spnExportHeight')
            sExportNormMin = config.get('world', 'spnExportNormMin')
            sExportNormMax = config.get('world', 'spnExportNormMax')
            sExportSubStartW = config.get('world', 'spnExportSubStartW')
            sExportSubStartH = config.get('world', 'spnExportSubStartH')
            sExportSubOffW = config.get('world', 'spnExportSubOffW')
            sExportSubOffH = config.get('world', 'spnExportSubOffH')
            sExportResample = config.get('world', 'cboExportResample')

            self.erosion_max_radius = config.get('map', 'erosion_max_radius')
            self.erosion_maxRadius = config.get('map', 'erosion_maxRadius')
            self.erosion_radius = config.get('map', 'erosion_radius')
            self.erosion_curve1 = config.get('map', 'erosion_curve1')
            self.erosion_curve2 = config.get('map', 'erosion_curve2')
            self.erosion_curve3 = config.get('map', 'erosion_curve3')
            self.humidity_precipitation_weight = config.get('map', 'humidity_precipitation_weight')
            self.humidity_irrigation_weight = config.get('map', 'humidity_irrigation_weight')
            self.hydrology_creek = config.get('map', 'hydrology_creek')
            self.hydrology_river = config.get('map', 'hydrology_river')
            self.hydrology_main_river = config.get('map', 'hydrology_main_river')
            self.icecap_max_freeze_percentage = config.get('map', 'icecap_max_freeze_percentage')
            self.icecap_freeze_chance_window = config.get('map', 'icecap_freeze_chance_window')
            self.icecap_surrounding_tile_influence = config.get('map', 'icecap_surrounding_tile_influence')
            self.irrigation_radius = config.get('map', 'irrigation_radius')
            self.permeability_perm_th_low = config.get('map', 'permeability_perm_th_low')
            self.permeability_perm_th_med = config.get('map', 'permeability_perm_th_med')
            self.permeability_octaves = config.get('map', 'permeability_octaves')
            self.permeability_freq = config.get('map', 'permeability_freq')
            self.precipitation_ths_low = config.get('map', 'precipitation_ths_low')
            self.precipitation_ths_med = config.get('map', 'precipitation_ths_med')
            self.precipitation_octaves = config.get('map', 'precipitation_octaves')
            self.precipitation_freq = config.get('map', 'precipitation_freq')
            self.temperature_distance_to_sun_hwhm = config.get('map', 'temperature_distance_to_sun_hwhm')
            self.temperature_axial_tilt_hwhm = config.get('map', 'temperature_axial_tilt_hwhm')
            self.temperature_octaves = config.get('map', 'temperature_octaves')
            self.temperature_frequency = config.get('map', 'temperature_frequency')
            self.wind_octaves = config.get('map', 'wind_octaves')
            self.wind_frequency = config.get('map', 'wind_frequency')
        else:
            # set values from world file
            # Will probably need to set Ancient Map options to DEFAULTS
            sResize = '1'
            sSea = 'True'
            sLandCol = 'True'
            sBiomes = 'True'
            sMount = 'True'
            sRivers = 'True'
            sLand = 'True'
            sAncData = '0'
            sAncFormat1 = '1'

            sWidth = str(self.world.width)
            sHeight = str(self.world.height)
            sPlates = str(self.world.n_plates)
            sRecursion = '2000'
            sFormat1 = '1'
            sData = '0'
            sBW = 'False'
            sVM = 'False'
            sPB = 'True'
            sFade = 'True'
            sSeaLevel = str(self.world.ocean_level)
            sTemp1 = self.world.temps[5]
            sTemp2 = self.world.temps[4]
            sTemp3 = self.world.temps[3]
            sTemp4 = self.world.temps[2]
            sTemp5 = self.world.temps[1]
            sTemp6 = self.world.temps[0]
            sPrecip1 = self.world.humids[6]
            sPrecip2 = self.world.humids[5]
            sPrecip3 = self.world.humids[4]
            sPrecip4 = self.world.humids[3]
            sPrecip5 = self.world.humids[2]
            sPrecip6 = self.world.humids[1]
            sPrecip7 = self.world.humids[0]
            sGamma = str(self.world.gamma_curve)
            sOffset = str(self.world.curve_offset)
            sOceanLevel = '0.65'
            sErosionPeriod = '60'
            sFoldingRatio = '0.02'
            sAggAbs = '1000000'
            sAggRel = '0.33'
            sNumCycles = '2'
            sExportWidth = '1024'
            sExportHeight = '1024'
            sExportNormMin = '0'
            sExportNormMax = '1024'
            sExportSubStartW = '0'
            sExportSubStartH = '0'
            sExportSubOffW = '1024'
            sExportSubOffH = '1024'
            sExportResample = '3'

            self.setDefaultMapOptions()

        # These are the Ancient Map Options
        self.spnResize.setValue(float(sResize))

        if sSea == 'True':
            self.rdoSeaBrown_3.setChecked(True)
        else:
            self.rdoSeaBrown_3.setChecked(False)

        if sLandCol == 'True':
            self.rdoLandBrown.setChecked(True)
        else:
            self.rdoLandBrown.setChecked(False)

        if sBiomes == 'True':
            self.rdoBiomesYes_3.setChecked(True)
        else:
            self.rdoBiomesYes_3.setChecked(False)

        if sMount == 'True':
            self.rdoMountYes_3.setChecked(True)
        else:
            self.rdoMountYes_3.setChecked(False)

        if sRivers == 'True':
            self.rdoRiverYes_3.setChecked(True)
        else:
            self.rdoRiverYes_3.setChecked(False)

        if sLand == 'True':
            self.rdoLandYes_3.setChecked(True)
        else:
            self.rdoLandYes_3.setChecked(False)

        self.cboAncData.setCurrentIndex(int(sAncData))
        self.cboAncFormat.setCurrentIndex(int(sAncFormat1))

        if sAncFormat1 == '0':
            self.sAncFormat = 'jpeg'
        elif sAncFormat1 == '2':
            self.sAncFormat = 'bmp'
        elif sAncFormat1 == '3':
            self.sAncFormat = 'gif'
        else:
            self.sAncFormat = 'png'

        self.spnResize.setEnabled(True)
        self.grpSea.setEnabled(True)
        self.grpLand.setEnabled(True)
        self.grpBiomes.setEnabled(True)
        self.grpMountains.setEnabled(True)
        self.grpRivers.setEnabled(True)
        self.grpBorder.setEnabled(True)
        self.grpVerbose_2.setEnabled(True)
        self.cboAncData.setEnabled(True)
        self.cboAncFormat.setEnabled(True)
        self.btnGenWorld_3.setEnabled(True)

        # These are the World Options
        self.spnSeed.setValue(self.iSeed)
        self.spnWidth.setValue(int(sWidth))
        self.spnHeight.setValue(int(sHeight))
        self.spnPlates.setValue(int(sPlates))
        self.spnRecursion.setValue(int(sRecursion))
        self.cboFormat.setCurrentIndex(int(sFormat1))
        self.cboData.setCurrentIndex(int(sData))

        if sFormat1 == '0':
            self.sFormat = 'jpeg'
        elif sFormat1 == '2':
            self.sFormat = 'bmp'
        elif sFormat1 == '3':
            self.sFormat = 'gif'
        else:
            self.sFormat = 'png'

        if sBW == 'True':
            self.rdoBWNo.setChecked(True)
        else:
            self.rdoBWNo.setChecked(False)

        if sVM == 'True':
            self.rdoVMNo.setChecked(True)
        else:
            self.rdoVMNo.setChecked(False)

        if sPB == 'True':
            self.rdoPBYes.setChecked(True)
        else:
            self.rdoPBYes.setChecked(False)

        if sFade == 'True':
            self.rdoFadeYes.setChecked(True)
        else:
            self.rdoFadeYes.setChecked(False)

        self.spnSea.setValue(float(sSeaLevel))
        self.spnTemp1.setValue(float(sTemp1))
        self.spnTemp2.setValue(float(sTemp2))
        self.spnTemp3.setValue(float(sTemp3))
        self.spnTemp4.setValue(float(sTemp4))
        self.spnTemp5.setValue(float(sTemp5))
        self.spnTemp6.setValue(float(sTemp6))
        self.spnPrecip1.setValue(float(sPrecip1))
        self.spnPrecip2.setValue(float(sPrecip2))
        self.spnPrecip3.setValue(float(sPrecip3))
        self.spnPrecip4.setValue(float(sPrecip4))
        self.spnPrecip5.setValue(float(sPrecip5))
        self.spnPrecip6.setValue(float(sPrecip6))
        self.spnPrecip7.setValue(float(sPrecip7))
        self.spnGamma.setValue(float(sGamma))
        self.spnOffset.setValue(float(sOffset))
        self.spnSeaLevel.setValue(float(sOceanLevel))
        self.spnErosionPeriod.setValue(int(sErosionPeriod))
        self.spnFoldingRatio.setValue(float(sFoldingRatio))
        self.spnAggAbs.setValue(int(sAggAbs))
        self.spnAggRel.setValue(float(sAggRel))
        self.spnNumCycles.setValue(int(sNumCycles))
        self.spnExportWidth.setValue(int(sExportWidth))
        self.spnExportHeight.setValue(int(sExportHeight))
        self.spnExportNormMin.setValue(int(sExportNormMin))
        self.spnExportNormMax.setValue(int(sExportNormMax))
        self.spnExportSubStartW.setValue(int(sExportSubStartW))
        self.spnExportSubStartH.setValue(int(sExportSubStartH))
        self.spnExportSubOffW.setValue(int(sExportSubOffW))
        self.spnExportSubOffH.setValue(int(sExportSubOffH))

        if sExportResample == 'Nearest Neighbour':
            self.cboExportResample.setCurrentIndex(0)
        elif sExportResample == 'Bilinear':
            self.cboExportResample.setCurrentIndex(1)
        elif sExportResample == 'Cubic':
            self.cboExportResample.setCurrentIndex(2)
        elif sExportResample == 'Cubic Spline':
            self.cboExportResample.setCurrentIndex(3)
        elif sExportResample == 'Lanczos':
            self.cboExportResample.setCurrentIndex(4)
        elif sExportResample == 'Average':
            self.cboExportResample.setCurrentIndex(5)
        else:
            self.cboExportResample.setCurrentIndex(6)

        self.enableButtons(True)

    def gvLargeSBVertChanged(self, iInt):
        self.updateBox()

    def gvLargeSBHorChanged(self, iInt):
        self.updateBox()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Drop:
            mimeData = event.mimeData()

            for mimeFormat in mimeData.formats():
                if mimeFormat != 'application/x-qabstractitemmodeldatalist':
                    continue

                data = self.decodeMimeData(mimeData.data(mimeFormat))

                if source == self.tblMapList.viewport():
                    if self.iDrag % 2 == 0:
                        curRowCount = self.tblMapList.rowCount()
                        self.tblMapList.insertRow(curRowCount)
                        iTemp = QtGui.QTableWidgetItem(data)
                        self.tblMapList.setItem(curRowCount, 0, iTemp)
                        self.tblMapList.setCurrentCell(curRowCount, 0)

                        sTemp = self.tblMapList.item(curRowCount, 0).text()

                        if sTemp not in self.mapDict:
                            self.mapDict[sTemp] = 255

                            self.lblCurrentMap.setEnabled(True)
                            self.spnOpacity.setEnabled(True)

                            self.tblAvailable.removeRow(self.tblAvailable.currentRow())
                            self.tblAvailable.setCurrentCell(0, 0)

                            self.btnUpdate.setEnabled(True)

                            if curRowCount > 0:
                                self.btnUp.setEnabled(True)
                                self.btnDown.setEnabled(True)
                            else:
                                self.btnUp.setEnabled(False)
                                self.btnDown.setEnabled(False)

                            self.spnOpacity.setValue(self.mapDict[sTemp])

                            self.updateOpacities()
                elif source == self.tblAvailable.viewport():
                    if self.iDrag % 2 == 0:
                        curRowCount = self.tblAvailable.rowCount()
                        self.tblAvailable.insertRow(curRowCount)
                        iTemp = QtGui.QTableWidgetItem(data)
                        self.tblAvailable.setItem(curRowCount, 0, QtGui.QTableWidgetItem(iTemp))
                        self.tblAvailable.setCurrentCell(curRowCount, 0)

                        self.tblMapList.removeRow(self.tblMapList.currentRow())
                        self.tblMapList.setCurrentCell(0, 0)

                        curRowCount = self.tblMapList.rowCount()

                        if curRowCount > 0:
                            self.btnUpdate.setEnabled(True)

                            sTemp = self.tblMapList.item(0, 0).text()
                            self.spnOpacity.setValue(self.mapDict[sTemp])
                        else:
                            self.btnUpdate.setEnabled(False)
                            self.lblCurrentMap.setText('None')
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
                            self.actionSave_All_Maps_As.setEnabled(False)
                            self.action_Print_Current_Map_View.setEnabled(False)
                            self.actionSave_Current_Map_View.setEnabled(False)

                        if curRowCount > 1:
                            self.btnUp.setEnabled(True)
                            self.btnDown.setEnabled(True)
                        else:
                            self.btnUp.setEnabled(False)
                            self.btnDown.setEnabled(False)

                        self.updateOpacities()

            self.iDrag = 0
        elif event.type() == QtCore.QEvent.DragEnter:
            self.iDrag += 1
        elif event.type() == QtCore.QEvent.DragLeave:
            pass

        return QtGui.QMainWindow.eventFilter(self, source, event)

    def updateOpacities(self):
        curRowCount = self.tblMapList.rowCount() - 1

        if curRowCount > 0:
            sTemp = self.tblMapList.item(curRowCount, 0).text()

            for k, v in self.mapDict.iteritems():
                if k == sTemp:
                    self.mapDict[k] = 255
                else:
                    if v == 255:
                        self.mapDict[k] = 127

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
        self.updateOpacities()

        for k, v in self.mapDict.iteritems():
            if k == sTmp:
                self.spnOpacity.setValue(v)

    def spnOpacityChanged(self, iInt):
        iRow = self.tblMapList.currentRow()
        sTmp = self.tblMapList.item(iRow, 0).text()
        self.mapDict[sTmp] = iInt
        self.updateOpacities()

    def btnDown_Clicked(self):
        iRow = self.tblMapList.currentRow()

        if iRow is None:
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
            self.updateOpacities()

    def btnAncient_Clicked(self):
        self.onMapBtnUpdate('ancient_world')

    def btnHeightmap_Clicked(self):
        self.onMapBtnUpdate('grayscale')

    def btnSatellite_Clicked(self):
        self.onMapBtnUpdate('satellite')

    def btnScatter_Clicked(self):
        self.onMapBtnUpdate('scatter')

    def spnWidthChanged(self):
        self.spnExportWidth.setValue(self.spnWidth.value())
        self.spnExportSubOffW.setValue(self.spnWidth.value())

        if self.spnWidth.value() > self.spnHeight.value():
            self.spnExportNormMax.setValue(self.spnWidth.value())

    def spnHeightChanged(self):
        self.spnExportHeight.setValue(self.spnHeight.value())
        self.spnExportSubOffH.setValue(self.spnHeight.value())

        if self.spnHeight.value() > self.spnWidth.value():
            self.spnExportNormMax.setValue(self.spnHeight.value())

    def onMapBtnUpdate(self, inStr):
        self.gvSceneSm = QtGui.QGraphicsScene()
        self.gvSceneLg = QtGui.QGraphicsScene()

        self.actionZoom_In.setEnabled(True)
        self.actionZoom_Out.setEnabled(True)
        self.actionFit_to_Width.setEnabled(True)
        self.actionFit_to_Height.setEnabled(True)
        self.actionActual_Size.setEnabled(True)
        self.actionFit_to_Window.setEnabled(True)
        self.action_Save.setEnabled(True)
        self.actionSave_All_Maps_As.setEnabled(True)
        self.action_Print_Current_Map_View.setEnabled(True)
        self.actionSave_Current_Map_View.setEnabled(True)

        if inStr != 'ancient_world':
            if self.sFormat == 'png' or self.sFormat == 'jpg' or self.sFormat == 'jpeg' or self.sFormat == 'bmp':
                sTmp = '%s/Maps/seed_%s_%s.%s' % (self.sDefaultDirectory, self.iSeed, inStr, self.sFormat)
            else:
                sTmp = '%s/Maps/seed_%s_%s.png' % (self.sDefaultDirectory, self.iSeed, inStr)
        else:
            if self.sAncFormat == 'png' or self.sAncFormat == 'jpg' or self.sAncFormat == 'jpeg' or self.sAncFormat == 'bmp':
                sTmp = '%s/Maps/seed_%s_%s.%s' % (self.sDefaultDirectory, self.iSeed, inStr, self.sAncFormat)
            else:
                sTmp = '%s/Maps/seed_%s_%s.png' % (self.sDefaultDirectory, self.iSeed, inStr)

        self.pixmap = QtGui.QPixmap(sTmp)
        piPixItemLg = QtGui.QGraphicsPixmapItem()
        piPixItemLg.setPixmap(self.pixmap)
        piPixItemLg.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)
        piPixItemSm = QtGui.QGraphicsPixmapItem()
        piPixItemSm.setPixmap(self.pixmap)
        piPixItemSm.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)

        piPixItemLg.setOpacity(1)
        piPixItemSm.setOpacity(1)

        self.gvSceneLg.addItem(piPixItemLg)
        self.gvSceneSm.addItem(piPixItemSm)

        self.gvSmall.setScene(self.gvSceneSm)
        self.gvSmall.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        self.gvLarge.setScene(self.gvSceneLg)
        self.gvLarge.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)

        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvSmall.centerOn(0, 0)
        self.gvSmall.fitInView(bounds, QtCore.Qt.KeepAspectRatio)

        self.onActionFitWindow()

        self.updateBox()

    def btnUp_Clicked(self):
        iRow = self.tblMapList.currentRow()

        if iRow is None:
            iRow = self.tblMapList.rowCount() - 1

        if iRow > 0:
            item1 = self.tblMapList.item(iRow, 0)
            item2 = self.tblMapList.item(iRow - 1, 0)
            sText = item1.text()
            sText1 = item2.text()

            item1.setText(sText1)
            item2.setText(sText)

            self.tblMapList.setCurrentCell(iRow - 1, 0)
            self.updateOpacities()

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
        self.actionSave_All_Maps_As.setEnabled(True)
        self.action_Print_Current_Map_View.setEnabled(True)
        self.actionSave_Current_Map_View.setEnabled(True)

        for index in reversed(xrange(self.tblMapList.rowCount())):
            if self.sFormat == 'png' or self.sFormat == 'jpg' or self.sFormat == 'jpeg' or self.sFormat == 'bmp':
                sTmp = '%s/Maps/seed_%s_%s.%s' % (self.sDefaultDirectory, self.iSeed, self.tblMapList.item(index, 0).text(), self.sFormat)
            else:
                sTmp = '%s/Maps/seed_%s_%s.png' % (self.sDefaultDirectory, self.iSeed, self.tblMapList.item(index, 0).text())

            self.pixmap = QtGui.QPixmap(sTmp)
            piPixItemLg = QtGui.QGraphicsPixmapItem()
            piPixItemLg.setPixmap(self.pixmap)
            piPixItemLg.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)
            piPixItemSm = QtGui.QGraphicsPixmapItem()
            piPixItemSm.setPixmap(self.pixmap)
            piPixItemSm.setFlag(QtGui.QGraphicsPixmapItem.ItemIgnoresParentOpacity, True)

            sTemp = self.tblMapList.item(index, 0).text()

            if not bFirst:
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
        self.gvSmall.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        self.gvLarge.setScene(self.gvSceneLg)
        self.gvLarge.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)

        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvSmall.centerOn(0, 0)
        self.gvSmall.fitInView(bounds, QtCore.Qt.KeepAspectRatio)

        self.onActionFitWindow()

        self.updateBox()

    def setDefaultMapOptions(self):
        self.erosion_max_radius = 40
        self.spnRFRadius.setValue(40)
        self.erosion_maxRadius = 40
        self.spnRERadius.setValue(40)
        self.erosion_radius = 2
        self.spnFLERadius.setValue(2)
        self.erosion_curve1 = 1.0
        self.spnREC1.setValue(1.0)
        self.erosion_curve2 = 0.2
        self.spnREC2.setValue(0.2)
        self.erosion_curve3 = 0.05
        self.spnREC3.setValue(0.05)
        self.humidity_precipitation_weight = 1.0
        self.spnPW.setValue(1.0)
        self.humidity_irrigation_weight = 3.0
        self.spnIW.setValue(3.0)
        self.hydrology_creek = 0.05
        self.spnTHCreek.setValue(0.05)
        self.hydrology_river = 0.02
        self.spnTHRiver.setValue(0.02)
        self.hydrology_main_river = 0.007
        self.spnTHMainRiver.setValue(0.007)
        self.icecap_max_freeze_percentage = 0.60
        self.spnMFP.setValue(0.60)
        self.icecap_freeze_chance_window = 0.2
        self.spnFCW.setValue(0.2)
        self.icecap_surrounding_tile_influence = 0.5
        self.spnSTI.setValue(0.5)
        self.irrigation_radius = 10
        self.spnIrrRad.setValue(10)
        self.permeability_perm_th_low = 0.75
        self.spnPermTHL.setValue(0.75)
        self.permeability_perm_th_med = 0.25
        self.spnPermTHM.setValue(0.25)
        self.permeability_octaves = 6
        self.spnPermOct.setValue(6)
        self.permeability_freq = 64.0
        self.spnPermFreq.setValue(64.0)
        self.precipitation_ths_low = 0.75
        self.spnPrecTHL.setValue(0.75)
        self.precipitation_ths_med = 0.3
        self.spnPrecTHM.setValue(0.3)
        self.precipitation_octaves = 6
        self.spnPrecOct.setValue(6)
        self.precipitation_freq = 64.0
        self.spnPrecFreq.setValue(64.0)
        self.temperature_distance_to_sun_hwhm = 0.12
        self.spnDistSun.setValue(0.12)
        self.temperature_axial_tilt_hwhm = 0.07
        self.spnAxTilt.setValue(0.07)
        self.temperature_octaves = 8
        self.spnTempOct.setValue(8)
        self.temperature_frequency = 16.0
        self.spnTempFreq.setValue(16.0)
        self.wind_octaves = 6
        self.spnWindOct.setValue(6)
        self.wind_frequency = 64.0
        self.spnWindFreq.setValue(64.0)

    def defaultMapOptions(self):
        self.setDefaultMapOptions()

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

    def btnRandomise_Clicked(self):
        from random import randint

        self.iSeed = randint(1, 65535)
        self.spnSeed.setValue(self.iSeed)
        self.sWorld = 'seed_%s.world' % str(self.iSeed)

    def onActionNew(self):
        self.showDialog('Are you sure you want to reset all the Data?', 'Yes', 'No', True, 1, ':Images\question.png')

    def onActionOpen(self):
        tDialog = QtGui.QFileDialog()
        tDialog.setDirectory(self.sDefaultDirectory)

        sTmp = tDialog.getOpenFileName(self, 'Open World File', '.', 'World Files (*.world)', '', QtGui.QFileDialog.DontUseNativeDialog)
        fi = QtCore.QFileInfo(sTmp)
        self.sWorld = "%s.world" % fi.baseName()

        if fi.baseName():
            self.popup.show()
            self.popup.textBrowser.setText('')
            self.popup.label.setText('Please wait while the World is being loaded...')

            self.updatePopup('World Loading....\n\nPlease Wait! This will take a while!')

            start_time = time.time()

            self.world = self.load_world(self.sWorld)

            elapsed_time = time.time() - start_time

            self.updatePopup(' ')
            self.updatePopup('World Loaded in %s seconds!' % str(format(elapsed_time, '.4f')))
            self.updatePopup('')

            self.world_info(self.world)
            self.updatePopup('')
            self.updatePopup('Please close this Window to return to the main UI.')

            self.clearLists()

            sTmp = os.path.basename(str(self.sWorld)).split('.')
            self.sSeed = QtCore.QString(sTmp[0])
            self.sSeed = self.sSeed.right(5)

            if self.sSeed[:1] == "_":
                self.sSeed = self.sSeed.right(4)

            self.iSeed = long(self.sSeed)

            self.enableWorldOptions()

            self.copyMapsTo()

            iCount = self.updateAvail()

            if iCount > 0:
                self.tblAvailable.setEnabled(True)
                self.tblMapList.setEnabled(True)

                self.changeScene('No Image(s) currently selected')
            else:
                self.tblAvailable.setRowCount(0)
                self.tblAvailable.setColumnCount(0)
                self.tblAvailable.setEnabled(False)

                self.changeScene('No Images currently exist for the loaded World')

            self.enableButtons(True)
        else:
            self.enableButtons(False)

            self.showDialog('You have selected an invalid World file!\n\nPlease try again.', 'OK', '', False, 0,
                            ':Images\error.png')

    def clearLists(self):
        self.tblMapList.clear()
        self.tblMapList.setRowCount(0)
        self.tblAvailable.clear()
        self.tblAvailable.setRowCount(0)

    def enableButtons(self, bIn):
        self.actionGrayscale_Heightmap.setEnabled(bIn)
        self.actionScatter_Plot.setEnabled(bIn)
        self.actionSatellite_View.setEnabled(bIn)
        self.actionGenerate_Ancient_World.setEnabled(bIn)
        self.action3D_View.setEnabled(bIn)
        self.actionExport_World.setEnabled(bIn)
        self.btnExport.setEnabled(bIn)

    def updateAvail(self):
        iCount = 0

        self.btnAW.setEnabled(False)
        self.btnGH.setEnabled(False)
        self.btnSM.setEnabled(False)
        self.btnSP.setEnabled(False)

        dst = '%s/Maps/' % self.sDefaultDirectory
        dirs = os.listdir(dst)

        for sFile in dirs:
            if sFile.endswith(self.sFormat):
                if str(self.iSeed) in str(sFile):
                    if 'ancient' not in str(sFile):
                        if 'scatter' not in str(sFile):
                            if 'satellite' not in str(sFile):
                                if 'grayscale' not in str(sFile):
                                    if self.tblMapList.rowCount() > 0:
                                        for x in range(self.tblMapList.rowCount()):
                                            if not str(self.tblMapList.item(x, 0).text()) in str(sFile):
                                                curRowCount = self.tblAvailable.rowCount()
                                                self.tblAvailable.insertRow(curRowCount)
                                                sTmp = sFile.split('_')
                                                sTmp = sTmp[2].split('.')
                                                iTemp = QtGui.QTableWidgetItem(sTmp[0])
                                                self.tblAvailable.setItem(curRowCount, 0, iTemp)

                                                iCount += 1
                                    else:
                                        if 'export' not in str(sFile):
                                            curRowCount = self.tblAvailable.rowCount()
                                            self.tblAvailable.insertRow(curRowCount)
                                            sTmp = sFile.split('_')
                                            sTmp = sTmp[2].split('.')
                                            iTemp = QtGui.QTableWidgetItem(sTmp[0])
                                            self.tblAvailable.setItem(curRowCount, 0, iTemp)

                                            iCount += 1
                                else:
                                    self.btnGH.setEnabled(True)
                            else:
                                self.btnSM.setEnabled(True)
                        else:
                            self.btnSP.setEnabled(True)
                    else:
                        self.btnAW.setEnabled(True)
            elif sFile.endswith(self.sAncFormat):
                if str(self.iSeed) in str(sFile):
                    if 'ancient' in str(sFile):
                        self.btnAW.setEnabled(True)

        return iCount

    def changeScene(self, inTxt):
        self.gvSceneSm = QtGui.QGraphicsScene()
        self.gvSceneLg = QtGui.QGraphicsScene()

        font = QtGui.QFont('Open Sans', 32)
        self.gvSceneSm.addText(inTxt, font)
        self.gvSceneLg.addText(inTxt, font)

        self.gvSmall.setScene(self.gvSceneSm)
        self.gvSmall.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)
        self.gvLarge.setScene(self.gvSceneLg)
        self.gvLarge.setRenderHint(
            QtGui.QPainter.Antialiasing or QtGui.QPainter.SmoothPixmapTransform or QtGui.QPainter.TextAntialiasing)

        bounds = QtCore.QRectF(self.gvSceneSm.itemsBoundingRect())
        self.gvSmall.centerOn(0, 0)
        self.gvSmall.fitInView(bounds, QtCore.Qt.KeepAspectRatio)
        bounds = QtCore.QRectF(self.gvSceneLg.itemsBoundingRect())
        self.gvLarge.centerOn(0, 0)
        # self.gvLarge.fitInView(bounds, QtCore.Qt.KeepAspectRatio)

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
        self.world_info(world)

    def world_info(self, world):
        self.updatePopup(' name               : %s' % world.name)
        self.updatePopup(' width              : %i' % world.width)
        self.updatePopup(' height             : %i' % world.height)
        self.updatePopup(' seed               : %i' % world.seed)
        self.updatePopup(' no plates          : %i' % world.n_plates)
        self.updatePopup(' ocean level        : %f' % world.ocean_level)
        self.updatePopup(' has biome          : %s' % world.has_biome())
        self.updatePopup(' has humidity       : %s' % world.has_humidity())
        self.updatePopup(' has irrigation     : %s' % world.has_irrigation())
        self.updatePopup(' has permeability   : %s' % world.has_permeability())
        self.updatePopup(' has watermap       : %s' % world.has_watermap())
        self.updatePopup(' has lakemap        : %s' % world.has_lakemap())
        self.updatePopup(' has rivermap       : %s' % world.has_rivermap())
        self.updatePopup(' has precipitations : %s' % world.has_precipitations())
        self.updatePopup(' has temperature    : %s' % world.has_temperature())
        self.updatePopup(' has icecap         : %s' % world.has_icecap())
        self.updatePopup(' has wind           : %s' % world.has_wind())

    def onActionSave(self):
        dst = self.sOutputDirectory
        sFile = self.sWorld
        copy(sFile, dst)

        self.updateConfig()

    def updateConfig(self):
        config = configparser2.ConfigParser()
        sFile = '/%s.cfg' % self.iSeed
        sFile = '%s%s' % (self.sDefaultDirectory, sFile)

        tResize = str(self.spnResize.value())

        tSea = self.rdoSeaBrown_3.isChecked()
        tLandCol = self.rdoLandBrown.isChecked()
        tBiomes = self.rdoBiomesYes_3.isChecked()
        tMount = self.rdoMountYes_3.isChecked()
        tRivers = self.rdoRiverYes_3.isChecked()
        tLand = self.rdoLandYes_3.isChecked()
        tData = self.cboAncData.currentIndex()
        tFormat = self.cboAncFormat.currentIndex()

        config['ancient'] = {'spnResize': tResize, 'rdoSea': tSea, 'rdoLandCol': tLandCol,
                             'rdoBiomes': tBiomes, 'rdoMount': tMount,
                             'rdoRivers': tRivers, 'rdoLand': tLand,
                             'cboAncData': tData, 'cboAncFormat': tFormat}

        # These are the World Options - Loading these from CONFIG File
        tSeed = self.spnSeed.value()
        tWidth = self.spnWidth.value()
        tHeight = self.spnHeight.value()
        tPlates = self.spnPlates.value()
        tRecursion = self.spnRecursion.value()
        tFormat = self.cboFormat.currentIndex()
        tData = self.cboData.currentIndex()

        tBW = self.rdoBWYes.isChecked()
        tVM = self.rdoVMYes.isChecked()
        tPB = self.rdoPBYes.isChecked()
        tFade = self.rdoFadeYes.isChecked()

        tSea = self.spnSea.value()
        tTemp1 = self.spnTemp1.value()
        tTemp2 = self.spnTemp2.value()
        tTemp3 = self.spnTemp3.value()
        tTemp4 = self.spnTemp4.value()
        tTemp5 = self.spnTemp5.value()
        tTemp6 = self.spnTemp6.value()
        tPrecip1 = self.spnPrecip1.value()
        tPrecip2 = self.spnPrecip2.value()
        tPrecip3 = self.spnPrecip3.value()
        tPrecip4 = self.spnPrecip4.value()
        tPrecip5 = self.spnPrecip5.value()
        tPrecip6 = self.spnPrecip6.value()
        tPrecip7 = self.spnPrecip7.value()
        tGamma = self.spnGamma.value()
        tOffset = self.spnOffset.value()
        tSeaLevel = self.spnSeaLevel.value()
        tErosionPeriod = self.spnErosionPeriod.value()
        tFoldingRatio = self.spnFoldingRatio.value()
        tAggAbs = self.spnAggAbs.value()
        tAggRel = self.spnAggRel.value()
        tNumCycles = self.spnNumCycles.value()
        tExportWidth = self.spnExportWidth.value()
        tExportHeight = self.spnExportHeight.value()
        tExportNormMin = self.spnExportNormMin.value()
        tExportNormMax = self.spnExportNormMax.value()
        tExportSubStartW = self.spnExportSubStartW.value()
        tExportSubStartH = self.spnExportSubStartH.value()
        tExportSubOffW = self.spnExportSubOffW.value()
        tExportSubOffH = self.spnExportSubOffH.value()
        tExportResample = self.cboExportResample.currentText()

        config['world'] = {'spnSeed': tSeed, 'spnWidth': tWidth, 'spnHeight': tHeight,
                           'spnPlates': tPlates, 'spnRecursion': tRecursion, 'cboFormat': tFormat,
                           'cboData': tData, 'rdoBW': tBW, 'rdoVM': tVM, 'rdoPB': tPB,
                           'rdoFade': tFade, 'spnSea': tSea, 'spnTemp1': tTemp1,
                           'spnTemp2': tTemp2, 'spnTemp3': tTemp3, 'spnTemp4': tTemp4,
                           'spnTemp5': tTemp5, 'spnTemp6': tTemp6, 'spnPrecip1': tPrecip1,
                           'spnPrecip2': tPrecip2, 'spnPrecip3': tPrecip3, 'spnPrecip4': tPrecip4,
                           'spnPrecip5': tPrecip5, 'spnPrecip6': tPrecip6, 'spnPrecip7': tPrecip7,
                           'spnGamma': tGamma, 'spnOffset': tOffset, 'spnSeaLevel': tSeaLevel,
                           'spnErosionPeriod': tErosionPeriod, 'spnFoldingRatio': tFoldingRatio,
                           'spnAggAbs': tAggAbs, 'spnAggRel': tAggRel, 'spnNumCycles': tNumCycles,
                           'spnExportWidth': tExportWidth, 'spnExportHeight': tExportHeight,
                           'spnExportNormMin': tExportNormMin, 'spnExportNormMax': tExportNormMax,
                           'spnExportSubStartW': tExportSubStartW, 'spnExportSubStartH': tExportSubStartH,
                           'spnExportSubOffW': tExportSubOffW, 'spnExportSubOffH': tExportSubOffH,
                           'cboExportResample': tExportResample}

        config['map'] = {'erosion_max_radius': self.erosion_max_radius, 'erosion_maxRadius': self.erosion_maxRadius,
                         'erosion_radius': self.erosion_radius, 'erosion_curve1': self.erosion_curve1,
                         'erosion_curve2': self.erosion_curve2, 'erosion_curve3': self.erosion_curve3,
                         'humidity_precipitation_weight': self.humidity_precipitation_weight,
                         'humidity_irrigation_weight': self.humidity_irrigation_weight,
                         'hydrology_creek': self.hydrology_creek, 'hydrology_river': self.hydrology_river,
                         'hydrology_main_river': self.hydrology_main_river,
                         'icecap_max_freeze_percentage': self.icecap_max_freeze_percentage,
                         'icecap_freeze_chance_window': self.icecap_freeze_chance_window,
                         'icecap_surrounding_tile_influence': self.icecap_surrounding_tile_influence,
                         'irrigation_radius': self.irrigation_radius,
                         'permeability_perm_th_low': self.permeability_perm_th_low,
                         'permeability_perm_th_med': self.permeability_perm_th_med,
                         'permeability_octaves': self.permeability_octaves,
                         'permeability_freq': self.permeability_freq,
                         'precipitation_ths_low': self.precipitation_ths_low,
                         'precipitation_ths_med': self.precipitation_ths_med,
                         'precipitation_octaves': self.precipitation_octaves,
                         'precipitation_freq': self.precipitation_freq,
                         'temperature_distance_to_sun_hwhm': self.temperature_distance_to_sun_hwhm,
                         'temperature_axial_tilt_hwhm': self.temperature_axial_tilt_hwhm,
                         'temperature_octaves': self.temperature_octaves,
                         'temperature_frequency': self.temperature_frequency, 'wind_octaves': self.wind_octaves,
                         'wind_frequency': self.wind_frequency}

        with open(sFile, 'w') as configfile:
            config.write(configfile)

        configfile.close()

    def onActionSaveAllAs(self):
        self.sFormat = self.cboFormat.currentText()

        self.sFormat = self.sFormat[-5:]

        if self.sFormat[:1] == '(':
            self.sFormat = self.sFormat[1:4]
        elif self.sFormat[:1] == ' ':
            self.sFormat = self.sFormat[2:4]
        else:
            self.sFormat = self.sFormat[:4]

        for index in reversed(xrange(self.tblMapList.rowCount())):
            sTmp = self.tblMapList.item(index, 0).text().lower()

            if sTmp == 'biome':
                self.onActionMapsBiome()
            elif sTmp == 'elevation':
                self.onActionMapsElevation()
            elif sTmp == 'humidity':
                self.onActionMapsHumidity()
            elif sTmp == 'icecaps':
                self.onActionMapsIceCaps()
            elif sTmp == 'ocean':
                self.onActionMapsOcean()
            elif sTmp == 'permeability':
                self.onActionMapsPermeability()
            elif sTmp == 'precipitation':
                self.onActionMapsPrecipitation()
            elif sTmp == 'rivers':
                self.onActionMapsRivers()
            elif sTmp == 'temperature':
                self.onActionMapsTemperature()
            elif sTmp == 'wind':
                self.onActionMapsWinds()

        self.sAll = 'all'
        self.copyMapsFrom()

    def onActionPrint(self):
        printerobject = QtGui.QPrinter(0)
        printdialog = QtGui.QPrintDialog(printerobject)

        if printdialog.exec_() == QtGui.QDialog.Accepted:
            pixmapImage = QtGui.QPixmap.grabWidget(self.gvSceneLg)
            painter = QtGui.QPainter(printerobject)
            painter.drawPixmap(0, 0, pixmapImage)
            del painter

    def onActionSaveCurrentView(self):
        import operator

        items = self.gvSceneLg.items()
        totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))

        pixMap = QtGui.QPixmap(totalRect.width(), totalRect.height())

        painter = QtGui.QPainter(pixMap)
        self.gvSceneLg.render(painter, totalRect)
        del painter

        pixMap.save('%s/Maps/Current_View' % self.sDefaultDirectory, 'PNG', -1)

    #        self.imageManipulation(pixMap, totalRect.width(), totalRect.height())
    #        byte_array = QtCore.QByteArray()
    #        tBuffer = QtCore.QBuffer(byte_array)
    #        tBuffer.open(QtCore.QIODevice.WriteOnly)
    #        pixMap.save(tBuffer, 'PNG')
    #        tBuffer.close()

    #        with open('image.json', 'w') as outfile:
    #            json.dumps(byte_array.toBase64(), outfile)
    # TODO: Implement imageManipulation?
    # Test code to see if I can extract Colours from Pixmap (WORKS!!)
    def imageManipulation(self, pTmp, iWidth, iHeight):
        tImage = pTmp.toImage()

        with open('test.csv', 'w') as yourFile:
            for x in range(int(iWidth)):
                for y in range(int(iHeight)):
                    c = tImage.pixel(x, y)
                    colors = QtGui.QColor(c).getRgbF()
                    #                    print '(%s,%s) = %s' % (x, y, colors)
                    yourFile.write('%s,%s,%s,%s,%s,%s,' % (x, y, colors[0], colors[1], colors[2], colors[3]))

        tImage = QtGui.QPixmap()

    def onActionQuit(self):
        self.showDialog('Are you sure you want to Quit?', 'Yes', 'No', True, 2, ':Images\question.png')

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
        visRect = self.gvLarge.mapToScene(vRect).boundingRect()

        x1 = visRect.x()
        x2 = x1 + visRect.width()
        y1 = visRect.y()
        y2 = y1 + visRect.height()

        self.addRedBox(x1, y1, x2, y2)

    def onActionHelp(self):
        os.startfile('.\Help Files\CHM\WorldEngine GUI.chm')

    def onActionAbout(self):
        self.print_version()

    def onActionGenerate(self):
        iTmp1 = 0
        iTmp = self.getValues()

        if iTmp == 0:
            iTmp1 = self.getMapOptions()

        if iTmp == 0 and iTmp1 == 0:
            self.cli_main()
            self.updateConfig()
            self.enableButtons(True)
        elif iTmp == 1:
            self.showDialog('The Precipitation Range is not in ASCENDING Order!\n\nPlease try again.', 'OK', '', False,
                            3, ':Images\error.png')
        elif iTmp == 2:
            self.showDialog('The Temperature Range is not in ASCENDING Order!\n\nPlease try again.', 'OK', '', False, 3,
                            ':Images\error.png')
        elif iTmp1 == 1:
            self.showDialog('The Erosion Curve Values in Map Options MUST be in DESCENDING Order!\n\nPlease try again.',
                            'OK', '', False, 3, ':Images\error.png')
        elif iTmp1 == 2:
            self.showDialog('The Hydrology Values in Map Options MUST be in DESCENDING Order!\n\nPlease try again.',
                            'OK', '', False, 3, ':Images\error.png')
        elif iTmp1 == 3:
            self.showDialog(
                'The Permeability Threshold Values in Map Options MUST be in DESCENDING Order!\n\nPlease try again.',
                'OK', '', False, 3, ':Images\error.png')
        elif iTmp1 == 4:
            self.showDialog(
                'The Precipitation Threshold Values in Map Options MUST be in DESCENDING Order!\n\nPlease try again.',
                'OK', '', False, 3, ':Images\error.png')

    def getMapOptions(self):
        iTmp = 0

        self.erosion_max_radius = self.spnRFRadius.value()
        self.erosion_maxRadius = self.spnRERadius.value()
        self.erosion_radius = self.spnFLERadius.value()
        self.erosion_curve1 = self.spnREC1.value()
        self.erosion_curve2 = self.spnREC2.value()
        self.erosion_curve3 = self.spnREC3.value()

        if self.erosion_curve1 <= self.erosion_curve2 or self.erosion_curve2 <= self.erosion_curve3 or self.erosion_curve1 <= self.erosion_curve3:
            iTmp = 1

        self.humidity_precipitation_weight = self.spnPW.value()
        self.humidity_irrigation_weight = self.spnIW.value()
        # self.hydrology_river_th = self.spin
        self.hydrology_creek = self.spnTHCreek.value()
        self.hydrology_river = self.spnTHRiver.value()
        self.hydrology_main_river = self.spnTHMainRiver.value()

        if self.hydrology_creek <= self.hydrology_river or self.hydrology_river <= self.hydrology_main_river or self.hydrology_creek <= self.hydrology_main_river:
            iTmp = 2

        self.icecap_max_freeze_percentage = self.spnMFP.value()
        self.icecap_freeze_chance_window = self.spnFCW.value()
        self.icecap_surrounding_tile_influence = self.spnSTI.value()
        self.irrigation_radius = self.spnIrrRad.value()
        self.permeability_perm_th_low = self.spnPermTHL.value()
        self.permeability_perm_th_med = self.spnPermTHM.value()
        self.permeability_octaves = self.spnPermOct.value()
        self.permeability_freq = self.spnPermFreq.value()

        if self.permeability_perm_th_low <= self.permeability_perm_th_med:
            iTmp = 3

        self.precipitation_ths_low = self.spnPrecTHL.value()
        self.precipitation_ths_med = self.spnPrecTHM.value()
        self.precipitation_octaves = self.spnPrecOct.value()
        self.precipitation_freq = self.spnPrecFreq.value()

        if self.precipitation_ths_low <= self.precipitation_ths_med:
            iTmp = 4

        self.temperature_distance_to_sun_hwhm = self.spnDistSun.value()
        self.temperature_axial_tilt_hwhm = self.spnAxTilt.value()
        self.temperature_octaves = self.spnTempOct.value()
        self.temperature_frequency = self.spnTempFreq.value()
        self.wind_octaves = self.spnWindOct.value()
        self.wind_frequency = self.spnWindFreq.value()

        return iTmp

    def onActionExportWorld(self):
        self.getValues()

        bError = False

        if self.dExportNormMin >= self.dExportNormMax:
            self.showDialog('Export Normalised Min MUST be less than Export Normalised Max!\n\nPlease try again.',
                            'OK', '', False, 0, ':Images\error.png')
            bError = True
        elif self.dExportSubStartW >= self.dExportWidth:
            self.showDialog('Export Subset Start Width MUST be less than Export Width!\n\nPlease try again.',
                            'OK', '', False, 0, ':Images\error.png')
            bError = True
        elif self.dExportSubStartH >= self.dExportHeight:
            self.showDialog('Export Subset Start Height MUST be less than Export Height!\n\nPlease try again.',
                            'OK', '', False, 0, ':Images\error.png')
            bError = True
        elif self.dExportSubStartW + self.dExportSubOffW > self.dExportWidth:
            self.showDialog('Total Subset Width MUST be less than or equal to Export Width!\n\nPlease try again.',
                            'OK', '', False, 0, ':Images\error.png')
            bError = True
        elif self.dExportSubStartH + self.dExportSubOffH > self.dExportHeight:
            self.showDialog('Total Subset Height MUST be less than or equal to Export Height!\n\nPlease try again.',
                            'OK', '', False, 0, ':Images\error.png')
            bError = True

        if not bError:
            self.popup.show()
            self.popup.textBrowser.setText('')
            self.print_world_info(self.world)
            self.updatePopup('')
            self.updatePopup('Please wait while the World is exported ...')
            self.updatePopup('')
            self.updatePopup('Using:')
            self.updatePopup('  Format:                %s' % self.sFormat)
            self.updatePopup('  Datatype:              %s' % self.sDataType)

#   export_dim - (Width, Height) - Can be 'None' if using WORLD Width & Height
#   export_norm - (Min, Max) - Can be 'None' if no Normalisation required
#   export_subset - (Start_Width, Start_Height, Offset_Width, Offset_Height) - Can be 'None' if exporting entire map
#   export_resample:
#   One of GRA_NearestNeighbour, GRA_Bilinear, GRA_Cubic, GRA_CubicSpline, GRA_Lanczos, GRA_Average, GRA_Mode
#       NB: will be gdal.GRA_CubicSpline etc.

            iWidth = self.spnWidth.value()
            iHeight = self.spnHeight.value()
            export_dim = None
            export_norm = None
            export_subset = None
            iExportW = self.spnExportWidth.value()
            iExportH = self.spnExportHeight.value()

            if iExportW != iWidth or iExportH != iHeight:
                export_dim = (iExportW, iExportH)

            if self.spnExportNormMin.value() != 0:
                if self.spnExportNormMax.value() != iExportW or self.spnExportNormMax.value() != iExportH:
                    export_norm = (self.spnExportNormMin.value(), self.spnExportNormMax.value())

            if self.spnExportSubStartW.value() != 0 or self.spnExportSubStartH.value() != 0:
                if self.spnExportSubOffW.value() != iExportW or self.spnExportSubOffH.value() != iExportH:
                    export_subset = (self.spnExportSubStartW.value(), self.spnExportSubStartH.value(), self.spnExportSubOffW.value(), self.spnExportSubOffH.value())

            export_resample = self.cboExportResample.currentText()

            if export_dim is None:
                self.updatePopup('  Dimensions:            %s  x  %s' % (iWidth, iHeight))
            else:
                self.updatePopup('  Dimensions:            %s  x  %s' % (export_dim[0], export_dim[1]))

            if export_norm is None:
                self.updatePopup('  Normalised Between:    No Normalisation')
            else:
                self.updatePopup('  Normalised Between:    %s and %s' % (export_norm[0], export_norm[1]))

            if export_subset is None:
                self.updatePopup('  Subset - Start:        No Subset')
            else:
                self.updatePopup('  Subset - Start:        %s  x  %s' % (export_subset[0], export_subset[1]))
                self.updatePopup('  Subset - Offset:       %s  x  %s' % (export_subset[2], export_subset[3]))

            self.updatePopup('  Resampling Algorithm:  %s' % export_resample)
            self.updatePopup('  Path:                  %s' % self.sOutputDirectory)

            tempPath = '%s/%s' % (self.sOutputDirectory, self.sWorld)

            export(self.world, self.sFormat, self.sDataType, export_dim, export_norm, export_subset, export_resample, path=tempPath)

            self.updatePopup('')
            self.updatePopup('...all done!')
            self.updatePopup('')
            self.updatePopup('Please close this Window to return to the main UI.')

    # 0 = OK
    # 1 = Precips wrong
    # 2 = Temps wrong
    def getValues(self):
        self.iSeed = self.spnSeed.value()
        self.sWorld = 'seed_%s.world' % self.iSeed
        self.iHeight = self.spnHeight.value()
        self.iWidth = self.spnWidth.value()
        self.iPlates = self.spnPlates.value()
        self.iRecursion = self.spnRecursion.value()
        self.sFormat = self.cboFormat.currentText()
        self.sFormat = self.sFormat[-5:]

        if self.sFormat[:1] == '(':
            self.sFormat = self.sFormat[1:4]
        elif self.sFormat[:1] == ' ':
            self.sFormat = self.sFormat[2:4]
        else:
            self.sFormat = self.sFormat[:4]

        self.sDataType = self.cboData.currentText()
        self.bBW = self.rdoBWYes.isChecked()

        common.set_verbose(self.rdoVMYes.isChecked())

        self.bPB = self.rdoPBYes.isChecked()
        self.bFB = self.rdoFadeYes.isChecked()
        self.dSea = self.spnSea.value()
        self.dTemp1 = self.spnTemp1.value()
        self.dTemp2 = self.spnTemp2.value()
        self.dTemp3 = self.spnTemp3.value()
        self.dTemp4 = self.spnTemp4.value()
        self.dTemp5 = self.spnTemp5.value()
        self.dTemp6 = self.spnTemp6.value()
        self.dPrecip1 = self.spnPrecip1.value()
        self.dPrecip2 = self.spnPrecip2.value()
        self.dPrecip3 = self.spnPrecip3.value()
        self.dPrecip4 = self.spnPrecip4.value()
        self.dPrecip5 = self.spnPrecip5.value()
        self.dPrecip6 = self.spnPrecip6.value()
        self.dPrecip7 = self.spnPrecip7.value()
        self.dGammaVal = self.spnGamma.value()
        self.dGammaOff = self.spnOffset.value()
        self.dSeaLevel = self.spnSeaLevel.value()
        self.dErosionPeriod = self.spnErosionPeriod.value()
        self.dFoldingRatio = self.spnFoldingRatio.value()
        self.dAggAbs = self.spnAggAbs.value()
        self.dAggRel = self.spnAggRel.value()
        self.dNumCycles = self.spnNumCycles.value()
        self.dExportWidth = self.spnExportWidth.value()
        self.dExportHeight = self.spnExportHeight.value()
        self.dExportNormMin = self.spnExportNormMin.value()
        self.dExportNormMax = self.spnExportNormMax.value()
        self.dExportSubStartW = self.spnExportSubStartW.value()
        self.dExportSubStartH = self.spnExportSubStartH.value()
        self.dExportSubOffW = self.spnExportSubOffW.value()
        self.dExportSubOffH = self.spnExportSubOffH.value()
        self.sExportResample = self.cboExportResample.currentText()

        self.dAncResize = self.spnResize.value()
        self.bAncSeaColour = self.rdoSeaBrown_3.isChecked()
        self.bAncLandColour = self.rdoLandBrown.isChecked()
        self.bAncBiomes = self.rdoBiomesYes_3.isChecked()
        self.bAncRivers = self.rdoRiverYes_3.isChecked()
        self.bAncMountains = self.rdoMountYes_3.isChecked()
        self.bAncBorders = self.rdoLandYes_3.isChecked()
        self.sAncFormat = self.cboAncFormat.currentText()

        if self.dTemp1 < self.dTemp2 < self.dTemp3 and self.dTemp4 < self.dTemp5 < self.dTemp6:
            if self.dPrecip1 < self.dPrecip2 < self.dPrecip3 and self.dPrecip4 < self.dPrecip5 < self.dPrecip6 < self.dPrecip7:
                self.sAncFormat = self.sAncFormat[-5:]

                if self.sAncFormat[:1] == '(':
                    self.sAncFormat = self.sAncFormat[1:4]
                elif self.sAncFormat[:1] == ' ':
                    self.sAncFormat = self.sAncFormat[2:4]
                else:
                    self.sAncFormat = self.sAncFormat[:4]

                self.sAncDataType = self.cboAncData.currentText()

                return 0
            else:
                return 1
        else:
            return 2

    def cli_main(self):
        sys.setrecursionlimit(self.iRecursion)
        step = Step.get_by_name('full')

        numpy.random.seed(self.iSeed)

        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('Please wait while the World is being created...')

        self.updatePopup('WorldEngine - a world generator (v. %s)' % VERSION)
        self.updatePopup('------------------------------------------------------------------------------------')
        self.updatePopup(' seed                 : %i' % self.iSeed)
        self.updatePopup(' name                 : %s' % self.sWorld)
        self.updatePopup(' width                : %i' % self.iWidth)
        self.updatePopup(' height               : %i' % self.iHeight)
        self.updatePopup(' number of plates     : %i' % self.iPlates)
        self.updatePopup(' world format         : %s' % self.sFormat)
        self.updatePopup(' world data type      : %s' % self.sDataType)
        self.updatePopup(' black and white maps : %s' % self.bBW)
        self.updatePopup(' fade borders         : %s' % self.bFB)
        self.updatePopup(
            ' temperature ranges   : %s' % [self.dTemp1, self.dTemp2, self.dTemp3, self.dTemp4, self.dTemp5,
                                            self.dTemp6])
        self.updatePopup(
            ' humidity ranges      : %s' % [self.dPrecip1, self.dPrecip2, self.dPrecip3, self.dPrecip4, self.dPrecip5,
                                            self.dPrecip6, self.dPrecip7])
        self.updatePopup(' gamma value          : %s' % self.dGammaVal)
        self.updatePopup(' gamma offset         : %s' % self.dGammaOff)

        self.updatePopup('')  # empty line
        self.updatePopup('starting ... ')
        self.updatePopup('NB: This could take a long time (10+ minutes) and the UI will become unresponsive.')
        self.updatePopup('    For example, on a Core i7-4700MQ @ 2.4GHz, Plates Simulation takes more than')
        self.updatePopup('    a minute, Ocean Initialisation about 4 minutes and the Watermap Simulation')
        self.updatePopup('    about 3 minutes. So, approximately 8 minutes for these three parts alone!')

        self.generateWorld(step)

        self.updatePopup('')  # empty line
        self.updatePopup('Producing Output ...')

        self.sFormat = self.cboFormat.currentText()
        self.sFormat = self.sFormat[-5:]

        if self.sFormat[:1] == '(':
            self.sFormat = self.sFormat[1:4]
        elif self.sFormat[:1] == ' ':
            self.sFormat = self.sFormat[2:4]
        else:
            self.sFormat = self.sFormat[:4]

        if self.sFormat != 'png' and self.sFormat != 'jpeg' and self.sFormat != 'jpg' and self.sFormat != 'bmp':
            self.bPNG = True

        self.onActionMapsBiome()
        self.updatePopup('    Generated Biome Map')
        self.onActionMapsElevation()
        self.updatePopup('    Generated Elevation Map')
        self.updatePopup('    Generated Plates Map')
        self.onActionMapsGrayscale()
        self.updatePopup('    Generated Grayscale Heightmap')
        self.updatePopup('    Generated Normal Map')
        self.onActionMapsHumidity()
        self.updatePopup('    Generated Humidity Map')
        self.onActionMapsIceCaps()
        self.updatePopup('    Generated Icecap Map')
        self.onActionMapsOcean()
        self.updatePopup('    Generated Ocean Map')
        self.onActionMapsPermeability()
        self.updatePopup('    Generated Permeability Map')
        self.onActionMapsPrecipitation()
        self.updatePopup('    Generated Precipitation Map')
        self.onActionMapsRivers()
        self.updatePopup('    Generated River Map')
        self.onActionMapsTemperature()
        self.updatePopup('    Generated Temperature Map')
        self.onActionMapsWinds()
        self.updatePopup('    Generated Wind Map')
        self.onActionMapsSatellite()
        self.updatePopup('    Generated Satellite Map')
        self.onActionMapsScatter()
        self.updatePopup('    Generated Scatter Plot')
        self.updatePopup('')
        self.updatePopup('All Done!')
        self.updatePopup('')
        self.updatePopup('Please close this Window to return to the main UI.')

        self.clearLists()

        iCount = self.updateAvail()

        self.tblAvailable.setEnabled(True)
        self.tblMapList.setEnabled(True)

        self.changeScene('No Image(s) currently selected')

        self.spnResize.setEnabled(True)
        self.grpSea.setEnabled(True)
        self.grpLand.setEnabled(True)
        self.grpBiomes.setEnabled(True)
        self.grpMountains.setEnabled(True)
        self.grpRivers.setEnabled(True)
        self.grpBorder.setEnabled(True)
        self.grpVerbose_2.setEnabled(True)
        self.cboAncData.setEnabled(True)
        self.cboAncFormat.setEnabled(True)
        self.btnGenWorld_3.setEnabled(True)

        self.sAll = 'all'
        self.copyMapsFrom()
        self.bPNG = False

    def copyMapsTo(self):
        if not self.sOutputDirectory:
            sTmp = '.'
        else:
            sTmp = str(self.sOutputDirectory)

        dst = '%s/Maps/' % self.sDefaultDirectory

        dirs = os.listdir(sTmp)

        for sFile in dirs:
            if sFile.endswith('.png') or sFile.endswith('.bmp') or sFile.endswith('.jpg') or sFile.endswith('.jpeg'):
                sTmpFile = '%s/%s' % (sTmp, sFile)
                copy(sTmpFile, dst)

    def copyMapsFrom(self):
        if self.sOutputDirectory != self.sDefaultDirectory:
            if not self.sOutputDirectory:
                sTmp = '.'
            else:
                sTmp = str(self.sOutputDirectory)

            dst = '%s/Maps/' % self.sDefaultDirectory

            dirs = os.listdir(dst)

            if self.sAll == 'all':
                for sFile in dirs:
                    if sFile.endswith('.png') or sFile.endswith('.bmp') or sFile.endswith('.jpg') or sFile.endswith('.jpeg'):
                        sTmpFile = '%s/%s' % (dst, sFile)
                        copy(sTmpFile, sTmp)

                dirs = os.listdir(self.sDefaultDirectory)

                for sFile in dirs:
                    if sFile.endswith('.world'):
                        copy(sFile, sTmp)
            elif self.sAll == 'world':
                dirs = os.listdir(self.sDefaultDirectory)

                for sFile in dirs:
                    if sFile.endswith('%s.world' % self.sSeed):
                        copy(sFile, sTmp)
            elif self.sAll == 'ancient':
                for sFile in dirs:
                    if sFile.endswith('%s_ancient_world.png' % self.sSeed) or sFile.endswith('%s_ancient_world.bmp' % self.sSeed)\
                            or sFile.endswith('%s_ancient_world.jpg' % self.sSeed) or sFile.endswith('%s_ancient_world.jpeg' % self.sSeed):
                        sTmpFile = '%s/%s' % (dst, sFile)
                        copy(sTmpFile, sTmp)
            else:
                for sFile in dirs:
                    if sFile.endswith('%s.png' % self.sSeed) or sFile.endswith('%s.bmp' % self.sSeed)\
                            or sFile.endswith('%s.jpg' % self.sSeed) or sFile.endswith('%s.jpeg' % self.sSeed):
                        sTmpFile = '%s/%s' % (dst, sFile)
                        copy(sTmpFile, sTmp)

            if not sTmp == '.':
                self.deleteMaps('maps')

                if self.sAll == 'all' or self.sAll == 'world':
                    self.deleteMaps('world')

    def deleteMaps(self, sTmp):
        #        sTmp = os.path.dirname(str(self.sWorld))
        dst = '%s/Maps/' % self.sDefaultDirectory
        dirs = os.listdir(dst)

        for sFile in dirs:
            if sFile.endswith('.png') or sFile.endswith('.bmp') or sFile.endswith('.jpg') or sFile.endswith('.jpeg'):
                os.remove(os.path.join(dst, sFile))

        if sTmp == 'world':
            dst = self.sDefaultDirectory
            dirs = os.listdir(dst)

            for sFile in dirs:
                if sFile.endswith('.world'):
                    os.remove(os.path.join(dst, sFile))

    def generateWorld(self, step):
        self.world = world_gen(self, self.sWorld, self.iWidth, self.iHeight, self.iSeed,
                               [self.dTemp1, self.dTemp2, self.dTemp3, self.dTemp4, self.dTemp5, self.dTemp6],
                               [self.dPrecip1, self.dPrecip2, self.dPrecip3, self.dPrecip4, self.dPrecip5,
                                self.dPrecip6, self.dPrecip7],
                               self.iPlates, self.dSea, step, self.dGammaVal, self.dGammaOff, self.bFB,
                               self.dSeaLevel,
                               self.dErosionPeriod, self.dFoldingRatio, self.dAggAbs, self.dAggRel, self.dNumCycles,
                               self.erosion_curve1, self.erosion_curve2, self.erosion_curve3, self.erosion_max_radius,
                               self.erosion_maxRadius,
                               self.erosion_radius, self.humidity_irrigation_weight, self.humidity_precipitation_weight,
                               self.hydrology_creek, self.hydrology_main_river, self.hydrology_river,
                               self.irrigation_radius,
                               self.icecap_freeze_chance_window, self.icecap_max_freeze_percentage,
                               self.icecap_surrounding_tile_influence,
                               self.permeability_freq, self.permeability_octaves, self.permeability_perm_th_low,
                               self.permeability_perm_th_med,
                               self.precipitation_freq, self.precipitation_octaves, self.precipitation_ths_low,
                               self.precipitation_ths_med,
                               self.temperature_axial_tilt_hwhm, self.temperature_distance_to_sun_hwhm,
                               self.temperature_frequency, self.temperature_octaves,
                               self.wind_frequency, self.wind_octaves)

        filename = '%s' % self.sWorld

        if self.bPB:
            with open(filename, "wb") as f:
                f.write(self.world.protobuf_serialize())
        else:
            save_world_to_hdf5(self.world, filename)

        self.updatePopup(' ')
        self.updatePopup("* world data saved in '%s'" % filename)

        self.sAll = 'world'
        self.copyMapsFrom()

    def onActionMapsAll(self):
        self.sFormat = self.cboFormat.currentText()

        self.sFormat = self.sFormat[-5:]

        if self.sFormat[:1] == '(':
            self.sFormat = self.sFormat[1:4]
        elif self.sFormat[:1] == ' ':
            self.sFormat = self.sFormat[2:4]
        else:
            self.sFormat = self.sFormat[:4]

        if self.sFormat != 'png' and self.sFormat != 'jpeg' and self.sFormat != 'jpg' and self.sFormat != 'bmp':
            self.bPNG = True

        self.sAll = 'map'

        self.onActionMapsBiome()
        self.onActionMapsElevation()
        self.onActionMapsGrayscale()
        self.onActionMapsHumidity()
        self.onActionMapsIceCaps()
        self.onActionMapsOcean()
        self.onActionMapsPermeability()
        self.onActionMapsPrecipitation()
        self.onActionMapsRivers()
        self.onActionMapsSatellite()
        self.onActionMapsScatter()
        self.onActionMapsTemperature()
        self.onActionMapsWinds()

        self.copyMapsFrom()
        self.bPNG = False

    def onActionMapsBiome(self):
        if self.sFormat == '':
            self.sFormat = 'png'
            self.bPNG = False

        filename = '%s/Maps/seed_%s_biome.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        draw_biome_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_biome.png" % (self.sDefaultDirectory, self.iSeed)
            draw_biome_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionMapsElevation(self):
        filename = '%s/Maps/seed_%s_elevation.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        sea_level = self.world.sea_level()
        draw_simple_elevation_on_file(self.world, filename, sea_level=sea_level)
        filename = '%s/Maps/seed_%s_plates.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        draw_plates_on_file(self.world, filename, self.bBW)

        if self.sFormat != 'png':
            filename = "%s/Maps/seed_%s_elevation.png" % (self.sDefaultDirectory, self.iSeed)
            draw_simple_elevation_on_file(self.world, filename, sea_level)
            filename = '%s/Maps/seed_%s_plates.png' % (self.sDefaultDirectory, self.iSeed)
            draw_plates_on_file(self.world, filename, self.bBW)

        iCount = self.updateAvail()

    def onActionMapsGrayscale1(self):
        self.onActionMapsGrayscale()
        self.btnHeightmap_Clicked()

    def onActionMapsGrayscale(self):
        filename = '%s/Maps/seed_%s_grayscale.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        draw_grayscale_heightmap_on_file(self.world, filename)

        if self.sFormat != 'png':
            filename = "%s/Maps/seed_%s_grayscale.png" % (self.sDefaultDirectory, self.iSeed)
            draw_grayscale_heightmap_on_file(self.world, filename)

        bumpFilename = '%s/Maps/seed_%s_normal.png' % (self.sDefaultDirectory, self.iSeed)

        if self.rdoVMYes.isChecked():
            tRes = readHeight2Bump(filename, bumpFilename, options='tqv')
        else:
            tRes = readHeight2Bump(filename, bumpFilename, options='tq')

        self.btnGH.setEnabled(True)

    def onActionMapsHumidity(self):
        filename = '%s/Maps/seed_%s_humidity.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_humidity.png' % (self.sDefaultDirectory, self.iSeed)
        draw_humidity_on_file(self.world, filename, self.bBW)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_humidity.png" % (self.sDefaultDirectory, self.iSeed)
            draw_humidity_on_file(self.world, filename, self.bBW)

        iCount = self.updateAvail()

    def onActionMapsIceCaps(self):
        filename = '%s/Maps/seed_%s_icecaps.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_icecaps.png' % (self.sDefaultDirectory, self.iSeed)
        draw_icecaps_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_icecaps.png" % (self.sDefaultDirectory, self.iSeed)
            draw_icecaps_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionMapsOcean(self):
        filename = '%s/Maps/seed_%s_ocean.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_ocean.png' % (self.sDefaultDirectory, self.iSeed)
        draw_ocean_on_file(self.world.layers['ocean'].data, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_ocean.png" % (self.sDefaultDirectory, self.iSeed)
            draw_ocean_on_file(self.world.layers['ocean'].data, filename)

        iCount = self.updateAvail()

    def onActionMapsPermeability(self):
        filename = '%s/Maps/seed_%s_permeability.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_permeability.png' % (self.sDefaultDirectory, self.iSeed)
        draw_permeability_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_permeability.png" % (self.sDefaultDirectory, self.iSeed)
            draw_permeability_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionMapsPrecipitation(self):
        filename = '%s/Maps/seed_%s_precipitation.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_precipitation.png' % (self.sDefaultDirectory, self.iSeed)
        draw_precipitation_on_file(self.world, filename, self.bBW)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_precipitation.png" % (self.sDefaultDirectory, self.iSeed)
            draw_precipitation_on_file(self.world, filename, self.bBW)

        iCount = self.updateAvail()

    def onActionMapsRivers(self):
        filename = '%s/Maps/seed_%s_rivers.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_rivers.png' % (self.sDefaultDirectory, self.iSeed)
        draw_riversmap_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_rivers.png" % (self.sDefaultDirectory, self.iSeed)
            draw_riversmap_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionMapsScatter1(self):
        self.onActionMapsScatter()
        self.btnScatter_Clicked()

    def onActionMapsScatter(self):
        filename = '%s/Maps/seed_%s_scatter.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_scatter.png' % (self.sDefaultDirectory, self.iSeed)
        draw_scatter_plot_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_scatter.png" % (self.sDefaultDirectory, self.iSeed)
            draw_scatter_plot_on_file(self.world, filename)

        self.btnSP.setEnabled(True)

    def onActionMapsSatellite1(self):
        self.onActionMapsSatellite()
        self.btnSatellite_Clicked()

    def onActionMapsSatellite(self):
        filename = '%s/Maps/seed_%s_satellite.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_satellite.png' % (self.sDefaultDirectory, self.iSeed)
        draw_satellite_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_satellite.png" % (self.sDefaultDirectory, self.iSeed)
            draw_satellite_on_file(self.world, filename)

        self.btnSM.setEnabled(True)

    def onActionMapsTemperature(self):
        filename = '%s/Maps/seed_%s_temperature.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_temperature.png' % (self.sDefaultDirectory, self.iSeed)
        draw_temperature_levels_on_file(self.world, filename, self.bBW)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_temperature.png" % (self.sDefaultDirectory, self.iSeed)
            draw_temperature_levels_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionMapsWinds(self):
        filename = '%s/Maps/seed_%s_wind.%s' % (self.sDefaultDirectory, self.iSeed, self.sFormat)
        # filename = '%s/Maps/seed_%s_wind.png' % (self.sDefaultDirectory, self.iSeed)
        draw_wind_on_file(self.world, filename)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_wind.png" % (self.sDefaultDirectory, self.iSeed)
            draw_wind_on_file(self.world, filename)

        iCount = self.updateAvail()

    def onActionAncient(self):
        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('Please wait while the Ancient Map is being created...')
        self.updatePopup('')  # empty line
        self.updatePopup('Generating Ancient Map...')
        self.updatePopup('')  # empty line

        resizeFactor = self.spnResize.value()
        self.updatePopup(' resize factor          : %s' % resizeFactor)

        if self.rdoSeaBrown_3.isChecked():
            seaColour = (212, 198, 169, 255)
            self.updatePopup(' sea colour             : brown')
        else:
            seaColour = (142, 162, 179, 255)
            self.updatePopup(' sea colour             : blue')

        if self.rdoLandBrown.isChecked():
            landColour = (181, 166, 127, 255)
            self.updatePopup(' land colour            : brown')
        else:
            landColour = (127, 181, 139, 255)
            self.updatePopup(' land colour            : green')

        if self.rdoBiomesYes_3.isChecked():
            self.updatePopup(' draw biomes            : yes')
        else:
            self.updatePopup(' draw biomes            : no')

        if self.rdoRiverYes_3.isChecked():
            self.updatePopup(' draw rivers            : yes')
        else:
            self.updatePopup(' draw rivers            : no')

        if self.rdoMountYes_3.isChecked():
            self.updatePopup(' draw mountains         : yes')
        else:
            self.updatePopup(' draw mountains         : no')

        if self.rdoLandYes_3.isChecked():
            self.updatePopup(' draw land outer border : yes')
        else:
            self.updatePopup(' draw land outer border : no')

        if self.rdoVerboseYes.isChecked():
            self.updatePopup(' verbose messages       : yes')
        else:
            self.updatePopup(' verbose messages       : no')

        self.updatePopup('')  # empty line
        self.updatePopup('starting (this will take a few minutes and the UI will become unresponsive) ...')

        self.sAncFormat = self.cboAncFormat.currentText()
        self.sAncFormat = self.sAncFormat[-5:]

        if self.sAncFormat[:1] == '(':
            self.sAncFormat = self.sAncFormat[1:4]
        elif self.sAncFormat[:1] == ' ':
            self.sAncFormat = self.sAncFormat[2:4]
        else:
            self.sAncFormat = self.sAncFormat[:4]

        self.bPNG = False

        if self.sAncFormat != 'png' and self.sAncFormat != 'jpeg' and self.sAncFormat != 'jpg' and self.sAncFormat != 'bmp':
            self.bPNG = True

        filename = '%s/Maps/seed_%s_ancient_world.%s' % (self.sDefaultDirectory, self.iSeed, self.sAncFormat)
        # filename = '%s/Maps/seed_%s_ancient_world.png' % (self.sDefaultDirectory, self.iSeed)

        drawBiome = self.rdoBiomesYes_3.isChecked()
        drawRivers = self.rdoRiverYes_3.isChecked()
        drawMountains = self.rdoMountYes_3.isChecked()
        drawOuterLandBorder = self.rdoLandYes_3.isChecked()
        ancVerbose = self.rdoVerboseYes.isChecked()

        draw_ancientmap_on_file(self, self.world, filename, resizeFactor, seaColour, landColour, drawBiome, drawRivers,
                                drawMountains, drawOuterLandBorder, ancVerbose)

        generated_file = "seed_%s_ancient_world.%s" % (self.iSeed, self.sAncFormat)

        if self.bPNG:
            filename = "%s/Maps/seed_%s_ancient_world.png" % (self.sDefaultDirectory, self.iSeed)
            draw_ancientmap_on_file(self, self.world, filename, resizeFactor, seaColour, landColour, drawBiome,
                                    drawRivers, drawMountains, drawOuterLandBorder, ancVerbose)

        self.updatePopup('')
        self.updatePopup("ancient map %s generated" % generated_file)

        self.updatePopup('')
        self.updatePopup('...all done!')
        self.updatePopup('')
        self.updatePopup('Please close this Window to return to the main UI.')

        self.sAll = 'ancient'

        self.copyMapsFrom()
        self.bPNG = False

        self.btnAW.setEnabled(True)
        self.btnAncient_Clicked()

    def onAction3DView(self):
        minHght = self.world.layers['elevation'].data.min()  # = -0.61182 in example
        maxHght = self.world.layers['elevation'].data.max()  # = 31.15302 in example

        diff = maxHght - minHght
        multHght = diff / 255.0

        hm = '%s/Maps/seed_%s_grayscale.png' % (self.sDefaultDirectory, self.iSeed)
        tm = '%s/Maps/seed_%s_elevation.png' % (self.sDefaultDirectory, self.iSeed)
        bm = '%s/Maps/seed_%s_normal.png' % (self.sDefaultDirectory, self.iSeed)

        # pi_3d(hm, self.world.width, self.world.height, multHght, tm, bm)
        world3dA(hm, self.world.width, self.world.height, multHght, tm, bm)

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
                raise Exception('Unable to load the worldfile as protobuf file')
        else:
            raise Exception('The given worldfile does not seem to be a protobuf file')

    def onActionSetOutputDirectory(self):
        self.sOutputDirectory = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory', '.', QtGui.QFileDialog.DontUseNativeDialog)

        if not self.sOutputDirectory:
            self.sOutputDirectory, _ = os.path.split(sys.argv[0])

    def print_version(self):
        self.popup.show()
        self.popup.textBrowser.setText('')
        self.popup.label.setText('WorldEngine Version Information')

        self.updatePopup('------------------------------------------------------------------------------------')
        self.updatePopup('')
        self.updatePopup(' WorldEngine - a world generator (v. %s)' % VERSION)
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' WorldEngine itself is (c) Federico Tomassetti and Bret Curtis, 2011-2016')
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' This WorldEngine GUI is (c) SpinalSoft (AU) 2016-2017')
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' Pi3D is (c) Tim Skillman, Paddy Gaunt, Tom Ritchford  2012 - 2017')
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' Icons are from "cc mono icon set" by Gentleface.com:')
        self.updatePopup(' https://www.iconfinder.com/iconsets/cc_mono_icon_set')
        self.updatePopup('')
        self.updatePopup(' except 3D & WINDOW which are attributable as follows:')
        self.updatePopup(' "Icon made by Freepik from www.flaticon.com"')
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' Stylesheet is a modified version of "Qt Dark Orange" from')
        self.updatePopup(' http://tech-artists.org/forum/showthread.php?2359-Release-Qt-dark-orange-stylesheet')
        self.updatePopup(' by LoneWolf')
        self.updatePopup('')
        self.updatePopup('')
        self.updatePopup(' Please close this Window to return to the main UI')
        self.updatePopup('')
        self.updatePopup('------------------------------------------------------------------------------------')

    # 0 = No Action, 1 = New, 2 = Quit, 3 = not in Ascending Order
    def btnCentre_Clicked(self):
        self.dialog.close()

        if self.iMsg == 1:
            self.setDefaults()
        elif self.iMsg == 2:
            self.deleteMaps('maps')
            self.deleteMaps('world')
            sys.exit(APP.exec_())
        elif self.iMsg == 3:
            self.toolBox.setCurrentIndex(3)
            self.tabWidget.setCurrentIndex(1)

    def btnRight_Clicked(self):
        self.dialog.close()
        self.iMsg = 0

    @pyqtSlot('QString')
    def updatePopup(self, sText):
        self.popup.textBrowser.append(sText)
        APP.processEvents()

    def onActionWindows(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('windows')

    def onActionWindowsXP(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('windowsxp')

    def onActionWindowsVista(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('windowsvista')

    def onActionMotif(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('motif')

    def onActionCDE(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('cde')

    def onActionPlastique(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('plastique')

    def onActionCleanLooks(self):
        if self.sshFile != '':
            self.setBlankStylesheet()
            self.sshFile = ''

        APP.setStyle('cleanlooks')

    def setBlankStylesheet(self):
        self.sshFile = 'blank.stylesheet'

        with open(self.sshFile, "r") as fh:
            self.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self.dialog.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self.popup.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self._3d.setStyleSheet(fh.read())

    def onActionDarkOrange(self):
        self.sshFile = 'darkorange.stylesheet'

        with open(self.sshFile, "r") as fh:
            self.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self.dialog.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self.popup.setStyleSheet(fh.read())
        with open(self.sshFile, "r") as fh:
            self._3d.setStyleSheet(fh.read())

if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    FORM = MyApp()
    APP.setWindowIcon(QtGui.QIcon(':/Images/icon.png'))
    APP.setStyle('plastique')
    FORM.show()
    APP.exec_()
