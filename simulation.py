import terrain
import device
import content
import random
import plotter

from parameters import *


class Simulator:

    def __init__(self):
        self.terrestrial = terrain.Terrain(TERRAIN_SIZE)
        self.num_contents_intervals = [50, 500, 5000, 50000, 500000]

        self.place_base_station()
        self.place_satellite()
        self.place_mobiles()

        # Generate content with zipf distribution
        self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, ZIPF_PARAMETER)


    def place_base_station(self):
        base_station = device.BaseStation(BASE_STATION_CACHE_CAPACITY, "LRU", BASE_STATION_RANGE)
        base_station.x = int(TERRAIN_SIZE / 2)
        base_station.y = int(TERRAIN_SIZE / 2)  # Located in center of terrain
        self.terrestrial.add_base_station(base_station)

    def place_satellite(self):
        satellite = device.Satellite(SATELLITE_CACHE_CAPACITY, "LRU", SATELLITE_DISTANCE)
        self.terrestrial.add_satellite(satellite)

    def place_mobiles(self):
        for i in range(NUMBER_OF_USERS):
            new_mobile = device.Mobile(i, MOBILE_CACHE_CAPACITY, "LRU", MOBILE_RANGE)
            new_mobile.x = random.randint(0, TERRAIN_SIZE - 1)  # x coordinate
            new_mobile.y = random.randint(0, TERRAIN_SIZE - 1)  # y coordinate
            self.terrestrial.add_mobile(new_mobile)


    def request_contents_randomly(self):
        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []
        for i in range(len(self.contents)):
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, self.contents[i])

            if i+1 in self.num_contents_intervals:
                self_hits.append(self.terrestrial.self_hit / i)
                d2d_hits.append(self.terrestrial.d2d_hit / i)
                bs_hits.append(self.terrestrial.bs_hit / i)
                sat_hits.append(self.terrestrial.sat_hit / i)
                universal.append(self.terrestrial.miss / i)

        plotter.plot_cache_hits(self_hits, d2d_hits, bs_hits, sat_hits, universal, self.num_contents_intervals)

    def request_contents_randomly_zipf(self):
        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []
        zipf = [1.2, 1.4, 1.6, 1.8, 2.0]
        for value in zipf:
            self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, value)
            for i in range(len(self.contents)):
                user = random.choice(self.terrestrial.mobiles)
                self.terrestrial.content_request(user, self.contents[i])

            self_hits.append(self.terrestrial.self_hit / i)
            d2d_hits.append(self.terrestrial.d2d_hit / i)
            bs_hits.append(self.terrestrial.bs_hit / i)
            sat_hits.append(self.terrestrial.sat_hit / i)
            universal.append(self.terrestrial.miss / i)
            self.terrestrial.clear_caches()


        plotter.plot_cache_hits(self_hits, d2d_hits, bs_hits, sat_hits, universal, zipf)


    def print_cache_stats(self):
        print("Number of contents:                  {}".format(len(self.contents)))
        print("Number of self cache hits:           {}".format(self.terrestrial.self_hit))
        print("Number of d2d cache hits:            {}".format(self.terrestrial.d2d_hit))
        print("Number of base station cache hits:   {}".format(self.terrestrial.bs_hit))
        print("Number of satellite cache hits:      {}".format(self.terrestrial.sat_hit))
        print("Number of cache miss:                {}".format(self.terrestrial.miss))


    def simulate_LRU(self):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.algorithm = "LRU"
        self.terrestrial.satellite.algorithm = "LRU"

        for mobile in self.terrestrial.mobiles:
            mobile.algorithm = "LRU"

        self.request_contents_randomly_zipf()
        self.print_cache_stats()


    def simulate_MLPLRU(self):
        pass

    def simulate(self):
        self.simulate_LRU()
        # self.simulate_MLPLRU()
        # self.simulate_Cache_Me_Cache()
