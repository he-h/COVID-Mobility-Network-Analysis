import numpy as np
from read_file import *
from model import *


def main(threshold):
    file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
    block_ids, dest_cbgs = read_file(file)
    g = generate_network(block_ids, dest_cbgs)

    new_dest_cbgs = dict()
    for i in dest_cbgs.keys():
        if dest_cbgs[i] > threshold:
            new_dest_cbgs[i] = dest_cbgs[i] = threshold
    percolation_g = generate_network(block_ids, new_dest_cbgs)

    return


if __name__ == '__main__':
    threshold = 0
    main(threshold)
