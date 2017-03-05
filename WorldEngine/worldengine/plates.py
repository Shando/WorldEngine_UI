# Every reference to platec has to be kept separated because it is a C
# extension which is not available when using this project from jython

import platec
import time
import numpy
# from generation import Step, add_noise_to_elevation, center_land, generate_world, \
#    get_verbose, initialize_ocean_and_thresholds, place_oceans_at_map_borders
# from model.world import World, Size, GenerationParameters

from generation import Step, add_noise_to_elevation, center_land, generate_world, \
    get_verbose, initialize_ocean_and_thresholds, place_oceans_at_map_borders
import model.world as modWorld


def generate_plates_simulation(obj, seed, width, height, sea_level=0.65,
                               erosion_period=60, folding_ratio=0.02,
                               aggr_overlap_abs=1000000, aggr_overlap_rel=0.33,
                               cycle_count=2, num_plates=10):

    p = platec.create(seed, width, height, sea_level, erosion_period,
                      folding_ratio, aggr_overlap_abs, aggr_overlap_rel,
                      cycle_count, num_plates)
    # Note: To rescale the worlds heightmap to roughly Earths scale, multiply by 2000.

    while platec.is_finished(p) == 0:
        platec.step(p)
    
    hm = platec.get_heightmap(p)
    pm = platec.get_platesmap(p)
    
    return hm, pm


def _plates_simulation(obj, name, width, height, seed, temps=[.874, .765, .594, .439, .366, .124],
                       humids=[.941, .778, .507, .236, 0.073, .014, .002], gamma_curve=1.25,
                       curve_offset=.2, num_plates=10, ocean_level=1.0,
                       step=Step.full(), sea_level=0.65, erosion_period=60, folding_ratio=0.02, agg_abs=1000000,
                       agg_rel=0.33, num_cycles=2):
    e_as_array, p_as_array = generate_plates_simulation(obj, seed, width, height, sea_level, erosion_period,
                                                        folding_ratio, agg_abs, agg_rel, num_cycles, num_plates)

    world = modWorld.World(name, modWorld.Size(width, height), seed,
                           modWorld.GenerationParameters(num_plates, ocean_level, step),
                           temps, humids, gamma_curve, curve_offset)
    world.set_elevation(numpy.array(e_as_array).reshape(height, width), None)
    world.set_plates(numpy.array(p_as_array, dtype=numpy.uint16).reshape(height, width))

    return world


def world_gen(obj, name, width, height, seed, temps=[.874, .765, .594, .439, .366, .124],
              humids=[.941, .778, .507, .236, 0.073, .014, .002], num_plates=10,
              ocean_level=1.0, step=Step.full(), gamma_curve=1.25, curve_offset=.2,
              fade_borders=True, sea_level=0.65, erosion_period=60, folding_ratio=0.02, agg_abs=1000000,
              agg_rel=0.33, num_cycles=2, erosion_curve1=0.0, erosion_curve2=0.0, erosion_curve3=0.0,
              erosion_max_radius=0, erosion_maxRadius=0, erosion_radius=0, humidity_irrigationWeight=0.0, humidity_precipitation_weight=0.0,
              hydrology_creek=0.0, hydrology_main_river=0.0, hydrology_river=0.0, irrigation_radius=0,
              icecap_freeze_chance_window=0.0, icecap_max_freeze_percentage=0.0, icecap_surrounding_tile_influence=0.0,
              permeability_freq=0.0, permeability_octaves=0, permeability_perm_th_low=0.0, permeability_perm_th_med=0.0,
              precipitation_freq=0.0, precipitation_octaves=0, precipitation_ths_low=0.0, precipitation_ths_med=0.0,
              temperature_axial_tilt_hwhm=0.0, temperature_distance_to_sun_hwhm=0.0, temperature_frequency=0.0, temperature_octaves=0,
              wind_frequency=0.0, wind_octaves=0):
        
    verbose = get_verbose()
    
    if verbose:
        start_time = time.time()
        obj.updatePopup(' ')
        obj.updatePopup('Generating Plates ...')

    world = _plates_simulation(obj, name, width, height, seed, temps, humids, gamma_curve, curve_offset, num_plates,
                               ocean_level, step, sea_level, erosion_period, folding_ratio, agg_abs, agg_rel,num_cycles)

    center_land(world)
        
    if verbose:
        elapsed_time = time.time() - start_time
        obj.updatePopup('    Plates Simulation completed in %s seconds' % str(format(elapsed_time, '.4f')))
        start_time = time.time()
    
    add_noise_to_elevation(world, numpy.random.randint(0, 4096))  # uses the global RNG; this is the very first call to said RNG - should that change, this needs to be taken care of
    
    if verbose:
        elapsed_time = time.time() - start_time        
        obj.updatePopup('    Elevation Noise added in %s seconds' % str(format(elapsed_time, '.4f')))
        start_time = time.time()
    
    if fade_borders:
        place_oceans_at_map_borders(world)
    
    initialize_ocean_and_thresholds(world)

    if verbose:
        elapsed_time = time.time() - start_time
        obj.updatePopup('    Oceans initialised in %s seconds' % str(format(elapsed_time, '.4f')))

    return generate_world(obj, world, step, erosion_curve1, erosion_curve2, erosion_curve3,
                          erosion_max_radius, erosion_maxRadius, erosion_radius,
                          humidity_irrigationWeight, humidity_precipitation_weight,
                          hydrology_creek, hydrology_main_river, hydrology_river, irrigation_radius,
                          icecap_freeze_chance_window, icecap_max_freeze_percentage, icecap_surrounding_tile_influence,
                          permeability_freq, permeability_octaves, permeability_perm_th_low, permeability_perm_th_med,
                          precipitation_freq, precipitation_octaves, precipitation_ths_low, precipitation_ths_med,
                          temperature_axial_tilt_hwhm, temperature_distance_to_sun_hwhm, temperature_frequency, temperature_octaves,
                          wind_frequency, wind_octaves)
