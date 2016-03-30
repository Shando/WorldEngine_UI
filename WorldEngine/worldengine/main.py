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
        
        grview = 
        grview.setViewport(QtOpenGL.QGLWidget())
        scene = QtGui.QGraphicsScene()
        tPix = QtGui.QPixmap('seed_11111_elevation.png')
        scene.addPixmap(tPix)
        grview.setScene(scene)
        grview.show()
        
    def btnRiver_Clicked(self):
        from random import randint

        
if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    FORM = MyApp()
    FORM.show()
    APP.exec_()
