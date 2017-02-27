#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

#This code is based on 3dWorld.py from the Book TBA

from math import sin, cos, radians
import pi3d
from pygame.constants import K_ESCAPE

def limit(value, inMin, inMax):
    if value < inMin:
        value = inMin
    elif value > inMax:
        value = inMax
    
    return value

def world3dA(inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap):
    DISPLAY = pi3d.Display.create(x = 50, y = 50)
#    inputs = pi3d.InputEvents()
    CAMERA = pi3d.Camera.instance()
    tex = pi3d.Texture("textures/grass.jpg")
    flatsh = pi3d.Shader("uv_flat")
    mapwidth = inWidth
    mapdepth = inDepth
    mapheight = inHeight
    
    # inHeightmap = Maps/seed_XXXXX_grayscale.png
    # inTextureMap = Maps/seed_XXXXX_elevation.png
    mymap = pi3d.ElevationMap(inHeightmap, width = mapwidth, depth = mapdepth, height = mapheight, divx = 199, divy = 199, ntiles=20, name = "sub")
    mymap.set_draw_details(flatsh, [tex], 1.0, 1.0)
    rot = 0.0
    tilt = 0.0
    height = 20.0
    viewHeight = 4
    sky = 200
    xm, ym, zm = 0.0, height, 0.0
    onGround = False
 
    mykeys = pi3d.Keyboard()
    mymouse = pi3d.Mouse(restrict = False)
    mymouse.start()
    
    omx, omy = mymouse.position()

    while DISPLAY.loop_running():
#    while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
#        inputs.do_input_events()
        # movement of camera
#        mx, my, mv, mh, md = inputs.get_mouse_movement()
        mx, my = mymouse.position()
        
        rot -= (mx - omx) * 0.2
        tilt -= (my - omy) * 0.2

        omx = mx
        omy = my

        CAMERA.reset()
        CAMERA.rotate(-tilt, rot, 0)
        CAMERA.position((xm, ym, zm))
    
        mymap.draw()

        k = mykeys.read()

        if k > -1:
            if k == 48: # ESCAPE key - '0' Key
                DISPLAY.destroy()
                mykeys.close()
                mymouse.stop()
                break
            elif k == 87 or k == 119:
#        if inputs.key_state("KEY_W"):
                xm -= sin(radians(rot))
                zm += cos(radians(rot))
            elif k == 83 or k == 115:
#        elif inputs.key_state("KEY_S"):
                xm += sin(radians(rot))
                zm -= cos(radians(rot))
            elif k == 82 or k == 114:
#        elif inputs.key_state("KEY_R"):
                ym += 2
                onGround = False
            elif k == 84 or k == 116:
#        elif inputs.key_state("KEY_T"):
                ym -= 2
        
        ym -= 0.1
        
        xm = limit(xm, -(mapwidth / 2), (mapwidth / 2))
        zm = limit(zm, -(mapdepth / 2), (mapdepth / 2))
        
        if ym >= sky:
            ym = sky
        
        ground = mymap.calcHeight(xm, zm) + viewHeight
        
        if (onGround == True) or (ym <= ground):
            ym = mymap.calcHeight(xm, zm) + viewHeight
            onGround = True
#    else:
#        inputs.release()
#        DISPLAY.destroy()