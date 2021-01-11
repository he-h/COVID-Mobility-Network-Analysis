import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
import pandas as pd
import json
import datetime as dt
from read_file import *


def get_xy(pt):
    return [pt.x, pt.y]


# gdf = gpd.read_file('shape_file/tl_2019_us_cbsa/tl_2019_us_cbsa.shp')
# # gdf = gpd.read_file('shape_file/cb_2018_us_cbsa_500k/cb_2018_us_cbsa_500k.shp')
# gdf['CSAFP'] = gdf['CSAFP'].astype(str).str.zfill(4)
# gdf['GEOID'] = gdf['GEOID'].astype(str)
# centroids = gdf['geometry'].centroid
# lons, lats = [list(t) for t in zip(*map(get_xy, centroids))]
# gdf['longitude'] = lons
# gdf['latitude'] = lats
# gdf.to_crs({"init": "epsg:4326"}).plot(color="white", edgecolor="grey", linewidth=0.5, alpha=0.75) #ax=ax
# mx, my = gdf['longitude'].values, gdf['latitude'].values
#
# pos = dict()
# for i, elem in enumerate(gdf['GEOID']):
#     pos[elem] = mx[i], my[i]
#
# with open("data/pos.json", "w") as outfile:
#     json.dump(pos, outfile)



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
        # print(i)
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

# with open('data/pos.json', 'r') as o:
#     pos = json.load(o)
# plt.figure()
# m = Basemap(
#     projection='merc',
#     llcrnrlon=-130,
#     llcrnrlat=25,
#     urcrnrlon=-60,
#     urcrnrlat=50,
#     lat_ts=0,
#     resolution='i',
#     suppress_ticks=True)
# m.readshapefile('tl_2017_us_state/tl_2017_us_state', 'states', drawbounds=True)
# # m.drawcountries(linewidth=3)
# # m.drawstates(linewidth=0.2)
# # m.drawcoastlines(linewidth=1)
# # m.fillcontinents(alpha=0.3)
# # m.drawcounties(linewidth=0.1)
#
# x, y = [], []
# for i in pos.keys():
#     x.append(pos[i][0])
#     y.append(pos[i][1])
# mx, my = m(x, y)
# pos1 = dict()
# for i, j in enumerate(pos.keys()):
#     pos1[j] = (mx[i], my[i])
#
# a=nx.Graph()
# a.add_edge('35620', '31080')
#
#
# nx.draw_networkx_nodes(G=a, pos=pos1)
# ax=plt.gca()
# for i, j in a.edges():
#     ax.annotate("",
#                 xy=pos1[i], xycoords='data',
#                 xytext=pos1[j], textcoords='data',
#                 arrowprops=dict(arrowstyle="-", color='cornflowerblue',
#                                 shrinkA=5, shrinkB=5,
#                                 patchA=None, patchB=None,
#                                 connectionstyle="arc3,rad=0.3",
#                                 ),
#                 )
#
#
# plt.tight_layout()
# plt.show()
