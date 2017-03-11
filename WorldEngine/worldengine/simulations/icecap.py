import numpy


class IcecapSimulation(object):
    # This class creates an "ice-map", i.e. a numpy array with positive values that describe the thickness of the ice at
    # a certain spot of the world.
    # Ice can appear wherever there is an ocean and the temperature is cold enough.

    @staticmethod
    def is_applicable(world):
        return world.has_ocean() and world.has_temperature()

    def execute(self, world, seed, freeze_chance_window, max_freeze_percentage, surrounding_tile_influence):
        self.fcw = freeze_chance_window
        self.mfp = max_freeze_percentage
        self.sti = surrounding_tile_influence
        world.set_icecap(self._calculate(self, world, seed))

        return world

    @staticmethod
    def _calculate(self, world, seed):
        # Notes on performance:
        #  -method is run once per generation
        #  -iterations        : width * height
        #  -memory consumption: width * height * sizeof(numpy.float) (permanent)
        #                       width * height * sizeof(numpy.bool) (temporary)

        # constants for convenience (or performance)
        ocean = world.layers['ocean'].data
        temperature = world.layers['temperature'].data

        # primary constants (could be used as global variables at some point); all values should be in [0, 1]
        # self.mfp  # only the coldest x% of the cold area will freeze (0 = no ice, 1 = all ice)
        # self.fcw  # the warmest x% of freezable area won't completely freeze (RNG decides)
        # self.sti  # chance-modifier to freeze a slightly warm tile when neighbors are frozen

        # secondary constants
        temp_min = temperature.min()  # coldest spot in the world
        # upper temperature-limit for freezing effects
        freeze_threshold = world.layers['temperature'].thresholds[2][1]

        # derived constants
        freeze_threshold = (freeze_threshold - temp_min) * self.mfp  # calculate freeze threshold above min
        freeze_chance_threshold = freeze_threshold * (1.0 - self.fcw)

        # local variables
        icecap = numpy.zeros((world.height, world.width), dtype=float)
        rng = numpy.random.RandomState(seed)  # create our own random generator

        # map that is True whenever there is land or (certain) ice around
        solid_map = numpy.logical_or(temperature <= freeze_chance_threshold + temp_min, numpy.logical_not(ocean))

        for y in range(world.height):
            for x in range(world.width):
                if world.is_ocean((x, y)) or world.river_map[y, x] > 0 or world.lake_map[y, x] > 0\
                        or world.watermap['data'][y, x] > 0:
                    t = temperature[y, x]

                    if t - temp_min < freeze_threshold:
                        # map temperature to freeze-chance (linear interpolation)
                        chance = numpy.interp(t, [temp_min, freeze_chance_threshold, freeze_threshold], [1.0, 1.0, 0.0])
                        # *will* freeze for temp_min <= t <= freeze_chance_threshold
                        # *can* freeze for freeze_chance_threshold < t < freeze_threshold

                        # count number of frozen/solid tiles around this one
                        if 0 < x < world.width - 1 and 0 < y < world.height - 1:  # exclude borders
                            surr_tiles = solid_map[y - 1:y + 2, x - 1:x + 2]
                            chance_mod = numpy.count_nonzero(surr_tiles)
                            chance_mod -= 1 if solid_map[y, x] else 0  # remove center-tile (i.e. the current tile)

                            # map amount of tiles to chance-modifier, [-1.0, 1.0]
                            chance_mod = numpy.interp(chance_mod, [0, surr_tiles.size - 1], [-1.0, 1.0])
                            chance += chance_mod * self.sti

                        if rng.rand() <= chance:  # always freeze for chance >= 1.0, never for <= 0.0
                            solid_map[y, x] = True  # mark tile as frozen
                            icecap[y, x] = freeze_threshold - (t - temp_min)  # thickness of the ice (arbitrary scale)

        return icecap
