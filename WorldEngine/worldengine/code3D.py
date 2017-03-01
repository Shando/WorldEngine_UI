#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

# This code is based on Amazing.py from the Pi3D Demo Library

import math
import pi3d


def pi_3d(inHeightmap, inWidth, inDepth, inHeight, inTextureMap, inBumpMap):
    rads = 0.017453292512  # degrees to radians

    # helpful messages
    # Esc to quit, W to go forward, Mouse to steer
    # At the edge you will turn into a ghost and be able to fly and pass through rocks!

    # Setup display and initialise pi3d
    DISPLAY = pi3d.Display.create(x=100, y=100, background=(0.4, 0.8, 0.8, 1), use_pygame=True)

    shader = pi3d.Shader("uv_bump")
    flatsh = pi3d.Shader("uv_flat")
    light = pi3d.Light((1, 1, 1), (400.0, 400.0, 350.0), (0.03, 0.03, 0.05), True)
    # sun = pi3d.Light((0.0, 1000.0, 0.0), (0.5, 1.0, 0.7), (0.3, 0.1, 0.1), is_point=True)
    
    # load Textures
    rockimg1 = pi3d.Texture("textures/techy1.jpg")
    rockimg2 = pi3d.Texture("textures/rocktile2.jpg")
    shineimg = pi3d.Texture("textures/stars.jpg")
    
    # environment cube
    ectex = pi3d.Texture("textures/ecubes/skybox_stormydays.jpg")
    myecube = pi3d.EnvironmentCube(size=900.0, maptype="CROSS")
    myecube.set_draw_details(flatsh, ectex)
    
    # Create elevation map
    # inWidth = Width of Map (i.e. 1024.0)
    # inDepth = Depth of Map (i.e. 1024.0)
    # inHeight = Height of Map (i.e 0.5)
    mapwidth = inWidth
    mapdepth = inDepth
    mapheight = inHeight
    bumpsh = pi3d.Shader('uv_bump')
    
    # inHeightmap = Maps/seed_XXXXX_grayscale.png
    # inTextureMap = Maps/seed_XXXXX_elevation.png
    # inBumpMap = Maps/seed_XXXXX_normal.png
    mymap = pi3d.ElevationMap(inHeightmap, width=mapwidth, depth=mapdepth, height=mapheight, divx=199, divy=199, name="sub")
    mymap.set_draw_details(shader, [rockimg1, rockimg2, shineimg], 128.0, 0.05)
    redplanet = pi3d.Texture(inTextureMap)
    bumpimg = pi3d.Texture(inBumpMap)
    mymap.set_draw_details(bumpsh, [redplanet, bumpimg], 128.0, 0.0)
    mymap.set_fog((0.3, 0.15, 0.1, 0.0), 1000.0)
    
    rot = 0.0
    tilt = 0.0
    avhgt = 3.0
    xm, oxm = 0.0, -1.0
    zm, ozm = 0.0, -1.0
    ym = mymap.calcHeight(xm, zm) + avhgt
    
    # Fetch key presses
    mykeys = pi3d.Keyboard()
    mymouse = pi3d.Mouse(restrict=False)
    mymouse.start()
    
    omx, omy = mymouse.position()
    
    fly = False
    walk = True
    
    CAMERA = pi3d.Camera.instance()

    print ('at line 71 - Code3D')
    while DISPLAY.loop_running():
        # movement of camera
        mx, my = mymouse.position()
        rot -= (mx - omx) * 0.2
        tilt += (my - omy) * 0.1
    
        dx = -math.sin(rot * rads)
        dz = math.cos(rot * rads)
        dy = math.sin(tilt * rads)

        if walk:
            if fly:
                xm += dx * 3
                zm += dz * 3
                ym += dy * 3
            else:
                dy = mymap.calcHeight(xm + dx * 1.5, zm + dz * 1.5) + avhgt - ym

            if dy < 1.2:  # limit steepness so can't climb up walls
                xm += dx * 0.5
                zm += dz * 0.5
                ym += dy * 0.5
        
            if xm < -490 or xm > 490 or zm < -490 or zm > 490:
                fly = True  # reached the edge
      
        if not (mx == omx and my == omy and oxm == xm and ozm == zm):
            CAMERA.reset()
            CAMERA.rotate(tilt, 0, 0)
            CAMERA.rotate(0, rot, 0)
            CAMERA.position((xm, ym, zm))
        
        omx = mx
        omy = my
        oxm = xm
        ozm = zm
        light.position((xm, ym + 15.0, zm))
        light.is_point = True
    
        mymap.set_light(light)
    
        myecube.position(xm, ym, zm)
        myecube.draw()
        mymap.draw()

        # key presses (ESCAPE to terminate)
        k = mykeys.read()

        if k > -1:
            if k == 119:  # W Key toggle
                walk = not walk
            elif k == 115:  # S Key
                walk = False
                dy = -(mymap.calcHeight(xm - dx, zm - dz) + avhgt) - ym
          
                if dy > -1.0:
                    xm -= dx
                    zm -= dz
                    ym += dy
            elif k == 27:  # ESCAPE key
                DISPLAY.destroy()
                mykeys.close()
                mymouse.stop()
                break
    
        # this will save a little time each loop if the camera is not moved
        CAMERA.was_moved = False
    
    quit()