import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from read_file import *
from model import *


def aug_str(id):
    id = str(id)

    if (len(id)) == 1:
        return '0' + id

    return id


def generate_files():
    files = []
    date = dt.date(2020,1,12)

    for i in range(28):
        month = aug_str(date.month)
        day = aug_str(date.day)

        files.append('data/'+month+'/'+day+'/2020-'+month+'-'+day+'-social-distancing.csv.gz')
        date += dt.timedelta(days=1)

    return files


def cc_sizes(g):
    thershold = 0
    thersholds = []
    num_cc = []
    step_size = .25
    stop_point = 50

    while True:
        perco_g = generate_network_threshold(g, thershold)
        cc = len(nx.connected_components(perco_g))
        thersholds.append(thershold)
        num_cc.append(cc)

        if cc >= 50:
            break

    return thersholds, num_cc


def plot(x, y):
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    data = generate_files()
    dest = read_files(data)
    G = generate_network(dest)