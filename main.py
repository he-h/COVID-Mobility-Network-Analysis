import numpy as np
from read_file import *
from model import *
import matplotlib.pyplot as plt


'''
This function is aim to plot number of element of G and SG with changing threshold described in the paper
'''


def plot_g_sg(file, num):
    block_ids, dest_cbgs = read_file(file, num)
    G = generate_network(block_ids, dest_cbgs)
    max_w = max_weight(G)

    # setting thresholds
    thresholds = np.arange(0, max_w, 1)
    num_g, num_sg = num_g_sg(generate_network(block_ids, dest_cbgs, thresholds))

    # plotting
    plt.xlabel('threshold')
    plt.ylabel('size of scc')
    plt.plot(thresholds, num_g, 'G')
    plt.plot(thresholds, num_sg, 'SG')
    plt.legend()
    plt.show()


def main(file, state_id):
    plot_g_sg(file, state_id)

    return


if __name__ == '__main__':
    path = 'data/01/01/2020-01-01-social-distancing.csv.gz'
    state_id = 25
    main(path, state_id)
