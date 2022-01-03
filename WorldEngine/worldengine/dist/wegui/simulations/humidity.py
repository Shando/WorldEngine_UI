import simulations.basic as basic
import numpy

class HumiditySimulation(object):
    @staticmethod
    def is_applicable(world):
        return world.has_precipitations() and world.has_irrigation() and (not world.has_humidity())

    def execute(self, world, seed, irrigationWeight, precipitationWeight):
        assert seed is not None
        data, quantiles = self._calculate(world, irrigationWeight, precipitationWeight)
        world.set_humidity(data, quantiles)

        return world

    @staticmethod
    def _calculate(world, irrigationWeight, precipitationWeight):
        humids = world.humids
        data = numpy.zeros((world.height, world.width), dtype=float)
        data = ((world.layers['precipitation'].data * precipitationWeight) - (world.layers['irrigation'].data * irrigationWeight)) / (precipitationWeight + irrigationWeight)

        # These were originally evenly spaced at 12.5% each but changing them
        # to a bell curve produced better results
        ocean = world.layers['ocean'].data
        quantiles = {'12': basic.find_threshold_f(data, humids[6], ocean),
                     '25': basic.find_threshold_f(data, humids[5], ocean),
                     '37': basic.find_threshold_f(data, humids[4], ocean),
                     '50': basic.find_threshold_f(data, humids[3], ocean),
                     '62': basic.find_threshold_f(data, humids[2], ocean),
                     '75': basic.find_threshold_f(data, humids[1], ocean),
                     '87': basic.find_threshold_f(data, humids[0], ocean)}

        return data, quantiles
