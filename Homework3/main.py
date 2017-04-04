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

def pairs_fix(arr):
    ret = []
    for x in range(len(arr) - 1, 0, -1):
        ret.append((arr[x] - arr[x - 1]) / 2)

    return ret[::-1]

def pairs_arr(ckd):
    arr = []
    #countneighbors includes single points, but it taken care of in subtracting below
    for x in bins:
        arr.append(pairs_count(ckd, x))
    ret = pairs_fix(arr)
    #for x in range(len(arr) - 1, 0, -1):
    #    arr[x] = (arr[x] - arr[x - 1]) / 2
    return ret[-15:]


# takes all within rather than all near r
def correlation(n, r, NN, RR):
    ratio = r / float(n)
    pairs_ratio = NN / float(RR)
    return (ratio * ratio) * pairs_ratio - 1

def calcJ3(n, r, ckd, ckd_r):
    print("Calculating J3")
    ratio = r / float(n)
    bins = np.linspace(.1,20, num=100)
    NN = [pairs_count(ckd, x) for x in bins]
    RR = [pairs_count(ckd_r, x) for x in bins]
    for x in range(len(NN) - 1, 0, -1):
        NN[x] = (NN[x] - NN[x - 1]) / 2
        RR[x] = (RR[x] - RR[x - 1]) / 2
    NN = NN[-99:]
    RR = RR[-99:]
    diff = bins[1] - bins[0]
    corr = [correlation(n, r, NN[x], RR[x]) for x in range(len(NN))]
    lower = [y * y * x * diff for (x,y) in zip(corr[1:], bins[1:])]
    upper = [y * y * x * diff for (x,y) in zip(corr[:-1], bins[:-1])]
    return 4 * np.pi * sum([(x + y) / 2 for (x,y) in zip(lower, upper)])

def correlation_plot(ckd, rand, num_rand):
    data = pairs_arr(ckd)
    print(data)
    n = ckd.n
    return [correlation(n, num_rand, x, y) for (x,y) in zip(data, rand)]

def log_arr(arr): 
    return [np.log10(x) for x in arr]

# BEGIN PART 1 STUFF

part1_names = ["SDSS_Mr21_rspace.dat", "SDSS_Mr20_rspace.dat", "SDSS_Mr20_zspace.dat"] 
part3_names = ["SDSS_Mr21_rspace.dat", "SDSS_Mr20_rspace.dat"] 

def calcMaxRad(i):
    return max([x[2]*3000.0 for x in read_data(part1_names[i])])

def errors(NN, n, j3, rad):
    print(NN)
    print(n)
    volume = (4/3 * np.pi * (rad ** 3))
    density = n / volume
    print("Density is") 
    print(density)
    return [(1 + 4*np.pi*density*j3) / np.sqrt(NN[x]) for x in range(len(NN))]

def part3():
    print("Part 3 Begin")
    random_points = read_data_spherical("SDSS_random.dat")
    random_ckd = cKDTree(random_points)
    random_pairs = pairs_arr(random_ckd)
    print(random_pairs)
    coords = [read_data_spherical(x) for x in part3_names]
    print("Read in Coordinates. Making correlation plots")
    
    ckds = [cKDTree(x) for x in coords]

    mr21 = correlation_plot(ckds[0], random_pairs, len(random_points))
    mr20 = correlation_plot(ckds[1], random_pairs, len(random_points))

    mr21_count = [pairs_count(ckds[0], r) for r in bins]
    mr20_count = [pairs_count(ckds[1], r) for r in bins]
    mr21_pairs = pairs_fix(mr21_count)
    mr20_pairs = pairs_fix(mr20_count)

    #j321 = calcJ3(ckds[0].n, random_ckd.n, ckds[0], random_ckd) 
    #j320 = calcJ3(ckds[1].n, random_ckd.n, ckds[1], random_ckd) 
    j321 = 12180.4369386
    j320 = 7569.38188017 
    print(j321)
    print(j320)
    rad21 = calcMaxRad(0)
    rad20 = calcMaxRad(1)
    print(rad21)
    print(rad20)

    mr21_error = errors(mr21_pairs, ckds[0].n, j321, rad21)
    mr20_error = errors(mr20_pairs, ckds[1].n, j320, rad20)

    print(mr21_error)
    print(mr20_error)

    plt.xscale("log", nonposx="clip")
    plt.yscale("log", nonposy="clip")
    plt.plot(bins[1::], mr21, label="Mr21")
    plt.plot(bins[1::], mr20, label="Mr20")
    plt.errorbar(bins[1::], mr21, capsize=10, yerr=mr21_error)
    plt.errorbar(bins[1::], mr20, capsize=10, yerr=mr20_error)
    plt.xlabel("log(r)")
    plt.ylabel("log(E(r))")
    plt.savefig('err_a.png')
    plt.close()

def part1():
    print("Part 1 Begin")
    random_points = read_data_spherical("SDSS_random.dat")
    random_pairs = pairs_arr(cKDTree(random_points))
    print(random_pairs)
    coords = [read_data_spherical(x) for x in part1_names]
    print("Read in Coordinates. Making correlation plots")
    ckds = [cKDTree(x) for x in coords]
    data = [correlation_plot(x, random_pairs, len(random_points)) for x in ckds]

    plt.plot(log_bins, log_arr(data[0]), label="Mr21")
    plt.plot(log_bins, log_arr(data[1]), label="Mr20")
    plt.xlabel("log(r)")
    plt.ylabel("log(E(r))")
    plt.savefig('plot_a.png')
    plt.close()

    plt.plot(log_bins, log_arr(data[1]), label = "Mr20_r")
    plt.plot(log_bins, log_arr(data[2]), label = "Mr20_z")
    plt.xlabel("log(r)")
    plt.ylabel("log(E(r))")
    plt.savefig('plot_b.png')
    plt.close()

    return data


# BEGIN PART 2 STUFF
def bias_plot(gal, dm):
    return [np.sqrt(x / y) for (x, y) in zip(gal, dm)]

def part2(part1Data):
    print("Begin part 2")
    ckd = cKDTree(read_data("DM.dat"))
    random_ckd = cKDTree(read_data("DM_random.dat"))
    print(random_ckd.n)
    print("Create corrleation plot for dark matter")
    dm_plot = correlation_plot(ckd, pairs_arr(random_ckd), random_ckd.n)

    bias21 = bias_plot(part1Data[0], dm_plot)
    bias20 = bias_plot(part1Data[1], dm_plot)

    plt.plot(log_bins, bias21, label="Mr21")
    plt.plot(log_bins, bias20, label="Mr20")
    plt.xlabel("log(r)")
    plt.ylabel("b(E(r))")
    plt.savefig('plot_c.png')
    plt.close()

def main(): 
    data = part1()
    #part2(data)
    part3()

if __name__ == '__main__':
    main()
