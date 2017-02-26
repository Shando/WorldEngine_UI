import simulations.basic as basic
import noise
import numpy

class PermeabilitySimulation(object):
    @staticmethod
    def is_applicable(world):
        return not world.has_permeability()

    def execute(self, world, seed, perm_freq, perm_oct, perm_th_low, perm_th_med):
        self.frequency = perm_freq
        self.octaves = perm_oct
        perm = self._calculate(self, seed, world.width, world.height)
        ocean = world.layers['ocean'].data
        perm_th = [
            ('low', basic.find_threshold_f(perm, perm_th_low, ocean)),
            ('med', basic.find_threshold_f(perm, perm_th_med, ocean)),
            ('hig', None)
        ]
        world.set_permeability(perm, perm_th)

    @staticmethod
    def _calculate(self, seed, width, height):
        rng = numpy.random.RandomState(seed)  # create our own random generator
        base = rng.randint(0, 4096)
        perm = numpy.zeros((height, width), dtype=float)
        freq = self.frequency * self.octaves

        for y in range(0, height):#TODO: numpy optimization?
            # yscaled = float(y) / height  # TODO: what is this?
            for x in range(0, width):
                n = noise.snoise2(x / freq, y / freq, self.octaves, base=base)
                perm[y, x] = n

        return perm
