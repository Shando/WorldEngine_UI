"""
This file should contain only functions that operates on pixels, not on images,
so no references to PIL are necessary and the module can be used also through
Jython
"""

import time
import numpy

# -------------------
# Reusable functions
# -------------------
def gradient(value, low, high, low_color, high_color):
    lr, lg, lb = low_color
    if high == low:
        return lr, lg, lb, 255
    _range = float(high - low)
    _x = float(value - low) / _range
    _ix = 1.0 - _x
    hr, hg, hb = high_color
    r = int(lr * _ix + hr * _x)
    g = int(lg * _ix + hg * _x)
    b = int(lb * _ix + hb * _x)
    return r, g, b, 255

def rgba_to_rgb(rgba):
    r, g, b, a = rgba
    return r, g, b

def draw_rivers_on_image(world, target, factor=1):
    # Draw only the rivers, it expects the background to be in place
    for y in range(world.height):
        for x in range(world.width):
            if world.is_land((x, y)) and (world.layers['river_map'].data[y, x] > 0.0):
                for dx in range(int(factor)):
                    for dy in range(int(factor)):
                        x1 = int(x * factor + dx)
                        y1 = int(y * factor + dx)
                        target.set_pixel(x1, y1, (0, 0, 128, 255))

            if world.is_land((x, y)) and (world.layers['lake_map'].data[y, x] != 0):
                for dx in range(int(factor)):
                    for dy in range(int(factor)):
                        x1 = int(x * factor + dx)
                        y1 = int(y * factor + dx)
                        target.set_pixel(x1, y1, (0, 100, 128, 255))

# -------------------
# Drawing ancient map
# -------------------
def _find_land_borders(world, factor):
    _ocean = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=bool)
    _borders = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=bool)

    # scale ocean
    for y in range(int(world.height * factor)):
        for x in range(int(world.width * factor)):
            if world.is_ocean((int(x / factor), int(y / factor))):
                _ocean[y, x] = True

    def my_is_ocean(pos):
        x, y = pos
        return _ocean[y, x]

    for y in range(int(world.height * factor)):
        for x in range(int(world.width * factor)):
            if not _ocean[y, x] and world.tiles_around_factor(factor, (x, y), radius=1, predicate=my_is_ocean):
                _borders[y, x] = True

    return _borders


def _find_outer_borders(world, factor, inner_borders):
    _ocean = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=bool)
    _borders = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=bool)

    # scale ocean
    for y in range(int(world.height * factor)):
        for x in range(int(world.width * factor)):
            if world.is_ocean((int(x / factor), int(y / factor))):
                _ocean[y, x] = True

    def is_inner_border(pos):
        x, y = pos
        return inner_borders[y, x]

    for y in range(int(world.height * factor)):
        for x in range(int(world.width * factor)):
            if _ocean[y, x] and not inner_borders[y, x] and world.tiles_around_factor(factor, (x, y), radius=1, predicate=is_inner_border):
                _borders[y, x] = True

    return _borders


def _find_mountains_mask(world, factor):
    _mask = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=float)

    for y in range(int(factor * world.height)):
        for x in range(int(factor * world.width)):
            if world.is_mountain((int(x / factor), int(y / factor))):
                v = len(world.tiles_around((int(x / factor), int(y / factor)), radius=3, predicate=world.is_mountain))

                if v > 32:
                    _mask[y, x] = v / 4.0  # force conversion to float, Python 2 will *not* do it automatically

    return _mask


def _mask(world, predicate, factor):
    _mask = numpy.zeros((int(factor * world.height), int(factor * world.width)), dtype=float)

    for y in range(int(factor * world.height)):
        for x in range(int(factor * world.width)):
            xf = int(x / factor)
            yf = int(y / factor)

            if predicate((xf, yf)):
                v = len(world.tiles_around((xf, yf), radius=1, predicate=predicate))

                if v > 5:
                    _mask[y, x] = v

    return _mask


def _find_boreal_forest_mask(world, factor):
    return _mask(world, predicate=world.is_boreal_forest, factor=factor)


