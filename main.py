import numpy as np
from read_file import *
from model import *
from plot import *
import matplotlib.pyplot as plt


max_w = 10


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(g, block_ids, dest_cbgs):
    # setting thresholds
    thresholds = np.arange(0, max_w, 0.1)

    num_g = []
    num_sg = []
    for i in thresholds:
        tmp_g, tmp_sg = num_g_sg(generate_network_threshold(g, i))
        num_g.append(tmp_g)
        num_sg.append(tmp_sg)

    return thresholds, num_g, num_sg


'''
This function is to find the bottleneck by analyzing the threshold around when the second SCC is the largest
'''


def calc_bottleneck(g, dest_cbgs, num_sg):
    max_index = [i for i, j in enumerate(num_sg) if j == max(num_sg)][0]

    G_sg_largest = generate_network_threshold(g, max_index)
    G_b_sg_largest = generate_network_threshold(g, max_index-1)

    G_sg_largest.sort(key=lambda a: len(a))
    scc_sg_largest = G_sg_largest[-1]
    scc_sg_s_largest = G_sg_largest[-2]

    for i, j in dest_cbgs.keys():
        if dest_cbgs[(i, j)] == max_index:
            if (i in scc_sg_largest and j in scc_sg_s_largest) or (j in scc_sg_largest and i in scc_sg_s_largest):
                return i, j

    return None


'''
This function is to generate file names with multiple dates
'''


def generate_file_name(num):
    names = []
    for i in range(1, num+1):
        tmp = 'data/04/0'+str(i)+'/2020-04-0'+str(i)+'-social-distancing.csv.gz'
        names.append(tmp)

    return names


def main(file, state_id):
    block_ids, dest_cbgs = read_files(path, state_id)
    G = generate_network(block_ids, dest_cbgs)
    thresholds, num_g, num_sg = calc_g_sg(G, block_ids, dest_cbgs)
    plot_g_sg(thresholds, num_g, num_sg)

    return


if __name__ == '__main__':
    state_id = 36
    path = generate_file_name(7)
    main(path, state_id)
    # files = generate_file_name(7)
    # block_ids, dest_cbgs = read_files(files, 36)
    # g = generate_network(block_ids, dest_cbgs)
    # plot_hist(g)
