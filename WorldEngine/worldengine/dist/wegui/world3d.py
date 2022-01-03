#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

# This code is based on '3dWorld.py' from the Book 'Raspberry Pi Cookbook for Python Programmers' by Tim Cox
# (ISBN-13: 978-1849696623)
# modified by Shando and Paddy from http://groups.google.com/forum/#!forum/pi3d

from math import sin, cos, radians
import pi3d
from PIL import Image
import numpy as np

def limit(value, inMin, inMax):
    if value < inMin:
        value = inMin
    elif value > inMax:
        value = inMax
    return value

class World3dA:
    def __init__(self, inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap, inSeaLevel):
        self.DISPLAY = pi3d.Display.create(0, 0, 1280, 1024)
        self.CAMERA = pi3d.Camera.instance()
        self.grass_tex = pi3d.Texture('textures/grasstile_n.jpg')
        self.w_norm = pi3d.Texture('textures/n_norm000.png')
        self.shader = pi3d.Shader("uv_bump")
        self.rshader = pi3d.Shader("uv_reflect")
        self.viewHeight = 4
        self.sky = 200
        self.keep_looping = False
        
    def startWorld(self, inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap, inSeaLevel):
        self.mykeys = pi3d.Keyboard()
        self.mymouse = pi3d.Mouse(restrict=False)
        self.mymouse.start()

        self.create_world(inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap, inSeaLevel)
        self.keep_looping = True
        
        self.xm -= sin(radians(self.rot))
        self.zm += cos(radians(self.rot))
        self.ym -= 0.1
        self.xm = limit(self.xm, -(self.mapwidth / 2), (self.mapwidth / 2))
        self.zm = limit(self.zm, -(self.mapdepth / 2), (self.mapdepth / 2))

        if self.ym >= self.sky:
            self.ym = self.sky

        self.ground = self.mymap.calcHeight(self.xm, self.zm) + self.viewHeight

        if self.onGround or (self.ym <= self.ground):
            self.ym = self.mymap.calcHeight(self.xm, self.zm) + self.viewHeight
            self.onGround = True

    def create_world(self, inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap, inSeaLevel):
        base_tex = np.array(Image.open(inTextureMap))
        base_gr = base_tex.copy()
        ix = np.where(base_gr[:,:,2] > 20)  # i.e. was blue
        base_gr[ix[0], ix[1], 1] += 50  # increase green
        base_gr[ix[0], ix[1], 2] = 0  # reduce blue
        texg = pi3d.Texture(base_gr)
        base_bl = base_tex.copy()
        base_bl[:,:] = [0, 0, 60, 170]  # uniform slightly transparent
        texb = pi3d.Texture(base_bl)
        self.mapwidth = inWidth
        self.mapdepth = inDepth
        self.mapheight = inHeight

        self.mymap = pi3d.ElevationMap(inBumpMap, width=self.mapwidth, depth=self.mapdepth, height=self.mapheight, divx=199, divy=199,
                                  ntiles=1, name="sub")
        self.mymap.set_draw_details(self.shader, [texg, self.grass_tex], 200.0)
        self.wmap = pi3d.ElevationMap(inBumpMap, width=self.mapwidth, depth=self.mapdepth, height=self.mapheight * 0.1, divx=199, divy=199,
                                 ntiles=1, name="water", y=inSeaLevel)
        self.wmap.set_draw_details(self.rshader, [texb, self.w_norm, texg], 50.0, 0.2)

        self.rot = 0.0
        self.tilt = 0.0
        self.height = 20.0
        self.xm, self.ym, self.zm = 0.0, self.height, 0.0
        self.onGround = False
        self.omx, self.omy = self.mymouse.position()

    def loop_running(self):
        if self.keep_looping and self.DISPLAY.loop_running():
            mx, my = self.mymouse.position()
            self.rot -= (mx - self.omx) * 0.2
            self.tilt -= (my - self.omy) * 0.2
            self.omx = mx
            self.omy = my

            self.CAMERA.reset()
            self.CAMERA.rotate(-self.tilt, self.rot, 0)
            self.CAMERA.position((self.xm, self.ym, self.zm))

            self.mymap.draw()
            self.wmap.draw()
            return True
        else:
            return False

    def stop_looping(self):
        self.keep_looping = False
        self.mykeys.close()
        self.mymouse.stop()

    def close(self):
        self.DISPLAY.destroy()

    def read_key_and_move(self):
        k = self.mykeys.read()

        if k > -1:
            if k == 48:  # ESCAPE key - '0' Key
                return k # return early and do scene change or stop
            elif k == 87 or k == 119:  # FORWARDS key - 'W' Key
                self.xm -= sin(radians(self.rot))
                self.zm += cos(radians(self.rot))
            elif k == 83 or k == 115:  # BACKWARDS key - 'S' Key
                self.xm += sin(radians(self.rot))
                self.zm -= cos(radians(self.rot))
            elif k == 82 or k == 114:  # UPWARDS key - 'R' Key
                self.ym += 2
                self.onGround = False
            elif k == 84 or k == 116:  # DOWNWARDS key - 'T' Key
                self.ym -= 2
            # only do this if a move key was pressed?
            self.ym -= 0.1
            self.xm = limit(self.xm, -(self.mapwidth / 2), (self.mapwidth / 2))
            self.zm = limit(self.zm, -(self.mapdepth / 2), (self.mapdepth / 2))

            if self.ym >= self.sky:
                self.ym = self.sky

            self.ground = self.mymap.calcHeight(self.xm, self.zm) + self.viewHeight

            if self.onGround or (self.ym <= self.ground):
                self.ym = self.mymap.calcHeight(self.xm, self.zm) + self.viewHeight
                self.onGround = True
        return None