def _find_temperate_forest_mask(world, factor):
    return _mask(world, predicate=world.is_temperate_forest, factor=factor)


def _find_warm_temperate_forest_mask(world, factor):
    return _mask(world, predicate=world.is_warm_temperate_forest, factor=factor)


def _find_tropical_dry_forest_mask(world, factor):
    return _mask(world, predicate=world.is_tropical_dry_forest, factor=factor)


def _draw_glacier(pixels, x, y):
    rg = 255 - (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    pixels[y, x] = (rg, rg, 255, 255)


def _draw_tundra(pixels, x, y):
    b = (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    r = 166 - b
    g = 148 - b
    b = 75 - b
    pixels[y, x] = (r, g, b, 255)


def _draw_cold_parklands(pixels, x, y):
    b = (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    r = 105 - b
    g = 96 - b
    b = 38 - int(b / 2)
    pixels[y, x] = (r, g, b, 255)


def _draw_boreal_forest(pixels, x, y, w, h):
    c = (0, 32, 0, 255)
    c2 = (0, 64, 0, 255)
    pixels[y - 4, x + 0] = c
    pixels[y - 3, x + 0] = c
    pixels[y - 2, x - 1] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 1, x - 1] = c
    pixels[y - 1, x + 1] = c
    pixels[y + 0, x - 2] = c
    pixels[y + 0, x + 1] = c
    pixels[y + 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 3] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x + 3] = c
    pixels[y + 3, x - 3] = c
    pixels[y + 3, x - 2] = c
    pixels[y + 3, x - 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 3, x + 1] = c
    pixels[y + 3, x + 2] = c
    pixels[y + 3, x + 3] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 2, x + 0] = c2
    pixels[y - 1, x + 0] = c2
    pixels[y - 0, x - 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2
    pixels[y + 1, x + 1] = c2
    pixels[y + 2, x - 2] = c2
    pixels[y + 2, x - 0] = c2
    pixels[y + 2, x + 1] = c2
    pixels[y + 2, x + 2] = c2


def _draw_temperate_forest1(pixels, x, y, w, h):
    c = (0, 64, 0, 255)
    c2 = (0, 96, 0, 255)
    pixels[y - 4, x + 0] = c
    pixels[y - 3, x + 0] = c
    pixels[y - 2, x - 1] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 1, x - 1] = c
    pixels[y - 1, x + 1] = c
    pixels[y + 0, x - 2] = c
    pixels[y + 0, x + 1] = c
    pixels[y + 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 3] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x + 3] = c
    pixels[y + 3, x - 3] = c
    pixels[y + 3, x - 2] = c
    pixels[y + 3, x - 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 3, x + 1] = c
    pixels[y + 3, x + 2] = c
    pixels[y + 3, x + 3] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 2, x + 0] = c2
    pixels[y - 1, x + 0] = c2
    pixels[y - 0, x - 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2
    pixels[y + 1, x + 1] = c2
    pixels[y + 2, x - 2] = c2
    pixels[y + 2, x - 0] = c2
    pixels[y + 2, x + 1] = c2
    pixels[y + 2, x + 2] = c2


def _draw_temperate_forest2(pixels, x, y, w, h):
    c = (0, 64, 0, 255)
    c2 = (0, 112, 0, 255)
    pixels[y - 4, x - 1] = c
    pixels[y - 4, x - 0] = c
    pixels[y - 4, x + 1] = c
    pixels[y - 3, x - 2] = c
    pixels[y - 3, x - 1] = c
    pixels[y - 3, x + 2] = c
    pixels[y - 2, x - 2] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x + 2] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 1] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x - 0] = c
    pixels[y + 2, x + 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 3, x + 0] = c2
    pixels[y - 3, x + 1] = c2
    pixels[y - 2, x - 1] = c2
    pixels[y - 2, x - 0] = c2
    pixels[y - 1, x - 1] = c2
    pixels[y - 1, x - 0] = c2
    pixels[y - 1, x + 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y - 0, x + 1] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2


