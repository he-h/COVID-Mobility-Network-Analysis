import pandas as pd

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


def read_file(path, num):
    df = pd.read_csv(path)
    block_ids = set()
    dest_cbgs = dict()

    for ind in df.index:
        block = str(df['origin_census_block_group'][ind])
        if not block.startswith(str(num)):
            continue
        block_ids.add(block)

        dests = parse_str(df['destination_cbgs'][ind])
        for i in dests.keys():
            if not i.startswith(str(num)):
                continue
            dest_cbgs[(block, i)] = dests[i]

    return block_ids, dest_cbgs


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


def read_files(paths, id):
    block_ids = set()
    dest_cbgs = dict()
    for i in paths:
        tmp_ids, tmp_dests = read_file(i, id)
        block_ids = block_ids.union(tmp_ids)
        merge(dest_cbgs, tmp_dests)

    for i in dest_cbgs.keys():
        dest_cbgs[i] /= len(paths)

    return block_ids, dest_cbgs


# file = ['data/01/01/2020-01-01-social-distancing.csv.gz', 'data/01/02/2020-01-02-social-distancing.csv.gz']
# # print(len(read_files(file, 25)[0]))
