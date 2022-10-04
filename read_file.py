import pandas as pd
import datetime as dt
import json


with open('data/MSAfips.json') as file:
    MSAfips = json.load(file)


'''
This function is to transform a string into a dict based on destination_cbgs
return a dict with key = destination and value = number of people been there
'''


def parse_str(tmp):
    tmp = tmp.lstrip('{').rstrip('}')
    dest_dict = dict()

    tmp = tmp.split(',')
    for i in tmp:
        i = i.split(':')
        key = i[0].strip('"')
        value = int(i[1])
        dest_dict[key] = value

    return dest_dict


'''
This function is designed for reading and processing csv.gz file to the data frame we want especially
origin_census_block_group and destination_cbgs from https://docs.safegraph.com/docs/social-distancing-metrics
return with a set of block ids and a dict with key = (start, destination) value = number of people
'''


def read_file(path, num=''):
    df = pd.read_csv(path)
    dest_cbgs = dict()

    for ind in df.index:
        block = str(df['origin_census_block_group'][ind])
        if not block.startswith(str(num)):
            continue

        if not in_states(block):
            continue

        dests = parse_str(df['destination_cbgs'][ind])
        for i in dests.keys():
            if i == block:
                continue

            if not i.startswith(str(num)):
                continue

            if not in_states(i):
                continue

            if dests[i] >= 3:
                dest_cbgs[(block, i)] = dests[i]

    return dest_cbgs


'''
This function merges two dictionaries with new value = sum of previous two dicts
'''


def merge(dict1, dict2):
    for i in dict2.keys():
        if i not in dict1.keys():
            dict1[i] = dict2[i]
        else:
            dict1[i] += dict2[i]

    return


'''
This function basically uses the function above to read multiple files with returning value block ids and destination cbgs
'''


def read_files(paths, id=''):
    dest_cbgs = dict()
    for i in paths:
        print(i)
        tmp_dests = read_file(i, id)
        merge(dest_cbgs, tmp_dests)

    for i in dest_cbgs.keys():
        dest_cbgs[i] /= len(paths)

    return dest_cbgs


'''
read file function for class generation
'''


def read_file_c(path, scope):
    df = pd.read_csv(path)
    dest_cbgs = dict()

    for ind in df.index:
        block = str(df['origin_census_block_group'][ind])
        if block not in scope:
            continue

        dests = parse_str(df['destination_cbgs'][ind])
        for i in dests.keys():
            if i == block:
                continue

            if i not in scope:
                continue
            if dests[i] >= 3:
                dest_cbgs[(block, i)] = dests[i]

    return dest_cbgs


'''
read multiple files for the class
'''


def read_files_c(date, scope):
    start = date - dt.timedelta(days=3)
    dest_cbgs = dict()

    for i in range(7):
        tmp_dests = read_file_c(file_str(start), scope)
        merge(dest_cbgs, tmp_dests)
        start += dt.timedelta(days=1)

    for i in dest_cbgs.keys():
        dest_cbgs[i] /= 7

    return daily_device_count(date), dest_cbgs


'''
get device count for the day
'''


def daily_device_count(date):
    df = pd.read_csv(file_str(date))
    devices = 0

    for ind in df.index:
        devices += df['device_count'][ind]

    return devices


'''
generate approriate str based on date
'''


def aug_str(id):
    id = str(id)

    if len(id) == 1:
        return '0' + id

    return id


'''
This function create path for file retraction
'''


def file_str(date):

    return date.strftime('data/%Y/%m/%d/%Y-%m-%d-social-distancing.csv.gz')


'''
This function test in location is within the scope we want
'''


def in_states(code):
    loc = int(code[:2])
    if loc <= 56 and loc != 2 and loc != 15:
        return True
    return False


'''
This function decide which MSA this block group belongs to
'''


def MSA_id(bg):
    if len(bg) == 12:
        id = bg[:5]
    else:
        id = '0' + bg[:4]
    for i in MSAfips.keys():
        if id in MSAfips[i]:
            return i

    return -1


'''
This creates inner MSA dictionary by default
'''


def default_MSAs_dict():
    tmp = dict()
    for i in MSAfips.keys():
        tmp[i] = dict()

    return tmp


'''
This function helps merge inner MSA dicts
'''


def inner_merge(d1, d2):
    for i in d1.keys():
        merge(d1[i], d2[i])


'''
date str
'''


def dt_str(date):
    return date.strftime('%m_%d')


'''
block str
'''


def block_str(tmp):
    if len(tmp) == 11:
        return '0' + str(tmp)

    return str(tmp)


def process_data_str(tmp):
    return 'processed_data/'+aug_str(tmp.month)+'/'+aug_str(tmp.day) + '/'


def qc_str(tmp):
    return 'qc/'+dt_str(tmp)+'.csv'


def comli(a, num):
    if len(a)<num:
        a.append(0)
        return comli(a,num)
    return a
