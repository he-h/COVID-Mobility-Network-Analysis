import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
import pandas as pd
import json
import datetime as dt
from read_file import *


def get_xy(pt):
    return [pt.x, pt.y]



def file_whole(path):
    dest = dict()
    device_count = dict()
    m_dest = default_MSAs_dict()

    df = pd.read_csv(path)

    for ind in df.index:
        block = block_str(str(df['origin_census_block_group'][ind]))

        block_m = MSA_id(block)
        if block_m == -1:
            continue

        if block_m in device_count.keys():
            device_count[block_m] += df['device_count'][ind]
        else:
            device_count[block_m] = df['device_count'][ind]



    return device_count


def read_files_whole(date):
    device_count = dict()
    dest = dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(7):
        tmp_device = file_whole(file_str(tmp))
        merge(device_count, tmp_device)
        tmp += dt.timedelta(days=1)

    for i in device_count.keys():
        device_count[i] /= 7

    with open("msa_device_count/"+ date.strftime('%m_%d') + ".json", "x") as outfile:
        json.dump(device_count, outfile)


    return device_count

date = dt.date(2020,1,1)
while date < dt.date(2021,1,1):
    read_files_whole(date)
    date+=dt.timedelta(days=1)

