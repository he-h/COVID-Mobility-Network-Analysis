import networkx as nx
import numpy as np

max_w = 40


'''
This function is to generate a graph with data produced by read_file.py
'''


def generate_d_network(dest_cbgs):
    G = nx.DiGraph()
    # add edges
    for i in dest_cbgs:
        G.add_edge(*i, weight=dest_cbgs[i])

    return G


'''
This function has almost same function as above but generate a undirected Graph
'''


def generate_network(dest_cbgs):
    G = nx.Graph()
    # add edges
    for i, j in dest_cbgs.keys():
        if (i, j) not in G.edges:
            G.add_edge(i, j, weight=dest_cbgs[i, j])
        else:
            weight = dest_cbgs[i, j] + G.edges[i, j]['weight']
            G.add_edge(i, j, weight=weight)

    return G


'''
this function is to generate percolation step of undirected network with threshold
'''


def generate_network_threshold(g, threshold=0):
    new_g = nx.Graph()

    edge_list = list(g.edges)
    for i, j in edge_list:
        weight = g.edges[i, j]['weight']
        if weight >= threshold:
            new_g.add_edge(i, j, weight=weight)

    return new_g


'''
this function is to generate percolation step of directed network with threshold
'''


def generate_d_network_threshold(g, threshold=0):
    new_g = nx.Graph()

    edge_list = list(g.edges)
    for i, j in edge_list:
        if g.edges[i, j]['weight'] >= threshold:
            new_g.add_edge(i, j)

    return new_g


'''
This function is find max weight of a graph
'''


def max_weight(g):
    m_weight = 0
    for i in g.edges:
        weight = g.edges[i[0], i[1]]['weight']
        if weight > m_weight:
            m_weight = weight

    return m_weight


'''
This function is to return the number of elements in the largest and second largest SCC
'''


def num_g_sg(g):
    if type(g) == nx.classes.digraph.DiGraph:
        scc = list(nx.strongly_connected_components(g))
    else:
        scc = list(nx.connected_components(g))

    len_scc = list(map(len, scc))
    len_scc.sort()
    len_scc.reverse()

    if len(len_scc) == 0:
        return 0, 0
    elif len(len_scc) == 1:
        return len_scc[0], 0
    else:
        return len_scc[0], len_scc[1]


'''
This function finds the largest and second largest before the largest value
'''


def l_sl_value(list):
    l = [i for i, j in enumerate(list) if j == max(list)][0]
    sublist = list[:l]
    sl = [i for i, j in enumerate(sublist) if j == max(sublist)][0]

    return l, sl


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(g):
    # setting thresholds
    thresholds = np.arange(4, max_w, 0.25)

    num_g = []
    num_sg = []
    for i in thresholds:
        tmp_g, tmp_sg = num_g_sg(generate_network_threshold(g, i))
        num_g.append(tmp_g)
        num_sg.append(tmp_sg)

    return thresholds, num_g, num_sg


'''
This function is to find the bottleneck by analyzing the threshold around when the second SCC is the largest
'''


def calc_bottleneck(g, thresholds, num_sg):
    max_index = [i for i, j in enumerate(num_sg) if j == max(num_sg)][0]
    bn_weight_b = thresholds[max_index]
    interval = thresholds[1] - thresholds[0]
    bn = []

    G_sg_largest = generate_network_threshold(g, bn_weight_b)

    if type(G_sg_largest) == nx.classes.digraph.DiGraph:
        scc = list(nx.strongly_connected_components(G_sg_largest))
    else:
        scc = list(nx.connected_components(G_sg_largest))

    scc.sort(key=lambda a: len(a))
    scc_sg_largest = scc[-1]
    scc_sg_s_largest = scc[-2]

    for i, j in g.edges():
        if bn_weight_b - interval < g.edges[(i, j)]['weight'] <= bn_weight_b:
            if (i in scc_sg_largest and j in scc_sg_s_largest) or (j in scc_sg_largest and i in scc_sg_s_largest):
                bn.append((i, j))

    return bn, bn_weight_b


'''
This function is to find the bottleneck by analyzing the threshold around when the second SCC is the largest
'''


def calc_bottleneck_c(g, thresholds, qc):
    interval = thresholds[1] - thresholds[0]
    bn = set()

    G_sg_largest = generate_network_threshold(g, qc)

    if type(G_sg_largest) == nx.classes.digraph.DiGraph:
        scc = list(nx.strongly_connected_components(G_sg_largest))
    else:
        scc = list(nx.connected_components(G_sg_largest))

    scc.sort(key=len)
    scc_sg_largest = scc[-1]
    scc_sg_s_largest = scc[-2]

    for i, j in g.edges():
        if qc - interval < g.edges[(i, j)]['weight'] <= qc:
            if (i in scc_sg_largest and j in scc_sg_s_largest) or (j in scc_sg_largest and i in scc_sg_s_largest):
                bn.add((i, j))

    return bn


'''
This function calculates the total flux of a graph
'''


def total_flux(g):
    flux = 0
    for i in g.edges():
        flux += g.edges[i]['weight']

    return flux


# file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
# G = generate_network(*read_file(file, 25), 10)
# print(num_g_sg(G))
