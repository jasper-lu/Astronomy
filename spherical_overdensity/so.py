import numpy as np
import time
import matplotlib.pyplot as plt

from periodic_kdtree import PeriodicKDTree, PeriodicCKDTree
from memoize import Memoize


bounds = np.array([141.3, 141.3, 141.3])
N = 5
K = 200
# E = allowed deviation from K
E = 1
MSun = 1.4 * (10**10)
# SR = starting radius for finding radius of overdensity
SR = 3.0

# Read in data for the program
def read_data(name):
    f = open(name)
    ret = []
    for line in f.xreadlines():
        ret.append([float(z) for z in line.split()])
    return ret

# Returns an array of (index, local density)
def calc_local_densities(points, kd):
    def density(r):
        return 3*(N+1)/(4*np.pi*(r ** 3))
    d = []
    for x in xrange(0, len(points)):
        r = kd.query(points[x], N+1)[0][N]
        temp = density(r)
        d.append((x, temp))
    return d

# Calculates the mean density of all points
def calc_mean_density(n):
    v = bounds[0] * bounds[1] * bounds[2]
    return n / v 

def mean_density(d, mean_d):
    return d / v 

def overdensity(n, r, mean): 
    v = 4.0/3.0 * np.pi * (r ** 3)
    #print "V: %g" %v
    return (n / v) / mean 

# return (radius, neighbors at radius)
def get_radius_neighbors(point, kd, mean):
    low = 0
    high = low + SR
    r = (low + high) / 2
    # print "%g < %g < %g | to first neighbor: %g" %(low, r, high, low)
    neighbors = [[]]
    def number_neighs(r):
        neighbors[0] = kd.query_ball_point(point, r)
        return len(neighbors[0])
    def od_temp(rad):
        return overdensity(number_neighs(rad), rad, mean)
    od = Memoize(od_temp)
    # print "dens:%g, number neighs %g" %(od(low), number_neighs(low))
    while (od(r) <= K - E or od(r) >= K + E):
        if od(r) > K: # our density is too high, so increase r
            low = r
        else: # our density is too low, so decrease r 
            high = r 
        r = (low + high) / 2
        # print "%g < %g < %g" %(low, r, high)
        #print "Current overdensity is %g" %od(r)
    #print od(r)
    return (r, neighbors[0])

def mass_number_density(halos):
    max = 0
    v = bounds[0] * bounds[1] * bounds[2]
    numbers = [0] * 50 
    for halo in halos:
        i = int((np.log10(halo[2] * MSun) - 10) * 10)
        if i < 50:
            numbers[i] = numbers[i] + 1
    return [x / v for x in numbers] 

def create_mass_plot(halos, outfile_name):
    plt.yscale("log", nonposy="clip")
    plt.xscale("log", nonposy="clip")
    masses = np.logspace(10,15,50)
    nd = mass_number_density(halos)

    masses, nd = zip(*[(x,y) for (x,y) in zip(masses, nd) if y != 0])

    print masses
    print nd

    plt.plot(masses, nd)

    plt.ylabel("Number Density (log10(n))")
    plt.xlabel("log10(Mass) (Msun/h)")
    #plt.gca().set_xlim([2, len(nd)])
    plt.savefig("Number Density vs Mass")
    plt.close()    

    f = open(outfile_name, 'w') 
    for x in xrange(0, len(nd)):
        s = masses[x] + " " + nd[x]
        print >> f, s

def test(points, kd, mean):
    for x in np.arange(0, 2, .1):
        print overdensity(len(kd.query_ball_point(points[0],x)), x, mean)

def run(file_name):
    print "Reading in the data from file"
    points = read_data(file_name)
    mean_density = calc_mean_density(len(points))
    print mean_density
    
    print "Initializing cKD Tree"
    kd = PeriodicCKDTree(bounds, points)
    test(points, kd, mean_density)

    print "calculating local densities for each particle"
    t = time.time()

    local_density = calc_local_densities(points, kd)
    local_density = sorted (local_density, key=lambda tup: tup[1], reverse=True)

    in_halo = set()
    # array of tuples (center, radius, number)
    halos = []

    for tup in local_density:
        if tup[0] not in in_halo:
            #print i 
            halo = get_radius_neighbors(points[tup[0]], kd, mean_density)
            for index in halo[1]:
                in_halo.add(index)
            halos.append((points[tup[0]], halo[0], len(halo[1])))
            #print "Found halo of size %g" %(len(halo[1]))

    create_mass_plot(halos, "halos_" + file_name)
    print "Total time to run: %g" %(time.time() - t)

data_files = ["DM.dat", "DM_100k.dat", "DM_200k.dat", "DM_1M.dat", "DM_2p8M.dat", "DM_5p5M.dat"]
for x in data_files:
    run(x)

'''
print "Radius is:\t %g" % temp[0]
print "Neighbors are:" 
print temp[1]
print "Step done in: \t%g" % (time.time()-t)
'''
