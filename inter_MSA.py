from read_file import *
from model import *
import networkx as nx

# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362


def file_inter_MSA(path):
    dest = dict()
    device_count = dict()
    df = pd.read_csv(path)

    for ind in df.index:
        block = str(df['origin_census_block_group'][ind])

        block_m = MSA_id(block)
        if block_m == -1:
            continue

        if block_m in device_count.keys():
            device_count[block_m] += df['device_count'][ind]
        else:
            device_count[block_m] = df['device_count'][ind]

        dests = eval(df['destination_cbgs'][ind])
        for i in dests.keys():
            if i == block:
                continue

            i_m = MSA_id(i)
            if i_m == -1 or i_m == block_m:
                continue
            if (block_m, i_m) in dest.keys():
                dest[(block_m, i_m)] += dests[i]
            else:
                dest[(block_m, i_m)] = dests[i]

    return device_count, dest


def read_files_inter_MSA(date):
    device_count = dict()
    dest = dict()

    tmp = date - dt.timedelta(days=3)
    print('s')

    for i in range(7):
        print(i)
        tmp_device, tmp_dests = file_inter_MSA(file_str(tmp))
        merge(dest, tmp_dests)
        merge(device_count, tmp_device)
        tmp += dt.timedelta(days=1)

    for i in device_count.keys():
        device_count[i] /= 7

    for i in dest.keys():
        dest[i] /= 7

    return device_count, dest

a,b = read_files_inter_MSA(dt.date(2020,3,1))

class InterMsaG:
    def __init__(self, date):
        self.date = date
        self.device_count, dest = read_files_inter_MSA(date)
        self.g = generate_network(dest)
