import numpy as np 
import matplotlib.pyplot as plt 
import math

from scipy.spatial import cKDTree 

def read_data(name):
    f = open(name) 
    ret = []
    for line in f.xreadlines():
        ret.append([float(z) for z in line.split()])
    return ret

def to_cartesian(spher_arr):
    arr = []
    for ele in spher_arr:
        x = ele[2] * math.sin(math.radians(ele[1])) * math.cos(math.radians(ele[0]))
        y = ele[2] * math.sin(math.radians(ele[1])) * math.sin(math.radians(ele[0]))
        z = ele[2] * math.cos(math.radians(ele[1]))
        arr.append([x, y, z])
    return arr

def read_data_spherical(name):
    data = [[x[0], 90-x[1], x[2]*3000.0] for x in read_data(name)]
    return to_cartesian(data)

# remember that log_bins includes the .1 in it.
# Take the last 15 in actuality
log_bins_aug = np.linspace(-1.0, 1.301, num=16)
log_bins = log_bins_aug[-15:]
bins = [10 ** x for x in log_bins_aug]

def pairs_count(ckd, r): 
    return ckd.count_neighbors(ckd, r) 

def pairs_arr(ckd):
    arr = []
    #countneighbors includes single points, but it taken care of in subtracting below
    for x in bins:
        arr.append(pairs_count(ckd, x))
    for x in range(len(arr) - 1, 0, -1):
        arr[x] = (arr[x] - arr[x - 1]) / 2
    return arr[-15:]


# takes all within rather than all near r
def correlation(n, r, NN, RR):
    ratio = r / float(n)
    pairs_ratio = NN / float(RR)
    return (ratio * ratio) * pairs_ratio - 1

def correlation_plot(ckd, rand, num_rand):
    data = pairs_arr(ckd)
    n = ckd.n
    return [correlation(n, num_rand, x, y) for (x,y) in zip(data, rand)]

def log_arr(arr): 
    return [np.log10(x) for x in arr]

# BEGIN PART 1 STUFF

part1_names = ["SDSS_Mr21_rspace.dat", "SDSS_Mr20_rspace.dat", "SDSS_Mr20_zspace.dat"] 

def part1():
    random_points = read_data_spherical("SDSS_random.dat")
    random_pairs = pairs_arr(cKDTree(random_points))
    coords = [read_data_spherical(x) for x in part1_names]
    data = [correlation_plot(cKDTree(x), random_pairs, len(random_points)) for x in coords]

    plt.plot(log_bins, log_arr(data[0]))
    plt.plot(log_bins, log_arr(data[1]))
    plt.savefig('plot_a.png')
    plt.close()

    plt.plot(log_bins, log_arr(data[1]))
    plt.plot(log_bins, log_arr(data[2]))
    plt.savefig('plot_b.png')
    plt.close()

    return data


# BEGIN PART 2 STUFF
def bias_plot(gal, dm):
    return [np.sqrt(x / y) for (x, y) in zip(gal, dm)]

def part2(part1Data):
    ckd = cKDTree(read_data("DM.dat"))
    random_ckd = cKDTree(read_data("DM_random.dat"))
    print(pairs_arr(ckd))
    print(pairs_arr(random_ckd))
    print(ckd.n)
    print(random_ckd.n)
    dm_plot = correlation_plot(ckd, pairs_arr(random_ckd), random_ckd.n)

    bias21 = bias_plot(part1Data[0], dm_plot)
    bias20 = bias_plot(part1Data[1], dm_plot)

    plt.plot(log_bins, bias21)
    plt.plot(log_bins, bias20)
    plt.savefig('plot_c.png')
    plt.close()

def main(): 
    data = part1()
    part2(data)

if __name__ == '__main__':
    main()
