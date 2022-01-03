import numpy
import time
import noise

import simulations.basic as basic
import simulations.hydrology as hydro
import simulations.irrigation as irri
import simulations.humidity as humid
import simulations.temperature as temp
import simulations.permeability as perm
import simulations.erosion as erosion
import simulations.precipitation as precip
import simulations.biome as biome
import simulations.icecap as icecap
import simulations.wind as wind
from common import anti_alias, get_verbose
from model.world import Step

# ------------------
# Initial generation
# ------------------


def center_land(world):
    """Translate the map horizontally and vertically to put as much ocean as
       possible at the borders. It operates on elevation and plates map"""

    y_sums = world.layers['elevation'].data.sum(1)  # 1 == sum along x-axis
    y_with_min_sum = y_sums.argmin()
    
    x_sums = world.layers['elevation'].data.sum(0)  # 0 == sum along y-axis
    x_with_min_sum = x_sums.argmin()

    latshift = 0
    world.layers['elevation'].data = numpy.roll(numpy.roll(world.layers['elevation'].data, -y_with_min_sum + latshift, axis=0), - x_with_min_sum, axis=1)
    world.layers['plates'].data = numpy.roll(numpy.roll(world.layers['plates'].data, -y_with_min_sum + latshift, axis=0), - x_with_min_sum, axis=1)


def place_oceans_at_map_borders(world):
    """
    Lower the elevation near the border of the map
    """

    ocean_border = int(min(30, max(world.width / 5, world.height / 5)))

    def place_ocean(x, y, i):
        world.layers['elevation'].data[y, x] = \
            (world.layers['elevation'].data[y, x] * i) / ocean_border

    for x in range(world.width):
        for i in range(ocean_border):
            place_ocean(x, i, i)
            place_ocean(x, world.height - i - 1, i)

    for y in range(world.height):
        for i in range(ocean_border):
            place_ocean(i, y, i)
            place_ocean(world.width - i - 1, y, i)


def add_noise_to_elevation(world, seed):
    octaves = 8
    freq = 16.0 * octaves
    
    for y in range(world.height):
        for x in range(world.width):
            n = noise.snoise2(x / freq * 2, y / freq * 2, octaves, base=seed)
            world.layers['elevation'].data[y, x] += n


def fill_ocean(elevation, sea_level):
    height, width = elevation.shape

    ocean = numpy.zeros(elevation.shape, dtype=bool)
    to_expand = []
    
    for x in range(width):  # handle top and bottom border of the map
        if elevation[0, x] <= sea_level:
            to_expand.append((x, 0))
    
        if elevation[height - 1, x] <= sea_level:
            to_expand.append((x, height - 1))
    
    for y in range(height):  # handle left- and rightmost border of the map
        if elevation[y, 0] <= sea_level:
            to_expand.append((0, y))
    
        if elevation[y, width - 1] <= sea_level:
            to_expand.append((width - 1, y))

    for t in to_expand:
        tx, ty = t
    
        if not ocean[ty, tx]:
            ocean[ty, tx] = True
        
            for px, py in _around(tx, ty, width, height):
                if not ocean[py, px] and elevation[py, px] <= sea_level:
                    to_expand.append((px, py))

    return ocean


def initialize_ocean_and_thresholds(world, ocean_level=1.0):
    """
    Calculate the ocean, the sea depth and the elevation thresholds
    :param world: a world having elevation but not thresholds
    :param ocean_level: the elevation representing the ocean level
    :return: nothing, the world will be changed
    """
    e = world.layers['elevation'].data
    ocean = fill_ocean(e, ocean_level)
    hl = basic.find_threshold_f(e, 0.10)  # the highest 10% of all (!) land are declared hills
    ml = basic.find_threshold_f(e, 0.03)  # the highest 3% are declared mountains
    e_th = [('sea', ocean_level),
            ('plain', hl),
            ('hill', ml),
            ('mountain', None)]
    
    harmonize_ocean(ocean, e, ocean_level)
    world.set_ocean(ocean)
    world.set_elevation(e, e_th)
    world.set_sea_depth(sea_depth(world, ocean_level))


def harmonize_ocean(ocean, elevation, ocean_level):
    """
    The goal of this function is to make the ocean floor less noisy.
    The underwater erosion should cause the ocean floor to be more uniform
    """

    shallow_sea = ocean_level * 0.85
    midpoint = shallow_sea / 2.0

    ocean_points = numpy.logical_and(elevation < shallow_sea, ocean)

    shallow_ocean = numpy.logical_and(elevation < midpoint, ocean_points)
    elevation[shallow_ocean] = midpoint - ((midpoint - elevation[shallow_ocean]) / 5.0)

    deep_ocean = numpy.logical_and(elevation > midpoint, ocean_points)
    elevation[deep_ocean] = midpoint + ((elevation[deep_ocean] - midpoint) / 5.0)

# ----
# Misc
# ----
def sea_depth(world, sea_level):
    sea_depth1 = sea_level - world.layers['elevation'].data

    for y in range(world.height):
        for x in range(world.width):
            if world.tiles_around((x, y), radius=1, predicate=world.is_land):
                sea_depth1[y, x] = 0
            elif world.tiles_around((x, y), radius=2, predicate=world.is_land):
                sea_depth1[y, x] *= 0.3
            elif world.tiles_around((x, y), radius=3, predicate=world.is_land):
                sea_depth1[y, x] *= 0.5
            elif world.tiles_around((x, y), radius=4, predicate=world.is_land):
                sea_depth1[y, x] *= 0.7
            elif world.tiles_around((x, y), radius=5, predicate=world.is_land):
                sea_depth1[y, x] *= 0.9
    
    sea_depth1 = anti_alias(sea_depth1, 10)

    min_depth = sea_depth1.min()
    max_depth = sea_depth1.max()
    sea_depth1 = (sea_depth1 - min_depth) / (max_depth - min_depth)
    
    return sea_depth1

