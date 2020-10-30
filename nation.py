import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import json
from read_file import *
from model import *

state_code = {
    '02': 'AK', '28': 'MS',
    '01': 'AL', '30': 'MT',
    '05': 'AR',	'37': 'NC',
    '60': 'AS',	'38': 'ND',
    '04': 'AZ',	'31': 'NE',
    '06': 'CA',	'33': 'NH',
    '08': 'CO',	'34': 'NJ',
    '09': 'CT',	'35': 'NM',
    '11': 'DC',	'32': 'NV',
    '10': 'DE',	'36': 'NY',
    '12': 'FL',	'39': 'OH',
    '13': 'GA',	'40': 'OK',
    '66': 'GU',	'41': 'OR',
    '15': 'HI',	'42': 'PA',
    '19': 'IA',	'72': 'PR',
    '16': 'ID',	'44': 'RI',
    '17': 'IL',	'45': 'SC',
    '18': 'IN',	'46': 'SD',
    '20': 'KS',	'47': 'TN',
    '21': 'KY',	'48': 'TX',
    '22': 'LA',	'49': 'UT',
    '25': 'MA',	'51': 'VA',
    '24': 'MD',	'78': 'VI',
    '23': 'ME',	'50': 'VT',
    '26': 'MI',	'53': 'WA',
    '27': 'MN',	'55': 'WI',
    '29': 'MO',	'54': 'WV',
    '56': 'WY'
}


def aug_str(id):
    id = str(id)

    if len(id) == 1:
        return '0' + id

    return id


def generate_files():
    files = []
    date = dt.date(2020, 1, 12)

    for i in range(28):
        month = aug_str(date.month)
        day = aug_str(date.day)

        files.append('data/'+month+'/'+day+'/2020-'+month+'-'+day+'-social-distancing.csv.gz')
        date += dt.timedelta(days=1)

    return files


def cc_sizes(g):
    thershold = 3
    thersholds = []
    num_cc = []
    step_size = .25
    stop_point = 50

    while True:
        perco_g = generate_network_threshold(g, thershold)
        cc = len(list(nx.connected_components(perco_g)))
        print(cc)
        break
        thersholds.append(thershold)
        thershold += step_size
        num_cc.append(cc)

        if cc <= 10000:
            regions = dict()

            for i, j in enumerate(sorted(list(nx.connected_components(perco_g)), key=len, reverse=True)):
                if i >= stop_point:
                    break
                regions[i] = tuple(j)

            with open("regions.json", "w") as outfile:
                json.dump(regions, outfile)
            break

    return thersholds, num_cc


def plot(x, y):
    plt.plot(x, y)
    plt.savefig('size_of_cc.png')


if __name__ == '__main__':
    data = generate_files()
    dest = read_files(data)
    G = generate_network(dest)
    thersholds, num_cc = cc_sizes(G)
    plot(thersholds, num_cc)