def _draw_steppe(pixels, x, y):
    b = (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    r = 96 - b
    g = 192 - b
    b = 96 - b
    pixels[y, x] = (r, g, b, 255)


def _draw_cool_desert(pixels, x, y, w, h):
    c = (72, 72, 53, 255)

    pixels[y - 2, x - 1] = c
    pixels[y - 2, x - 0] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x - 1] = c
    pixels[y - 1, x - 0] = c
    pixels[y - 1, x + 4] = c
    pixels[y - 0, x - 4] = c
    pixels[y - 0, x - 3] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y - 0, x + 6] = c
    pixels[y + 1, x - 5] = c
    pixels[y + 1, x - 0] = c
    pixels[y + 1, x + 7] = c
    pixels[y + 1, x + 8] = c
    pixels[y + 2, x - 8] = c
    pixels[y + 2, x - 7] = c


def _draw_warm_temperate_forest(pixels, x, y, w, h):
    c = (0, 96, 0, 255)
    c2 = (0, 192, 0, 255)
    pixels[y - 4, x - 1] = c
    pixels[y - 4, x - 0] = c
    pixels[y - 4, x + 1] = c
    pixels[y - 3, x - 2] = c
    pixels[y - 3, x - 1] = c
    pixels[y - 3, x + 2] = c
    pixels[y - 2, x - 2] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x + 2] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 1] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x - 0] = c
    pixels[y + 2, x + 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 3, x + 0] = c2
    pixels[y - 3, x + 1] = c2
    pixels[y - 2, x - 1] = c2
    pixels[y - 2, x - 0] = c2
    pixels[y - 1, x - 1] = c2
    pixels[y - 1, x - 0] = c2
    pixels[y - 1, x + 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y - 0, x + 1] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2


def _draw_chaparral(pixels, x, y):
    b = (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    r = 180 - b
    g = 171 - b
    b = 113 - b
    pixels[y, x] = (r, g, b, 255)


def _draw_hot_desert(pixels, x, y, w, h):
    c = (72, 72, 53, 255)

    pixels[y - 2, x - 1] = c
    pixels[y - 2, x - 0] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x - 1] = c
    pixels[y - 1, x - 0] = c
    pixels[y - 1, x + 4] = c
    pixels[y - 0, x - 4] = c
    pixels[y - 0, x - 3] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y - 0, x + 6] = c
    pixels[y + 1, x - 5] = c
    pixels[y + 1, x - 0] = c
    pixels[y + 1, x + 7] = c
    pixels[y + 1, x + 8] = c
    pixels[y + 2, x - 8] = c
    pixels[y + 2, x - 7] = c


def _draw_tropical_dry_forest(pixels, x, y, w, h):
    c = (51, 36, 3, 255)
    c2 = (139, 204, 58, 255)
    pixels[y - 4, x - 1] = c
    pixels[y - 4, x - 0] = c
    pixels[y - 4, x + 1] = c
    pixels[y - 3, x - 2] = c
    pixels[y - 3, x - 1] = c
    pixels[y - 3, x + 2] = c
    pixels[y - 2, x - 2] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x + 2] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 1] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x - 0] = c
    pixels[y + 2, x + 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 3, x + 0] = c2
    pixels[y - 3, x + 1] = c2
    pixels[y - 2, x - 1] = c2
    pixels[y - 2, x - 0] = c2
    pixels[y - 1, x - 1] = c2
    pixels[y - 1, x - 0] = c2
    pixels[y - 1, x + 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y - 0, x + 1] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2


