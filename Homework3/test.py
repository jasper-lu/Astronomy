import numpy as np
from scipy.spatial import cKDTree
import pylab
import math
import scipy.spatial as spatial
import matplotlib.pyplot as plt


def main():
    bins = []
    log_r_arr = []
    log_binWidth = (1.301 - (-1)) / 15
    log_binWidthBase = -1 + log_binWidth
    for element in range(15):
        log_r_arr.append(log_binWidthBase)
        binWithbase = 10 ** log_binWidthBase
        log_binWidthBase = log_binWidthBase + log_binWidth
        bins.append(binWithbase)

    data_mr20_rspace = []
    data_mr20_zspace = []
    data_mr21_rspace = []
    data_random = []
    mr20_zspace_count = 0
    mr20_rspace_count = 0
    mr21_rspace_count = 0
    random_count = 0
    with open("SDSS_Mr21_rspace.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, 90 - n2, n3 * 300000.0 / 100.0]
            data_mr21_rspace.append(row)
            mr21_rspace_count += 1
    with open("SDSS_Mr20_rspace.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, 90 - n2, n3 * 300000.0 / 100.0]
            data_mr20_rspace.append(row)
            mr20_rspace_count += 1
    with open("SDSS_Mr20_zspace.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, 90 - n2, n3 * 300000.0 / 100.0]
            data_mr20_zspace.append(row)
            mr20_zspace_count += 1
    with open("SDSS_random.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, 90 - n2, n3 * 300000.0 / 100.0]
            data_random.append(row)
            random_count += 1

    mr20_rspace_coordinates = []
    for element in range(len(data_mr20_rspace)):
        x = data_mr20_rspace[element][2] * math.sin(math.radians(data_mr20_rspace[element][1])) * math.cos(
            math.radians(data_mr20_rspace[element][0]))
        y = data_mr20_rspace[element][2] * math.sin(math.radians(data_mr20_rspace[element][1])) * math.sin(
            math.radians(data_mr20_rspace[element][0]))
        z = data_mr20_rspace[element][2] * math.cos(math.radians(data_mr20_rspace[element][1]))
        mr20_rspace_coordinates.append([x, y, z])

    mr20_zspace_coordinates = []
    for element in range(len(data_mr20_zspace)):
        x = data_mr20_zspace[element][2] * math.sin(math.radians(data_mr20_zspace[element][1])) * math.cos(
            math.radians(data_mr20_zspace[element][0]))
        y = data_mr20_zspace[element][2] * math.sin(math.radians(data_mr20_zspace[element][1])) * math.sin(
            math.radians(data_mr20_zspace[element][0]))
        z = data_mr20_zspace[element][2] * math.cos(math.radians(data_mr20_zspace[element][1]))
        mr20_zspace_coordinates.append([x, y, z])

    mr21_rspace_coordinates = []
    for element in range(len(data_mr21_rspace)):
        x = data_mr21_rspace[element][2] * math.sin(math.radians(data_mr21_rspace[element][1])) * math.cos(
            math.radians(data_mr21_rspace[element][0]))
        y = data_mr21_rspace[element][2] * math.sin(math.radians(data_mr21_rspace[element][1])) * math.sin(
            math.radians(data_mr21_rspace[element][0]))
        z = data_mr21_rspace[element][2] * math.cos(math.radians(data_mr21_rspace[element][1]))
        mr21_rspace_coordinates.append([x, y, z])

    random_coordinates = []
    for element in range(len(data_random)):
        x = data_random[element][2] * math.sin(math.radians(data_random[element][1])) * math.cos(
            math.radians(data_random[element][0]))
        y = data_random[element][2] * math.sin(math.radians(data_random[element][1])) * math.sin(
            math.radians(data_random[element][0]))
        z = data_random[element][2] * math.cos(math.radians(data_random[element][1]))
        random_coordinates.append([x, y, z])

    point_tree_mr_20_r = cKDTree(mr20_rspace_coordinates)
    base_bin_mr_20_r = point_tree_mr_20_r.count_neighbors(point_tree_mr_20_r, 0.1)
    mr20_rspace_bin_count = []
    for element in range(len(bins)):
        mr20_rspace_bin_count.append(point_tree_mr_20_r.count_neighbors(point_tree_mr_20_r, bins[element]))
    for element in range(len(mr20_rspace_bin_count) - 1, 0, -1):
        mr20_rspace_bin_count[element] = (mr20_rspace_bin_count[element] - mr20_rspace_bin_count[element - 1]) / 2
    mr20_rspace_bin_count[0] = (mr20_rspace_bin_count[0] - base_bin_mr_20_r) / 2
    print("mr20_rspace_bin: " + str(mr20_rspace_bin_count))

    point_tree_mr_20_z = cKDTree(mr20_zspace_coordinates)
    base_bin_mr_20_z = point_tree_mr_20_z.count_neighbors(point_tree_mr_20_z, 0.1)
    mr20_zspace_bin_count = []
    for element in range(len(bins)):
        mr20_zspace_bin_count.append(point_tree_mr_20_z.count_neighbors(point_tree_mr_20_z, bins[element]))
    for element in range(len(mr20_zspace_bin_count) - 1, 0, -1):
        mr20_zspace_bin_count[element] = (mr20_zspace_bin_count[element] - mr20_zspace_bin_count[element - 1]) / 2
    mr20_zspace_bin_count[0] = (mr20_zspace_bin_count[0] - base_bin_mr_20_z) / 2
    print("mr20_zspace_bin: " + str(mr20_zspace_bin_count))

    point_tree_mr_21_r = cKDTree(mr21_rspace_coordinates)
    base_bin_mr_21_r = point_tree_mr_21_r.count_neighbors(point_tree_mr_21_r, 0.1)
    mr21_rspace_bin_count = []
    for element in range(len(bins)):
        mr21_rspace_bin_count.append(point_tree_mr_21_r.count_neighbors(point_tree_mr_21_r, bins[element]))
    for element in range(len(mr21_rspace_bin_count) - 1, 0, -1):
        mr21_rspace_bin_count[element] = (mr21_rspace_bin_count[element] - mr21_rspace_bin_count[element - 1]) / 2
    mr21_rspace_bin_count[0] = (mr21_rspace_bin_count[0] - base_bin_mr_21_r) / 2
    print("mr21_rspace_bin: " + str(mr21_rspace_bin_count))

    point_tree_random = cKDTree(random_coordinates)
    base_bin_random = point_tree_random.count_neighbors(point_tree_random, 0.1)
    print(base_bin_random)
    random_bin_count = []

    for element in range(len(bins)):
        random_bin_count.append(point_tree_random.count_neighbors(point_tree_random, bins[element]))
    for element in range(len(random_bin_count) - 1, 0, -1):
        random_bin_count[element] = (random_bin_count[element] - random_bin_count[element - 1]) / 2
    random_bin_count[0] = (random_bin_count[0] - base_bin_random) / 2
    print("random_bin: " + str(random_bin_count))

    corr_mr20_r = correlation_function(random_count, mr20_rspace_count,
                                       mr20_rspace_bin_count, random_bin_count)
    corr_mr20_z = correlation_function(random_count, mr20_zspace_count,
                                       mr20_zspace_bin_count, random_bin_count)
    corr_mr21_r = correlation_function(random_count, mr21_rspace_count,
                                       mr21_rspace_bin_count, random_bin_count)

    # take log
    # for element in range(len(corr_mr20_r)):
    #     corr_mr20_r[element] = math.log(corr_mr20_r[element], 10)
    #
    # for element in range(len(corr_mr21_r)):
    #     corr_mr21_r[element] = math.log(corr_mr21_r[element], 10)
    #
    # for element in range(len(corr_mr20_z)):
    #     corr_mr20_z[element] = math.log(corr_mr20_z[element], 10)

    # Mr < -20 and Mr < -21 r
    # correlation_function_mr21, = plt.plot(log_r_arr, corr_mr21_r)
    # correlation_function_mr20r, = plt.plot(log_r_arr, corr_mr20_r)
    # plt.legend([correlation_function_mr21, correlation_function_mr20r], ['mr21', 'mr20'])
    # plt.ylabel('log (r)')
    # plt.xlabel('logr')
    # plt.show()

    # # Mr < -20 z and Mr < -20 r
    # correlation_function_mr20z, = plt.plot(log_r_arr, corr_mr20_z)
    # correlation_function_mr20r, =  plt.plot(log_r_arr, corr_mr20_r)
    # plt.legend([correlation_function_mr20z, correlation_function_mr20r], ['mr20z', 'mr20r'])
    # plt.xlabel('logr')
    # plt.show()

    data_DM = []
    data_DM_random = []
    DM_count = 0
    DM_random_count = 0

    with open("DM.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, n2, n3]
            data_DM.append(row)
            DM_count += 1

    with open("DM_random.dat") as fileIn:
        for line in fileIn:
            n1, n2, n3 = (float(s) for s in line.split())
            row = [n1, n2, n3]
            data_DM_random.append(row)
            DM_random_count += 1

    point_tree_DM = cKDTree(data_DM)
    base_bin_DM = point_tree_DM.count_neighbors(point_tree_DM, 0.1)
    DM_bin_count = []
    for element in range(len(bins)):
        DM_bin_count.append(point_tree_DM.count_neighbors(point_tree_DM, bins[element]))
    for element in range(len(DM_bin_count) - 1, 0, -1):
        DM_bin_count[element] = (DM_bin_count[element] - DM_bin_count[element - 1]) / 2
    DM_bin_count[0] = (DM_bin_count[0] - base_bin_DM) / 2
    print("DM_bin: " + str(DM_bin_count))

    point_tree_DM_random = cKDTree(data_DM_random)
    base_bin_DM_random = point_tree_DM_random.count_neighbors(point_tree_DM_random, 0.1)
    DM_random_bin_count = []
    for element in range(len(bins)):
        DM_random_bin_count.append(point_tree_DM_random.count_neighbors(point_tree_DM_random, bins[element]))
    for element in range(len(DM_random_bin_count) - 1, 0, -1):
        DM_random_bin_count[element] = (DM_random_bin_count[element] - DM_random_bin_count[element - 1]) / 2
    DM_random_bin_count[0] = (DM_random_bin_count[0] - base_bin_DM_random) / 2
    print("DM_random_bin: " + str(DM_random_bin_count))

    corr_DM = correlation_function(DM_random_count, DM_count, DM_bin_count, DM_random_bin_count)

    b_mr20 = []
    for element in range(len(corr_DM)):
        value = (corr_mr20_r[element] / corr_DM[element]) ** (1 / 2)
        b_mr20.append(value)

    b_mr21 = []
    for element in range(len(corr_DM)):
        value = (corr_mr21_r[element] / corr_DM[element]) ** (1 / 2)
        b_mr21.append(value)

    # Mr < -20 and Mr < -21 bias function plots
    bias_function_mr21, = plt.plot(log_r_arr, b_mr21)
    bias_function_mr20, =  plt.plot(log_r_arr, b_mr20)
    plt.legend([bias_function_mr21, bias_function_mr20], ['bias function mr21', 'bias function mr20'])
    plt.show()


def correlation_function(random_count, data_count, data_arr, random_arr):
    result = []
    for element in range(len(data_arr)):
        result.append(((random_count / data_count) ** 2.0) * (data_arr[element]
                                                              / random_arr[element]) - 1)
    return result

if __name__ == '__main__':
    main()





