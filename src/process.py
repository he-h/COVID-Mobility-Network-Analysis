import csv
from read_file import *

date = dt.date(2020, 1, 19)


def aug_file(date):
    return 'processed_data/'+aug_str(date.month)+'/'+aug_str(date.day)+'/'


for k in range(7):
    df = pd.read_csv(file_str(date))

    dest_cbgs = dict()
    device_count = dict()

    for ind in df.index:
        block = str(df['origin_census_block_group'][ind])
        if not in_states(block):
            continue

        device_count[block] = df['device_count'][ind]

        dests = parse_str(df['destination_cbgs'][ind])
        for i in dests.keys():
            if i == block:
                continue

            if not in_states(i):
                continue

            dest_cbgs[block, i] = dests[i]

    with open(aug_file(date) + 'edge.csv', mode='x') as edges:

        csvwriter = csv.writer(edges)

        csvwriter.writerow(['from', 'to', 'weight'])

        for a, b in dest_cbgs.keys():
            csvwriter.writerow([a, b, dest_cbgs[(a,b)]])

    with open(aug_file(date) + 'device.csv', mode='x') as devices:

        csvwriter = csv.writer(devices)

        csvwriter.writerow(['block', 'device'])

        for j in device_count.keys():
            csvwriter.writerow([j, device_count[j]])

    date += dt.timedelta(days=1)
