import pandas as pd
import datetime as dt

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

            if dests[i] >= 2:
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
    month = aug_str(date.month)
    day = aug_str(date.day)

    return 'data/' + month + '/' + day + '/2020-' + month + '-' + day + '-social-distancing.csv.gz'


'''
This function test in location is within the scope we want
'''


def in_states(code):
    loc = int(code[:2])
    if loc <= 56:
        return True
    return False
