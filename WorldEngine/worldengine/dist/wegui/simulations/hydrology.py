import simulations.basic as basic
import numpy

class WatermapSimulation(object):
    @staticmethod
    def is_applicable(world):
        return world.has_precipitations() and (not world.has_watermap())

    def execute(self, world, seed, hydrology_creek, hydrology_main_river, hydrology_river):
        assert seed is not None
        self.creek = hydrology_creek
        self.main_river = hydrology_main_river
        self.river = hydrology_river
        data, thresholds = self._watermap(self, world, 20000)
        world.set_watermap(data, thresholds)

        return world

    @staticmethod
    def _watermap(self, world, n):
        def droplet(in_world, pos, q, _watermap):
            if q < 0:
                return

            x, y = pos
            pos_elev = in_world.layers['elevation'].data[y, x] + _watermap[y, x]
            lowers = []
            min_higher = None
            min_lower = None
            tot_lowers = 0

            for p in in_world.tiles_around((x, y)):
                px, py = p
                e = in_world.layers['elevation'].data[py, px] + _watermap[py, px]

                if e < pos_elev:
                    dq = int(pos_elev - e) << 2
                    if min_lower is None or e < min_lower:
                        min_lower = e

                        if dq == 0:
                            dq = 1

                    lowers.append((dq, p))
                    tot_lowers += dq
                else:
                    if min_higher is None or e > min_higher:
                        min_higher = e
                        # pos_min_higher = p

            if lowers:
                f = q / tot_lowers

                for l in lowers:
                    s, p = l

                    if not in_world.is_ocean(p):
                        px, py = p
                        ql = f * s
                        # ql = q
                        going = ql > 0.05
                        _watermap[py, px] += ql

                        if going:
                            droplet(world, p, ql, _watermap)
            else:
                _watermap[y, x] += q

        _watermap_data = numpy.zeros((world.height, world.width), dtype=float)

        for i in range(n):
            x, y = world.random_land()  # will return None for x and y if no land exists

            if x is not None and world.precipitations_at((x, y)) > 0:
                droplet(world, (x, y), world.precipitations_at((x, y)), _watermap_data)

        ocean = world.layers['ocean'].data
        thresholds = dict()
        thresholds['creek'] = basic.find_threshold_f(_watermap_data, self.creek, ocean=ocean)
        thresholds['river'] = basic.find_threshold_f(_watermap_data, self.river, ocean=ocean)
        thresholds['main river'] = basic.find_threshold_f(_watermap_data, self.main_river, ocean=ocean)

        return _watermap_data, thresholds
