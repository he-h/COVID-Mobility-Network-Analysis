import pandas as pd
import json

'''
This function is to transform a string into a dict based on destination_cbgs
'''
def parse_str(tmp):


'''
This function is designed for reading and processing csv.gz file to the data frame we want especially
origin_census_block_group and destination_cbgs from sourcegraph.com 
'''
def read_file(path):
    df = pd.read_csv(path)
    block_ids = set()
    dest_cbgs = dict()
    return block_ids, dest_cbgs

file = 'data/01/01/2020-01-01-social-distancing.csv.gz'

df = pd.read_csv(file)

for ind in df.index:
    print(type(df['origin_census_block_group'][ind]))
    dic = df['destination_cbgs'][ind]
    print(type(dic))
    break

# print(df.describe())
# for row in df.iterrows():
#     print(row['origin_census_block_group'])
# print(df)
