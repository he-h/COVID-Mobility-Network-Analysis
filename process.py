import csv
from read_file import *
import os
from whole_network import read_files_whole

date = dt.date(2020, 3, 8)


def aug_file(date):
    return 'processed_data/'+aug_str(date.month)+'/'+aug_str(date.day)+'/'


while date < dt.date(2020, 11, 1):

    path = 'processed_data/'+aug_str(date.month)+'/'+aug_str(date.day) + '/'

    device_count, dest, m_dev, m_dest = read_files_whole(date)

    with open(path + 'inter_msa_edge.csv', mode='x') as edges:

        csvwriter = csv.writer(edges)

        csvwriter.writerow(['from', 'to', 'weight'])

        for i in dest.keys():
            if dest[i] > 1:
                csvwriter.writerow([i[0], i[1], dest[i]])

    with open(path + 'msa_edge.csv', mode='x') as edges:

        csvwriter = csv.writer(edges)

        csvwriter.writerow(['from', 'to', 'weight', 'msa'])

        for i in m_dest.keys():
            for j in m_dest[i].keys():
                if m_dest[i][j] > 2:
                    csvwriter.writerow([j[0], j[1], m_dest[i][j], i])

    with open(path + 'inter_msa_device.csv', mode='x') as devices:

        csvwriter = csv.writer(devices)

        csvwriter.writerow(['msa', 'device'])

        for i in device_count.keys():
            csvwriter.writerow([i, device_count[i]])

    date += dt.timedelta(days=28)
