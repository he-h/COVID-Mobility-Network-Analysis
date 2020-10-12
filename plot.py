import matplotlib.pyplot as plt
import geopandas as gpd
import networkx as nx
from model import *

'''
This function is aim to plot number of element of G and SG with changing threshold described in the paper
'''


def plot_g_sg(x, g, sg):

    figure, axis_1 = plt.subplots()

    axis_1.plot(x, g, color='blue', label='largest SCC')
    axis_1.set_xlabel('threshold')
    axis_1.set_ylabel('size')

    axis_2 = axis_1.twinx()
    axis_2.plot(x, sg, color='orange', label='second largest SCC')
    lines_1, labels_1 = axis_1.get_legend_handles_labels()
    lines_2, labels_2 = axis_2.get_legend_handles_labels()

    lines = lines_1 + lines_2
    labels = labels_1 + labels_2

    axis_1.legend(lines, labels, loc=0)

    plt.show()

    return


'''
This function plot the histograph of weights of edges with a logrithmic scale
'''


def plot_hist(g):
    value = list()

    for i in g.edges():
        value.append(g.edges[i]['weight'])

    plt.hist(value, label='number of weights', log=True, bins=7000)
    plt.xscale('log')
    plt.grid(True)
    plt.legend()
    plt.show()

    return


'''
This function returns latitude and longitude of a point
'''


def get_xy(pt):
    return [pt.x, pt.y]


'''
This function is used to plot a map of network
'''


def plot_map(g, id):
    gdf = gpd.read_file('tl_2017_' + str(id) + '_bg/tl_2017_' + str(id) + '_bg.shp')
    gdf['GEOID'] = gdf['GEOID'].astype(str)
    centroids = gdf['geometry'].centroid
    lons, lats = [list(t) for t in zip(*map(get_xy, centroids))]
    gdf['longitude'] = lons
    gdf['latitude'] = lats
    gdf.to_crs({"init": "epsg:4326"}).plot(color="white", edgecolor="grey", linewidth=0.5, alpha=0.75) #ax=ax
    mx, my = gdf['longitude'].values, gdf['latitude'].values

    pos = dict()
    for i, elem in enumerate(gdf['GEOID']):
        pos[elem] = mx[i], my[i]

    nx.draw_networkx(g, pos=pos, node_color='#bebada', with_labels=False, node_size=10)

    plt.show()

    return


'''
This function is used to plot a map with the largest second connected component and bottleneck
'''


def plot_map_bn(g, bottleneck, bn_weight, id):
    gdf = gpd.read_file('tl_2017_' + str(id) + '_bg/tl_2017_' + str(id) + '_bg.shp')
    gdf['GEOID'] = gdf['GEOID'].astype(str)
    centroids = gdf['geometry'].centroid
    lons, lats = [list(t) for t in zip(*map(get_xy, centroids))]
    gdf['longitude'] = lons
    gdf['latitude'] = lats
    gdf.to_crs({"init": "epsg:4326"}).plot(color="white", edgecolor="grey", linewidth=0.5, alpha=0.75) #ax=ax
    mx, my = gdf['longitude'].values, gdf['latitude'].values

    pos = dict()
    for i, elem in enumerate(gdf['GEOID']):
        pos[elem] = mx[i], my[i]

    new_g = generate_network_threshold(g, bn_weight)

    cc = list(new_g.edges())
    cc = sorted(cc, key=len)
    cc.reverse()

    largest_cc = nx.Graph()
    largest_cc.add_edges_from(cc[0])
    nx.draw_networkx(largest_cc, pos=pos, node_color='#bebada', with_labels=False, node_size=10)

    s_largest_cc = nx.Graph()
    s_largest_cc.add_edges_from(cc[1])
    nx.draw_networkx(s_largest_cc, pos=pos, node_color='#bebada', with_labels=False, node_size=10)

    bn = nx.Graph()
    bn.add_edge(bottleneck[0], bottleneck[1])
    nx.draw_networkx(bn, pos=pos, node_color='#f54242', with_labels=False, node_size=10)

    plt.legend()
    plt.show()

    return
