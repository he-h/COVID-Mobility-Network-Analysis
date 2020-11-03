import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import json
from read_file import *
from model import *

nation_bg_num = 211267

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


def generate_files():
    files = []
    date = dt.date(2020, 1, 12)

    for i in range(28):
        month = aug_str(date.month)
        day = aug_str(date.day)

        files.append('data/'+month+'/'+day+'/2020-'+month+'-'+day+'-social-distancing.csv.gz')
        date += dt.timedelta(days=1)

    return files


def statescope(region):
    scope = set()

    for i in region:
        scope.add(i[:2])

    return scope


def attributes(g):
    threshold = 3

    thresholds = []
    num_cc = []

    # percentage of different cluster based on original network
    per_cc_1 = []
    per_cc_2 = []
    per_cc_10 = []
    per_cc_50 = []

    # percent of different clusters based on current network
    c_per_cc_1 = []
    c_per_cc_2 = []
    c_per_cc_10 = []
    c_per_cc_50 = []

    step_size = 1
    stop_point = 10

    while threshold <= stop_point:
        print(threshold)
        perco_g = generate_network_threshold(g, threshold)
        size = len(perco_g.nodes)
        ccs = sorted(list(nx.connected_components(perco_g)), key=len, reverse=True)
        thresholds.append(threshold)

        num_cc.append(len(ccs))

        cc_1 = sum(map(len, ccs[:1]))
        cc_2 = sum(map(len, ccs[1:2]))
        cc_10 = sum(map(len, ccs[:10]))
        cc_50 = sum(map(len, ccs[:50]))

        per_cc_1.append(cc_1 / nation_bg_num)
        per_cc_2.append(cc_2 / nation_bg_num)
        per_cc_10.append(cc_10 / nation_bg_num)
        per_cc_50.append(cc_50 / nation_bg_num)

        c_per_cc_1.append(cc_1 / size)
        c_per_cc_2.append(cc_2 / size)
        c_per_cc_10.append(cc_10 / size)
        c_per_cc_50.append(cc_50 / size)

        # add data to json file
        regions = dict()
        scope = dict()

        for i, j in enumerate(ccs):
            if i >= 50:
                break
            regions[i] = tuple(j)
            scope[i] = tuple(statescope(j))

        with open("region_div/region"+str(threshold)+".json", "w") as outfile:
            json.dump(regions, outfile)

        with open("region_div/region_s_"+str(threshold)+".json", "w") as outfile:
            json.dump(scope, outfile)

        threshold += step_size

    return thresholds, num_cc, per_cc_1, per_cc_2, per_cc_10, per_cc_50, c_per_cc_1, c_per_cc_2, c_per_cc_10, c_per_cc_50


def size_plot(x, y):
    plt.figure()
    plt.plot(x, y)
    plt.ylabel('Number of clusters')
    plt.xlabel('Threshold')
    plt.savefig('nations/num_cc.png')


def percent_plot(threshold, cc_1, cc_2, cc_10, cc_50, title):
    plt.figure()
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    plt.plot(threshold, cc_1, color='dodgerblue', label='1st cc')
    plt.plot(threshold, cc_2, color='peachpuff', label='2nd cc')
    plt.plot(threshold, cc_10, color='gray', label='top 10 cc')
    plt.plot(threshold, cc_50, color='silver', label='top 50 cc')

    plt.grid(True)
    plt.legend()
    plt.title(title)
    plt.savefig('nations/'+title+'.png')


if __name__ == '__main__':
    data = generate_files()
    dest = read_files(data)
    G = generate_network(dest)
    thresholds, num_cc, per_cc_1, per_cc_2, per_cc_10, per_cc_50, c_per_cc_1, c_per_cc_2, c_per_cc_10, c_per_cc_50 = attributes(G)
    size_plot(thresholds, num_cc)
    percent_plot(thresholds, per_cc_1, per_cc_2, per_cc_10, per_cc_50, 'Cluster size as a proportion to whole network')
    percent_plot(thresholds, c_per_cc_1, c_per_cc_2, c_per_cc_10, c_per_cc_50, 'Cluster size as a proportion to percolation network')
