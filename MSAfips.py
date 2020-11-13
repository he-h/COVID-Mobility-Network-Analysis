import json
from read_file import *


def aug_str1(id):
    id = str(id)

    if len(id) == 1:
        return '00' + id
    elif len(id) == 2:
        return '0' + id

    return id


df = pd.read_csv('data/MSAfips.csv')

MSA_fips = dict()

for ind in df.index:
    msa = str(df['msa.cmsa.fips'][ind])

    if msa not in MSA_fips.keys():
        MSA_fips[msa] = []

    MSA_fips[msa].append(aug_str(df['fips.state'][ind]) + aug_str1(df['fips.county'][ind]))

    with open("data/MSAfips.json", "w") as outfile:
        json.dump(MSA_fips, outfile)