def _around(x, y, width, height):
    ps = []

    for dx in range(-1, 2):
        nx = x + dx
    
        if 0 <= nx < width:
            for dy in range(-1, 2):
                ny = y + dy
        
                if 0 <= ny < height and (dx != 0 or dy != 0):
                    ps.append((nx, ny))
   
    return ps

def generate_world(obj, w, step, erosion_curve1, erosion_curve2, erosion_curve3,
                   erosion_max_radius, erosion_maxRadius, erosion_radius,
                   humidity_irrigationWeight, humidity_precipitation_weight,
                   hydrology_creek, hydrology_main_river, hydrology_river, irrigation_radius,
                   icecap_freeze_chance_window, icecap_max_freeze_percentage, icecap_surrounding_tile_influence,
                   permeability_freq, permeability_octaves, permeability_perm_th_low, permeability_perm_th_med,
                   precipitation_freq, precipitation_octaves, precipitation_ths_low, precipitation_ths_med,
                   temperature_axial_tilt_hwhm, temperature_distance_to_sun_hwhm, temperature_frequency, temperature_octaves,
                   wind_frequency, wind_octaves):

    if get_verbose():
        start_time = time.time()
        obj.updatePopup(' ')
        obj.updatePopup('Generating World ...')
        obj.updatePopup('    Running Temperature Simulation ...')

    # Prepare sufficient seeds for the different steps of the generation
    rng = numpy.random.RandomState(w.seed)  # create a fresh RNG in case the global RNG is compromised (i.e. has been queried an indefinite amount of times before generate_world() was called)
    sub_seeds = rng.randint(0, numpy.iinfo(numpy.int32).max, size=100)  # choose lowest common denominator (32 bit Windows numpy cannot handle a larger value)
    seed_dict = {
                 'PrecipitationSimulation': sub_seeds[0],  # after 0.19.0 do not ever switch out the seeds here to maximize seed-compatibility
                 'ErosionSimulation':       sub_seeds[1],
                 'WatermapSimulation':      sub_seeds[2],
                 'IrrigationSimulation':    sub_seeds[3],
                 'TemperatureSimulation':   sub_seeds[4],
                 'HumiditySimulation':      sub_seeds[5],
                 'PermeabilitySimulation':  sub_seeds[6],
                 'BiomeSimulation':         sub_seeds[7],
                 'IcecapSimulation':        sub_seeds[8],
                 'WindSimulation':          sub_seeds[9],
                 '':                        sub_seeds[99]
    }

    w = temp.TemperatureSimulation().execute(w, seed_dict['TemperatureSimulation'], temperature_distance_to_sun_hwhm,
                                             temperature_axial_tilt_hwhm, temperature_frequency, temperature_octaves)

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Temperature Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Precipitation Simulation ...')

    # Precipitation with thresholds
    w = precip.PrecipitationSimulation().execute(w, seed_dict['PrecipitationSimulation'], precipitation_freq, precipitation_octaves, precipitation_ths_low, precipitation_ths_med)

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Precipitation Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Erosion Simulation ...')

    w = erosion.ErosionSimulation().execute(w, seed_dict['ErosionSimulation'], hydrology_river, erosion_max_radius,
                                            erosion_maxRadius, erosion_radius, erosion_curve1, erosion_curve2, erosion_curve3)  # seed not currently used

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Erosion Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Watermap Simulation ...')

    w = hydro.WatermapSimulation().execute(w, seed_dict['WatermapSimulation'], hydrology_creek, hydrology_main_river, hydrology_river)  # seed not currently used

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Watermap Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Irrigation Simulation ...')

    w = irri.IrrigationSimulation().execute(w, seed_dict['IrrigationSimulation'], irrigation_radius)  # seed not currently used

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Irrigation Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Humidity Simulation ...')

    w = humid.HumiditySimulation().execute(w, seed_dict['HumiditySimulation'], humidity_irrigationWeight, humidity_precipitation_weight)  # seed not currently used

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Humidity Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Permeability Simulation ...')

    w = perm.PermeabilitySimulation().execute(w, seed_dict['PermeabilitySimulation'], permeability_freq, permeability_octaves,
                                              permeability_perm_th_low, permeability_perm_th_med)

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Permeability Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Biome Simulation ...')
        obj.updatePopup(' ')

    w, cm, biome_cm = biome.BiomeSimulation().execute(w, seed_dict['BiomeSimulation'])  # seed not currently used

    for cl in cm.keys():
        count = cm[cl]

        if get_verbose():
            obj.updatePopup('        %s = %i' % (str(cl), count))

    if get_verbose():
        obj.updatePopup('    Biomes obtained:')

    for cl in biome_cm.keys():
        count = biome_cm[cl]

        if get_verbose():
            obj.updatePopup('        %30s = %7i' % (str(cl), count))

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup(' ')
        obj.updatePopup('    Biome Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Icecap Simulation ...')

    w = icecap.IcecapSimulation().execute(w, seed_dict['IcecapSimulation'], icecap_freeze_chance_window,
                                          icecap_max_freeze_percentage, icecap_surrounding_tile_influence)  # makes use of temperature-map
    
    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Icecap Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))
        obj.updatePopup('    Running Wind Simulation ...')

    w = wind.WindSimulation().execute(w, seed_dict['WindSimulation'], wind_frequency, wind_octaves)

    if get_verbose():
        elapsed_time = time.time() - start_time
        start_time = time.time()
        obj.updatePopup('    Wind Simulation completed in %s seconds' % str(format(elapsed_time, '.3f')))

    return w
