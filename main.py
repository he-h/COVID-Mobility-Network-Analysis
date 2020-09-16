import numpy as np
from read_file import *
from model import *


def main(threshold):
    file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
    G = generate_network(*read_file(file))

    return

if __name__ == '__main__':
    threshold = 0
    main(threshold)
