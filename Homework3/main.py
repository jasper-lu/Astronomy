import numpy as np 
import matplotlib.pyplot as plt 
import math

from scipy.spatial import cKDTree 
def read_data(name):
    f = open(name)
    ret = []
    for line in f.xreadlines():
        x, y, z = [float(z) for z in line.split()]
        ret.append([x, 90 - y, z * 3000.0])
    return ret

def to_cartesian(spher_arr):
    arr = []
    for ele in spher_arr:
        x = ele[2] * math.sin(math.radians(ele[1])) * math.cos(math.radians(ele[0]))
        y = ele[2] * math.sin(math.radians(ele[1])) * math.sin(math.radians(ele[0]))
        z = ele[2] * math.cos(math.radians(ele[1]))
        arr.append([x, y, z])
    return arr

random_points = to_cartesian(read_data("SDSS_random.dat"))

random_size = len(random_points)
random_kd = cKDTree(random_points)

base_r = 10** (-1 - 2.301/14)
log_bins = np.linspace(-1.0, 1.301, num=15)
bins = [10 ** x for x in log_bins]

print("created log bins")

def pairs_count(ckd, r): 
    return ckd.count_neighbors(ckd, r) 

def pairs_arr(ckd):
    arr = []
    base_count = pairs_count(ckd, base_r)
    for x in bins:
        arr.append(pairs_count(ckd, x))
    print(arr)
    for x in range(len(arr) - 1, 0, -1):
        arr[x] = (arr[x] - arr[x - 1]) / 2
    print(base_count)
    arr[0] = (arr[0] - base_count) / 2

    return arr

random_pairs = pairs_arr(random_kd)

# takes all within rather than all near r
def correlation(n, NN, RR):
    ratio = random_size / float(n)
    pairs_ratio = NN / float(RR)
    return (ratio * ratio) * pairs_ratio - 1

def correlation_plot(ckd):
    data = pairs_arr(ckd)
    n = ckd.n
    print(data)
    return [correlation(n, x, y) for (x,y) in zip(data, random_pairs)]

print("before mr21 data")
mr21_r_data = to_cartesian(read_data("SDSS_Mr21_rspace.dat"))
print("before mr21 ckd")
mr21_r_ckd = cKDTree(mr21_r_data)
print("before mr21 correlationPlot")
mr21_r_corr = correlation_plot(mr21_r_ckd)

print("before mr20 data")
mr20_r_data = to_cartesian(read_data("SDSS_Mr20_rspace.dat"))
print("before mr20 ckd")
mr20_r_ckd = cKDTree(mr20_r_data)
print("before mr20 corr")
mr20_r_corr = correlation_plot(mr20_r_ckd)

mr20_z_data = to_cartesian(read_data("SDSS_Mr20_zspace.dat"))
mr20_z_ckd = cKDTree(mr20_z_data)
mr20_z_corr = correlation_plot(mr20_z_ckd)

def log_arr(arr): 
    return [np.log10(x) for x in arr]

print(mr21_r_corr)

plt.plot(log_bins, log_arr(mr21_r_corr))
plt.plot(log_bins, log_arr(mr20_r_corr))
plt.show()