def _draw_jungle(pixels, x, y, w, h):
    c = (0, 128, 0, 255)
    c2 = (0, 255, 0, 255)
    pixels[y - 4, x - 1] = c
    pixels[y - 4, x - 0] = c
    pixels[y - 4, x + 1] = c
    pixels[y - 3, x - 2] = c
    pixels[y - 3, x - 1] = c
    pixels[y - 3, x + 2] = c
    pixels[y - 2, x - 2] = c
    pixels[y - 2, x + 1] = c
    pixels[y - 2, x + 2] = c
    pixels[y - 1, x - 2] = c
    pixels[y - 1, x + 2] = c
    pixels[y - 0, x - 2] = c
    pixels[y - 0, x - 1] = c
    pixels[y - 0, x + 2] = c
    pixels[y + 1, x - 2] = c
    pixels[y + 1, x + 1] = c
    pixels[y + 1, x + 2] = c
    pixels[y + 2, x - 1] = c
    pixels[y + 2, x - 0] = c
    pixels[y + 2, x + 1] = c
    pixels[y + 3, x - 0] = c
    pixels[y + 4, x - 0] = c

    pixels[y - 3, x + 0] = c2
    pixels[y - 3, x + 1] = c2
    pixels[y - 2, x - 1] = c2
    pixels[y - 2, x - 0] = c2
    pixels[y - 1, x - 1] = c2
    pixels[y - 1, x - 0] = c2
    pixels[y - 1, x + 1] = c2
    pixels[y - 0, x - 0] = c2
    pixels[y - 0, x + 1] = c2
    pixels[y + 1, x - 1] = c2
    pixels[y + 1, x - 0] = c2


def _draw_savanna(pixels, x, y):
    b = (x ** int(y / 5) + x * 23 + y * 37 + (x * y) * 13) % 75
    r = 255 - b
    g = 246 - b
    b = 188 - b
    pixels[y, x] = (r, g, b, 255)


def _draw_a_mountain(pixels, x, y, w=3, h=3, land_color=(181, 166, 127, 255)):
    mcr = (75, 75, 75, 255)

    # left edge
    for mody in range(-h, h + 1):
        bottomness = (float(mody + h) / 2.0) / w
        leftborder = int(bottomness * w)
        darkarea = int(bottomness * w / 2)
        lightarea = int(bottomness * w / 2)

        for itx in range(darkarea, leftborder + 1):
            pixels[y + mody, x - itx] = gradient(itx, darkarea, leftborder, (0, 0, 0), (64, 64, 64))
        for itx in range(-darkarea, lightarea + 1):
            pixels[y + mody, x + itx] = gradient(itx, -darkarea, lightarea, (64, 64, 64), (128, 128, 128))
        for itx in range(lightarea, leftborder):
            pixels[y + mody, x + itx] = land_color

    # right edge
    for mody in range(-h, h + 1):
        bottomness = (float(mody + h) / 2.0) / w
        modx = int(bottomness * w)
        pixels[y + mody, x + modx] = mcr      


