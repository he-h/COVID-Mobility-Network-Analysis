import numpy as np
import pandas as pd
import pandas


def read_file_a(df, num=''):
    #
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

for file in sorted(file_list):
    df = pd.read_csv(file)
    df['origin_census_block_group'] = df['origin_census_block_group'].astype(str).str.zfill(12)
    df['GEOID'] = df['origin_census_block_group'].str[0:5]
    tmp1 = df[['GEOID','origin_census_block_group', 'date_range_start',
       'device_count', 'distance_traveled_from_home',
       'completely_home_device_count', 'median_home_dwell_time',
       'median_non_home_dwell_time','median_percentage_time_home']]
    tmp1x =tmp1.groupby('GEOID').agg({'device_count':sum, 'distance_traveled_from_home':np.median,
       'completely_home_device_count':sum, 'median_home_dwell_time':np.median,
       'median_non_home_dwell_time':np.median,'median_percentage_time_home':np.median}).reset_index()
    dicx = read_file_a(df, num='')
    dfx =pandas.DataFrame().from_dict(dicx.items())
    dfx.columns = ['id','count']
    dfx['origin_census_block_group']= dfx['id'].astype(str).str[2:14]
    dfx['dest_census_block_group']= dfx['id'].astype(str).str[18:30]
    dfx['origin_census_block_group'] = dfx['origin_census_block_group'].astype(str).str.zfill(12)
    dfx['dest_census_block_group'] = dfx['dest_census_block_group'].astype(str).str.zfill(12)
    dfx = dfx.drop(dfx.columns[0], axis=1)
    dfx['county1'] = dfx['origin_census_block_group'].astype(str).str[0:5]
    dfx['county2'] = dfx['dest_census_block_group'].astype(str).str[0:5]
    tmpx = dfx.groupby(['county1','county2']).agg({'count':sum}).reset_index()
    tmpx.columns=['GEOID1','GEOID2','count']
    tmp1x.to_csv('/scratch/deng.yi/safegraph/social-distancing/'+file[27:37]+'-social-distancing.csv',index = False)
    tmpx.to_csv('/scratch/deng.yi/safegraph/bg_flux/'+file[27:37]+'-flux.csv',index = False)