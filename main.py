import numpy as np
from read_file import *
from model import *
import matplotlib.pyplot as plt


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(file, num):
    block_ids, dest_cbgs = read_file(file, num)
    G = generate_network(block_ids, dest_cbgs)
    max_w = max_weight(G)

    # setting thresholds
    thresholds = np.arange(0, max_w, 1)

    num_g = []
    num_sg = []
    for i in range(max_w):
        tmp_g, tmp_sg = num_g_sg(generate_network(block_ids, dest_cbgs, i))
        num_g.append(tmp_g)
        num_sg.append(tmp_sg)

    return thresholds, num_g, num_sg


'''
This function is aim to plot number of element of G and SG with changing threshold described in the paper
'''


def plot_g_sg(x, g, sg):
    # plotting
    plt.xlabel('threshold')
    plt.ylabel('size of scc')
    plt.scatter(x, g, s=1, label='G')
    plt.scatter(x, sg, s=1, label='SG')
    plt.legend()
    plt.show()

    return


def main(file, state_id):
    plot_g_sg(*calc_g_sg(file, state_id))

    return


if __name__ == '__main__':
    path = 'data/03/31/2020-03-31-social-distancing.csv.gz'
    state_id = 36
    main(path, state_id)
