import numpy


class IrrigationSimulation(object):
    @staticmethod
    def is_applicable(world):
        return world.has_watermap() and (not world.has_irrigation())

    def execute(self, world, seed, irrigation_radius):
        world.set_irrigation(self._calculate(self, world, irrigation_radius))

    @staticmethod
    def _calculate(self, world, irrigation_radius):
        # Notes on performance:
        #  -method is run once per generation
        #  -iterations        : width * height
        #  -memory consumption: width * height * sizeof(numpy.float) (permanent)

        width = world.width
        height = world.height
        self.radius = irrigation_radius

        # create array of pre-calculated values -> less calculations
        d = numpy.arange(-self.radius, self.radius + 1, 1, dtype=float)
        x, y = numpy.meshgrid(d, d)  # x/y distances to array center
        # calculate final matrix: ln(sqrt(x^2+y^2) + 1) + 1
        logs = numpy.log1p(numpy.sqrt(numpy.square(x) + numpy.square(y))) + 1

        # create output array
        values = numpy.zeros((height, width), dtype=float)
        it_all = numpy.nditer(values, flags=['multi_index'], op_flags=['readonly'])

        while not it_all.finished:
            x = it_all.multi_index[1]
            y = it_all.multi_index[0]
            if world.is_ocean((x, y)):
                # coordinates used for the values-slice (tl = top-left etc.)
                tl_v = (max(x - self.radius, 0), max(y - self.radius, 0))
                br_v = (min(x + self.radius, width - 1), min(y + self.radius, height - 1))
                # coordinates used for the logs-slice
                tl_l = (max(self.radius - x, 0), max(self.radius - y, 0))
                br_l = (
                    min(self.radius - x + width - 1, 2 * self.radius),
                    min(self.radius - y + height - 1, 2 * self.radius))

                # extract the necessary parts of the arrays
                logs_relevant = logs[tl_l[1]:br_l[1] + 1, tl_l[0]:br_l[0] + 1]

                # finish calculation
                values[tl_v[1]:br_v[1] + 1, tl_v[0]:br_v[0] + 1] += world.layers['watermap'].data[y, x] / logs_relevant

            it_all.iternext()

        return values
