import json
# from plot import *
from whole_network import *
import time
from datetime import date
import inter_MSA
import pandas as pd
from sklearn import linear_model

# path = 'data/2020/01/01/2020-01-01-social-distancing.csv.gz'
# device_count = "msa_device_count/01_01.json"
# with open(device_count, "r") as outfile:
#     device_count = json.load(outfile)
#
# dest = dict()
# m_dest = default_MSAs_dict()
#
# df = pd.read_csv(path)
# if __name__ == '__main__':
#     for ind in df.index:
#         block = block_str(str(df['origin_census_block_group'][ind]))
#
#         block_m = MSA_id(block)
#         if block_m == -1:
#             continue
#         #
#         # if block_m in device_count.keys():
#         #     device_count[block_m] += df['device_count'][ind]
#         # else:
#         #     device_count[block_m] = df['device_count'][ind]
#
#         dests = eval(df['destination_cbgs'][ind])
#         for i in dests.keys():
#             if dests[i] <= 2:
#                 continue
#
#             str_i = block_str(str(i))
#
#             if str_i == block:
#                 continue
#
#             i_m = MSA_id(str_i)
#             if i_m == -1:
#                 continue
#
#             if i_m != block_m:
#                 tmp = tuple(sorted([block_m, i_m]))
#                 if tmp in dest.keys():
#                     dest[tmp] += dests[i]/device_count[block_m]/7*10000
#                 else:
#                     dest[tmp] = dests[i]/device_count[block_m]/7*10000
#             else:
#                 tmp = tuple(sorted([block, str_i]))
#                 if tmp in m_dest[block_m].keys():
#                     m_dest[block_m][tmp] += dests[i]/df['device_count'][ind]/7*100
#                 else:
#                     m_dest[block_m][tmp] = dests[i]/df['device_count'][ind]/7*100
#
#     msa = ['17820', '35620', '31080', '26420', '23540', '24500']
#     for i in msa:
#         with open('edgelist'+i+'.csv', mode='x') as edges:
#
#             csvwriter = csv.writer(edges)
#
#             csvwriter.writerow(['bg', 'bg2', 'weight'])
#             for i, j in m_dest[i].items():
#                 csvwriter.writerow([i[0], i[1], j])
#     # tmp = InterMsaG(date(2020,1,1), dest, device_count)
#     # tmp.plot_w_qc_perco()
#     # plt.clf()
#     # a = m_dest['41860'] #31080
#     # c = m_dest['31080']
#     # import geopandas as gpd
#     #
#     # gdf = gpd.read_file('tl_2017_06_bg/tl_2017_06_bg.shp')
#     # gdf['GEOID'] = gdf['GEOID'].astype(str)
#     # centroids = gdf['geometry'].centroid
#     # lons, lats = [list(t) for t in zip(*map(get_xy, centroids))]
#     # gdf['longitude'] = lons
#     # gdf['latitude'] = lats
#     # gdf.to_crs({"init": "epsg:4326"}).plot(color="white", edgecolor="grey", linewidth=0.5, alpha=0.75) #ax=ax
#     # mx, my = gdf['longitude'].values, gdf['latitude'].values
#     #
#     # pos = dict()
#     # for i, elem in enumerate(gdf['GEOID']):
#     #     pos[elem] = mx[i], my[i]
#     #
#     # b = generate_network(a)
#     # print(len(b.edges))
#     # nx.draw_networkx_nodes(b, pos=pos, node_color='red', node_size=.5)
#     # ax = plt.gca()
#     # for i, j in b.edges():
#     #     ax.annotate("",
#     #                 xy=pos[i], xycoords='data',
#     #                 xytext=pos[j], textcoords='data',
#     #                 arrowprops=dict(arrowstyle="-", color='blue',
#     #                                 shrinkA=5, shrinkB=5,
#     #                                 patchA=None, patchB=None,
#     #                                 connectionstyle="arc3,rad=0.3",
#     #                                 ),
#     #                 )
#     #
#     # d = generate_network(c)
#     # nx.draw_networkx_nodes(d, pos=pos, node_color='green', node_size=.5)
#     # ax = plt.gca()
#     # for i, j in d.edges():
#     #     ax.annotate("",
#     #                 xy=pos[i], xycoords='data',
#     #                 xytext=pos[j], textcoords='data',
#     #                 arrowprops=dict(arrowstyle="-", color='purple',
#     #                                 shrinkA=5, shrinkB=5,
#     #                                 patchA=None, patchB=None,
#     #                                 connectionstyle="arc3,rad=0.3",
#     #                                 ),
#     #                 )
#     # plt.tight_layout()
#     # plt.show()
from statsmodels.compat import lzip
import statsmodels.stats.api as sms
import statsmodels.api as sm
import numpy as np
import statsmodels.formula.api as smf
import seaborn as sns
plt.clf()
fig, ax = plt.subplots()
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
tmp = date(2020,2,1)
a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
a['gc_size'] = np.log(a['gc_size'])
sns.regplot(y="qc", x="gc_size", data=a, color='#9ecae1',label='Before')
tmp = date(2020,4,6)


a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
a['gc_size'] = np.log(a['gc_size'])
qc = a['qc']
q = a['gc_size']
# plt.scatter(qc, q, s=10, color='dodgerblue')
sns.regplot(y="qc", x="gc_size", data=a, color='#fdae6b',label='After')



plt.ylabel(r'$\alpha{q_c}$', fontsize=17)
plt.xlabel(r'$\alpha{GC}$ Size(log)', fontsize=15)
plt.legend(prop={'size':21})
plt.savefig('qc_gc_b.png')


plt.clf()
fig, ax = plt.subplots()
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
tmp = date(2020,2,1)
a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
sns.regplot(y="qc", x="flux", data=a, color='#9ecae1',label='Before')

tmp = date(2020,4,6)


a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
sns.regplot(y="qc", x="flux", data=a, color='#fdae6b',label='After')


plt.ylabel(r'$\alpha{q_c}$', fontsize=17)
plt.xlabel(r'$\alpha$ Total Flux', fontsize=15)

plt.savefig('qc_flux_b.png')


plt.clf()
fig, ax = plt.subplots()
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
tmp = date(2020,2,1)
a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
sns.regplot(y="qc", x="edge_w",data=a, color='#9ecae1',label='Before')

tmp = date(2020,4,6)


a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
sns.regplot(y="qc", x="edge_w", data=a, color='#fdae6b',label='After')





plt.ylabel(r'$\alpha{q_c}$', fontsize=17)
plt.xlabel(r'$\alpha$ Median Edge Weight', fontsize=15)

plt.savefig('qc_edge_b.png')

plt.clf()
tmp = date(2020,2,1)
a = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
# a['gc_size'] = np.log(a['gc_size'])
# sns.regplot(x="qc", y="gc_size", data=a, color='#9ecae1',label='Before')
tmp = date(2020,4,6)


b = pd.read_csv(tmp.strftime('qc/%m_%d.csv'))
a['gc_size'] = b['qc']
qc = a['qc']
q = a['gc_size']
# plt.scatter(qc, q, s=10, color='dodgerblue')
fig, ax = plt.subplots()
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
sns.regplot(x="qc", y="gc_size", data=a, color='#9ecae1')






plt.xlabel(r'$q_c$(before)', fontsize=16)
plt.ylabel(r'$q_c$', fontsize=16)

plt.savefig('m.png')