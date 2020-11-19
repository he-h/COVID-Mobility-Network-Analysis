from read_file import *


def aug_str1(id):
    id = str(id)

    if len(id) == 1:
        return '00' + id
    elif len(id) == 2:
        return '0' + id

    return id


df = pd.read_csv('data/MSA_2.csv')

MSA_fips = dict()
MSA_name = dict()

for ind in df.index:
    msa = str(df['msa'][ind])

    if msa not in MSA_fips.keys():
        MSA_fips[msa] = []

    block = str(df['county'][ind])
    if len(block) == 4:
        block = '0' + block

    if not in_states(block):
        continue
    MSA_fips[msa].append(block)
    MSA_name[msa] = str(df['msa-name'][ind])[:str(df['msa-name'][ind]).find('(')-1]

with open("data/MSAfips.json", "w") as outfile:
        json.dump(MSA_fips, outfile)

with open("data/MSAname.json", "w") as outfile:
    json.dump(MSA_name, outfile)
