import simulations.basic as basic
import numpy

class HumiditySimulation(object):
    @staticmethod
    def is_applicable(world):
        return world.has_precipitations() and world.has_irrigation() and (
            not world.has_humidity())

    def execute(self, world, seed, irrigationWeight, precipitationWeight):
        assert seed is not None
        self.irrigation_Weight = irrigationWeight
        self.precipitation_Weight = precipitationWeight
        data, quantiles = self._calculate(self, world)
        world.set_humidity(data, quantiles)

    @staticmethod
    def _calculate(self, world):
        humids = world.humids
        data = numpy.zeros((world.height, world.width), dtype=float)
        data = (world.layers['precipitation'].data * self.precipitation_Weight - world.layers['irrigation'].data * self.irrigation_Weight)/(self.precipitation_Weight + self.irrigation_Weight)

        # These were originally evenly spaced at 12.5% each but changing them
        # to a bell curve produced better results
        ocean = world.layers['ocean'].data
        quantiles = {}
        quantiles['12'] = basic.find_threshold_f(data, humids[6], ocean)
        quantiles['25'] = basic.find_threshold_f(data, humids[5], ocean)
        quantiles['37'] = basic.find_threshold_f(data, humids[4], ocean)
        quantiles['50'] = basic.find_threshold_f(data, humids[3], ocean)
        quantiles['62'] = basic.find_threshold_f(data, humids[2], ocean)
        quantiles['75'] = basic.find_threshold_f(data, humids[1], ocean)
        quantiles['87'] = basic.find_threshold_f(data, humids[0], ocean)

        return data, quantiles