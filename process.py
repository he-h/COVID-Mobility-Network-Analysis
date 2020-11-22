import csv
from read_file import *
import os
from whole_network import read_files_whole

date = dt.date(2020, 3, 18)


def aug_file(date):
    return 'processed_data/'+aug_str(date.month)+'/'+aug_str(date.day)+'/'

os.mkdir("processed_data")
for i in range(3, 11):
    os.mkdir("processed_data/"+aug_str(i))


while date < dt.date(2020, 11, 1):

    path = 'processed_data/'+aug_str(date.month)+'/'+aug_str(date.day) + '/'
    os.mkdir("processed_data/" + aug_str(date.month) + '/' + aug_str(date.day))

    device_count, dest, m_dev, m_dest = read_files_whole(date)

    with open(path + 'inter_msa_edge.csv', mode='x') as edges:

        csvwriter = csv.writer(edges)

        csvwriter.writerow(['edge', 'weight'])

        for i in dest.keys():
            csvwriter.writerow([i, dest[i]])

    with open(path + 'msa_edge.csv', mode='x') as edges:

        csvwriter = csv.writer(edges)

        csvwriter.writerow(['edge', 'weight', 'msa'])

        for i in m_dest.keys():
            for j in m_dest[i].keys():
                if m_dest[i][j] > 2:
                    csvwriter.writerow([j, m_dest[i][j], i])

    with open(path + 'inter_msa_device.csv', mode='x') as devices:

        csvwriter = csv.writer(devices)

        csvwriter.writerow(['msa', 'device'])

        for i in device_count.keys():
            csvwriter.writerow([i, device_count[i]])

    with open(path + 'msa_device.csv', mode='x') as devices:

        csvwriter = csv.writer(devices)

        csvwriter.writerow(['bg', 'device', 'msa'])

        for i in m_dev.keys():
            for j in m_dev[i].keys():
                csvwriter.writerow([j, m_dev[i][j], i])

    date += dt.timedelta(days=7)
