import numpy as np
from read_file import *
from model import *
from plot import *
import matplotlib.pyplot as plt


max_w = 10
region_file = ''


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(g):
    # setting thresholds
    thresholds = np.arange(0, max_w, 0.25)

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


def calc_bottleneck(g, thresholds, num_sg):
    max_index = [i for i, j in enumerate(num_sg) if j == max(num_sg)][0]
    bn_weight_b = thresholds[max_index]
    interval = thresholds[1] - thresholds[0]
    bn = []

    G_sg_largest = generate_network_threshold(g, bn_weight_b)

    if type(G_sg_largest) == nx.classes.digraph.DiGraph:
        scc = list(nx.strongly_connected_components(G_sg_largest))
    else:
        scc = list(nx.connected_components(G_sg_largest))
        
    scc.sort(key=lambda a: len(a))
    scc_sg_largest = scc[-1]
    scc_sg_s_largest = scc[-2]

    for i, j in g.edges():
        if bn_weight_b - interval < g.edges[(i, j)]['weight'] <= bn_weight_b:
            if (i in scc_sg_largest and j in scc_sg_s_largest) or (j in scc_sg_largest and i in scc_sg_s_largest):
                bn.append((i, j))

    return bn, bn_weight_b


'''
This function is to generate file names with multiple dates
'''


def generate_file_name(num):
    names = []
    for i in range(1, num+1):
        tmp = 'data/01/0'+str(i)+'/2020-01-0'+str(i)+'-social-distancing.csv.gz'
        names.append(tmp)

    return names


def main(file, state_id):
    dest_cbgs = read_files(file, state_id)
    G = generate_network(dest_cbgs)
    thresholds, num_g, num_sg = calc_g_sg(G)
    plot_g_sg(thresholds, num_g, num_sg)
    # bn, bn_weight = calc_bottleneck(G, thresholds, num_sg)
    # plot_map_bn(G, bn, bn_weight, state_id)

    return


if __name__ == '__main__':
    state_id = 48
    path = generate_file_name(7)
    main(path, state_id)

    # block_ids, dest_cbgs = read_files(path, 36)
    # g = generate_network(block_ids, dest_cbgs)
    # plot_hist(g)
