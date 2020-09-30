import numpy as np
from read_file import *
from model import *
import matplotlib.pyplot as plt


max_w = 30


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(g, block_ids, dest_cbgs):
    # setting thresholds
    thresholds = np.arange(0, max_w, 0.1)

    num_g = []
    num_sg = []
    for i in thresholds:
        tmp_g, tmp_sg = num_g_sg(generate_network(block_ids, dest_cbgs, i))
        num_g.append(tmp_g)
        num_sg.append(tmp_sg)

    return thresholds, num_g, num_sg


'''
This function is aim to plot number of element of G and SG with changing threshold described in the paper
'''


def plot_g_sg(x, g, sg):
    # fig, ax = plt.subplots(constrained_layout=True)
    #
    # ax.scatter(x, g, label='Largest SCC')
    # ax.scatter(x, sg, label='Second largest SCC')
    #
    # ax.set_xlabel('threshold')
    # ax.set_ylabel('Size')
    # ax.legend()

    # ax1.set_xlabel('threshold')
    # ax1.set_ylabel('size of G scc')
    # ax1.scatter(x, g, s=1, label='G')
    # ax1.tick_params(axis='y')
    # ax1.legend(loc=0)
    #
    #
    # ax2.set_ylabel('size of SG scc')

    # ax2.scatter(x, sg, s=1, color='orange', label='SG')
    # ax2.tick_params(axis='y')
    # ax2.legend(loc=0)
    #
    # fig.tight_layout()
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('threshold')
    ax1.set_ylabel('size')
    ax1.plot(x, g)
    ax1.tick_params(axis='y')
    ax2 = ax1.twinx()
    ax2.plot(x, sg, color='orange')
    ax2.tick_params(axis='y')
    fig.tight_layout()

    plt.show()

    return


'''
This function is to find the bottleneck by analyzing the threshold around when the second SCC is the largest
'''


def calc_bottleneck(block_ids, dest_cbgs, num_sg):
    max_index = [i for i, j in enumerate(num_sg) if j == max(num_sg)][0]

    G_sg_largest = generate_network(block_ids, dest_cbgs, max_index)
    G_b_sg_largest = generate_network(block_ids, dest_cbgs, max_index-1)

    G_sg_largest.sort(key=lambda a: len(a))
    scc_sg_largest = G_sg_largest[-1]
    scc_sg_s_largest = G_sg_largest[-2]

    for i, j in dest_cbgs.keys():
        if dest_cbgs[(i, j)] == max_index:
            if (i in scc_sg_largest and j in scc_sg_s_largest) or (j in scc_sg_largest and i in scc_sg_s_largest):
                return i, j

    return None


'''
This function plot the histograph of weights of edges with a logrithmic scale
'''


def plot_hist(dest_cbgs):
    value = list(dest_cbgs.values())

    plt.hist(value, label='number of weights', log=True, bins=100)
    # plt.yscale('log')
    plt.legend()
    plt.show()

    return


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
    block_ids, dest_cbgs = read_files(path, state_id)
    G = generate_network(block_ids, dest_cbgs)
    thresholds, num_g, num_sg = calc_g_sg(G, block_ids, dest_cbgs)
    plot_g_sg(thresholds, num_g, num_sg)
    # print(calc_g_sg())
    return


if __name__ == '__main__':
    state_id = 25
    path = generate_file_name(7)
    main(path, state_id)
    # files = generate_file_name(7)
    # block_ids, dest_cbgs = read_files(files, 25)
    # plot_hist(dest_cbgs)
