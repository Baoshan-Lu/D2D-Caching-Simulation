import matplotlib.pyplot as plt


def plot_cache_hits(self_hits, d2d_hits, bs_hits, sat_hits, universal, interval):
    plt.plot(self_hits)     # self cache hit
    plt.plot(d2d_hits)    # d2d cache hit
    plt.plot(bs_hits)    # base station cache hit
    plt.plot(sat_hits)    # satellite cache hit
    plt.plot(universal)    # get from universal resource


    plt.xlabel('zipf parameter')
    plt.ylabel('cache hit ratio')

    plt.xticks([0,1,2,3,4], interval)
    plt.legend(['self cache hits', 'd2d cache hits', 'bs cache hit', 'satellite cache hit', 'cache miss'], loc='upper right')

    plt.show()