def draw_ancientmap(obj, world, target, resize_factor=1, sea_color=(212, 198, 169, 255), draw_biome=True,
                    land_color=(181, 166, 127, 255), draw_rivers=True, draw_mountains=True,
                    draw_outer_land_border=False, verbose=False):
    rng = numpy.random.RandomState(world.seed)  # create our own random generator

    if verbose:
        start_time = time.time()
        obj.updatePopup('    Initialisation started ...')

    borders = _find_land_borders(world, resize_factor)

    if draw_outer_land_border:
        outer_borders = _find_outer_borders(world, resize_factor, borders)
        outer_borders = _find_outer_borders(world, resize_factor, outer_borders)

    if draw_mountains:
        mountains_mask = _find_mountains_mask(world, resize_factor)

    if draw_biome:
        boreal_forest_mask = _find_boreal_forest_mask(world, resize_factor)
        temperate_forest_mask = _find_temperate_forest_mask(world, resize_factor)
        warm_temperate_forest_mask = _find_warm_temperate_forest_mask(world, resize_factor)
        tropical_dry_forest_mask = _find_tropical_dry_forest_mask(world, resize_factor)
        # jungle is actually Tropical Rain Forest and Tropical Seasonal Forest
        jungle_mask = _mask(world, world.is_jungle, resize_factor)
        tundra_mask = _mask(world, world.is_tundra, resize_factor)
        # savanna is actually Tropical semi-arid
        savanna_mask = _mask(world, world.is_savanna, resize_factor)
        cold_parklands_mask = _mask(world, world.is_cold_parklands, resize_factor)
        steppe_mask = _mask(world, world.is_steppe, resize_factor)
        cool_desert_mask = _mask(world, world.is_cool_desert, resize_factor)
        chaparral_mask = _mask(world, world.is_chaparral, resize_factor)
        hot_desert_mask = _mask(world, world.is_hot_desert, resize_factor)
        rock_desert_mask = _mask(world, world.is_hot_desert, resize_factor)

    def unset_mask(pos):
        x, y = pos
        mountains_mask[y, x] = 0

    def unset_boreal_forest_mask(pos):
        x, y = pos
        boreal_forest_mask[y, x] = 0

    def unset_temperate_forest_mask(pos):
        x, y = pos
        temperate_forest_mask[y, x] = 0

    def unset_warm_temperate_forest_mask(pos):
        x, y = pos
        warm_temperate_forest_mask[y, x] = 0

    def unset_tropical_dry_forest_mask(pos):
        x, y = pos
        tropical_dry_forest_mask[y, x] = 0

    def unset_jungle_mask(pos):
        x, y = pos
        jungle_mask[y, x] = 0

    def unset_tundra_mask(pos):
        x, y = pos
        tundra_mask[y, x] = 0

    def unset_savanna_mask(pos):
        x, y = pos
        savanna_mask[y, x] = 0

    def unset_hot_desert_mask(pos):
        x, y = pos
        hot_desert_mask[y, x] = 0

    def unset_rock_desert_mask(pos):
        x, y = pos
        rock_desert_mask[y, x] = 0

    def unset_cold_parklands_mask(pos):
        x, y = pos
        cold_parklands_mask[y, x] = 0

    def unset_steppe_mask(pos):
        x, y = pos
        steppe_mask[y, x] = 0

    def unset_cool_desert_mask(pos):
        x, y = pos
        cool_desert_mask[y, x] = 0

    def unset_chaparral_mask(pos):
        x, y = pos
        chaparral_mask[y, x] = 0

    def on_border(pos):
        x, y = pos
        return borders[y, x]

    if verbose:
        elapsed_time = time.time() - start_time
        obj.updatePopup('    Initialisation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        start_time = time.time()
        obj.updatePopup('    Colour Ocean started ...')

    border_color = (0, 0, 0, 255)
    outer_border_color = gradient(0.5, 0, 1.0, rgba_to_rgb(border_color), rgba_to_rgb(sea_color))

    for y in range(int(resize_factor * world.height)):
        for x in range(int(resize_factor * world.width)):
            xf = int(x / resize_factor)
            yf = int(y / resize_factor)

            if borders[y, x]:
                target.set_pixel(x, y, border_color)
            elif draw_outer_land_border and outer_borders[y, x]:
                target.set_pixel(x, y, outer_border_color)
            elif world.is_ocean((xf, yf)):
                target.set_pixel(x, y, sea_color)
            else:
                target.set_pixel(x, y, land_color)

    if verbose:
        elapsed_time = time.time() - start_time
        obj.updatePopup('    Colour Ocean completed in %s seconds' % str(format(elapsed_time, '.3f')))
        start_time = time.time()
        obj.updatePopup('    Anti Alias started ...')

    def anti_alias(steps):
        def _anti_alias_step():
            for y in range(int(resize_factor * world.height)):
                for x in range(int(resize_factor * world.width)):
                    _anti_alias_point(x, y)

        def _anti_alias_point(x, y):
            n = 2
            tot_r = target[y, x][0] * 2
            tot_g = target[y, x][1] * 2
            tot_b = target[y, x][2] * 2

            for dy in range(-1, +2):
                py = y + dy

                if 0 < py < int(resize_factor * world.height):
                    for dx in range(-1, +2):
                        px = x + dx

                        if 0 < px < int(resize_factor * world.width):
                            n += 1
                            tot_r += target[py, px][0]
                            tot_g += target[py, px][1]
                            tot_b += target[py, px][2]

            r = int(tot_r / n)
            g = int(tot_g / n)
            b = int(tot_b / n)
            target[y, x] = (r, g, b, 255)

        for i in range(steps):
            _anti_alias_step()

    anti_alias(1)

    if verbose:
        elapsed_time = time.time() - start_time
        obj.updatePopup('    Anti Alias completed in %s seconds' % str(format(elapsed_time, '.3f')))

    # Draw glacier
    if draw_biome:
        if verbose:
            start_time = time.time()
            obj.updatePopup('    Draw Biomes started ...')

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if not borders[y, x] and world.is_iceland((int(x / resize_factor), int(y / resize_factor))):
                    _draw_glacier(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Glacier completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw tundra
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if tundra_mask[y, x] > 0:
                    _draw_tundra(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Tundra completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw cold parklands
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if cold_parklands_mask[y, x] > 0:
                    _draw_cold_parklands(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Cold Parklands completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw steppes
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if steppe_mask[y, x] > 0:
                    _draw_steppe(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Steppe completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw chaparral
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if chaparral_mask[y, x] > 0:
                    _draw_chaparral(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Chaparral completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw savanna
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if savanna_mask[y, x] > 0:
                    _draw_savanna(target, x, y)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Savannah completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw cool desert
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if cool_desert_mask[y, x] > 0:
                    w = 8
                    h = 2
                    r = 9

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_cool_desert(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_cool_desert_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Cool Desert completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw hot desert
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if hot_desert_mask[y, x] > 0:
                    w = 8
                    h = 2
                    r = 9

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_hot_desert(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_hot_desert_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Hot Desert completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw boreal forest
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if boreal_forest_mask[y, x] > 0:
                    w = 4
                    h = 5
                    r = 6

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_boreal_forest(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_boreal_forest_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Boreal Forest completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw temperate forest
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if temperate_forest_mask[y, x] > 0:
                    w = 4
                    h = 5
                    r = 6

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        if rng.random_sample() <= .5:
                            _draw_temperate_forest1(target, x, y, w=w, h=h)
                        else:
                            _draw_temperate_forest2(target, x, y, w=w, h=h)

                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_temperate_forest_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Temperate Forest completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw warm temperate forest
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if warm_temperate_forest_mask[y, x] > 0:
                    w = 4
                    h = 5
                    r = 6

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_warm_temperate_forest(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_warm_temperate_forest_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Warm Temperate Forest completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw dry tropical forest
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if tropical_dry_forest_mask[y, x] > 0:
                    w = 4
                    h = 5
                    r = 6

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_tropical_dry_forest(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_tropical_dry_forest_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Dry Tropical Forest completed in %s seconds' % str(format(elapsed_time, '.3f')))
        # Draw jungle
            start_time = time.time()

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if jungle_mask[y, x] > 0:
                    w = 4
                    h = 5
                    r = 6

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_jungle(target, x, y, w=w, h=h)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_jungle_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Jungle completed in %s seconds' % str(format(elapsed_time, '.3f')))

    if draw_rivers:
        if verbose:
            start_time = time.time()
            obj.updatePopup('    Draw Rivers started ...')

        draw_rivers_on_image(world, target, resize_factor)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Rivers completed in %s seconds' % str(format(elapsed_time, '.3f')))

    # Draw mountains
    if draw_mountains:
        if verbose:
            start_time = time.time()
            obj.updatePopup('    Draw Mountains started ...')

        for y in range(int(resize_factor * world.height)):
            for x in range(int(resize_factor * world.width)):
                if mountains_mask[y, x] > 0:
                    w = mountains_mask[y, x]
                    h = 3 + int(world.level_of_mountain((int(x / resize_factor), int(y / resize_factor))))
                    r = max(int(w / 3 * 2), h)

                    if len(world.tiles_around_factor(resize_factor, (x, y), radius=r, predicate=on_border)) <= 2:
                        _draw_a_mountain(target, x, y, w, h, land_color)
                        world.on_tiles_around_factor(resize_factor, (x, y), radius=r, action=unset_mask)

        if verbose:
            elapsed_time = time.time() - start_time
            obj.updatePopup('    Draw Mountains completed in %s seconds' % str(format(elapsed_time, '.3f')))
