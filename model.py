import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


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
    new_g.add_nodes_from(g.nodes)

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


def num_g_sg(scc):

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


def l_sl_value(li):
    if len(li) == 0:
        return 0,0
    l = [i for i, j in enumerate(li) if j == max(li)][0]
    sublist = li[:l]
    if l == 0:
        sl = 0
    else:
        sl = [i for i, j in enumerate(sublist) if j == max(sublist)][0]

    return l, sl


'''
This function is to calculate the number of elements in largest and second largest SCC changing with thresholds
'''


def calc_g_sg(g, start, interval, d1=None, final=100):
    node_size = len(g.nodes())
    tmp_g = node_size

    tmp_t = start
    thresholds = []
    num_g = []
    num_sg = []
    dev_g = []
    dev_sg = []
    num_rest = []
    lens=[]

    while tmp_g > node_size/final and tmp_g != 1:

        tmp_n = generate_network_threshold(g, tmp_t)
        lens.append(len(tmp_n.edges))
        scc = sorted(list(nx.connected_components(tmp_n)), key=len, reverse=True)
        tmp_g, tmp_sg = num_g_sg(scc)
        num_g.append(tmp_g)
        num_sg.append(tmp_sg)
        if len(scc) < 2:
            num_rest.append(0)
        else:
            num_rest.append(sum(map(len, scc[1:]))/(len(scc)-1))

        thresholds.append(tmp_t)
        if final != 100 and tmp_t > 20:
            break

        if interval > 1 and tmp_t < 100:
            tmp_t += 1
        else:
            tmp_t += interval

        if d1 is None:
            continue
        if len(scc) != 0:
            dev_g.append(sum_device(scc[0], d1))
            if len(scc) == 1:
                dev_sg.append(0)
            else:
                dev_sg.append(sum_device(scc[1], d1))
        else:
            dev_sg.append(0)
            dev_g.append(0)

    return np.array(thresholds), np.array(num_g), np.array(num_sg), np.array(num_rest), np.array(dev_g), np.array(dev_sg), np.array(lens)


'''
This function calculate the sum of device in GC and SGC
'''


def sum_device(nodes, d1):
    s = 0
    for i in nodes:
        if i in d1.keys():
          s += d1[i]

    return s


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

    scc.sort(key=len)
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
    if len(scc) == 1:
        return set()
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


'''
This function returns latitude and longitude of a point
'''


def get_xy(pt):
    return [pt.x, pt.y]


# file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
# G = generate_network(*read_file(file, 25), 10)
# print(num_g_sg(G))

# def bottlenecks(self):
#     g_perco_b = generate_network_threshold(self.g, self.qc - .25)
#     s_cc = sorted(list(nx.connected_components(self.g_perco)), key=len, reverse=True)[1]
#     l_cc = sorted(list(nx.connected_components(g_perco_b)), key=len, reverse=True)[0]
#     l_cc = l_cc.difference(s_cc)
#
#     bc = set()
#
#     for i, j in g_perco_b.edges():
#         if self.qc - .25 <= g_perco_b.edges[i, j]['weight'] < self.qc:
#             if (i in s_cc and j in l_cc) or (i in l_cc and j in s_cc):
#                 bc.add((i, j))
#
#     return bc

def calc_bn_set_diff(g_b, g):
    bn = set()
    g_b_1 = g_b.subgraph(sorted(list(nx.connected_components(g_b)), key=len, reverse=True)[0])
    g_b_link = set(g_b_1.edges())
    tmp = sorted(list(nx.connected_components(g)), key=len, reverse=True)
    g_1, g_2 = tmp[0], tmp[1]
    tmp_0 = set()
    tmp_1 = set()

    for i, j in g_b_link.difference(set(g.edges())):
        if (i in g_1 and j in g_1) or (i in g_2 and j in g_2):
            continue

        if g_b_1.degree(i) == 1 or g_b_1.degree(j) == 1:
            continue

        if (i in g_2 and j in g_1) or (i in g_2 and j in g_1):
            bn.add((i,j))
            continue

        if (i in g_1) or (j in g_1):
            tmp_0.add((i,j))

        if (i in g_2) or (j in g_2):
            tmp_1.add((i,j))

    for i,j in tmp_0:
        for k in tmp_1:
            if i in k or j in k:
                bn.add((i,j))
                bn.add(k)

    return bn


def select(dic, num):
    tmp = set()
    for i in dic.keys():
        if dic[i] > num:
            tmp.add(str(i))

    return tmp
