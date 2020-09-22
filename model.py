import networkx as nx
from read_file import *
import matplotlib.pyplot as plt

'''
This function is to generate a graph with data produced by read_file.py
'''


def generate_network(block_ids, dest_cbgs, threshold=0):
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(block_ids)
    # add edges
    for i in dest_cbgs:
        if dest_cbgs[i] < threshold:
            continue
        G.add_edge(*i, weight=dest_cbgs[i])

    return G


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
    scc = list(nx.strongly_connected_components(g))
    len_scc = list(map(len, scc))
    len_scc.sort().reverse()

    if len(len_scc) == 0:
        return 0, 0
    elif len(len_scc) == 1:
        return len_scc[0], 0
    else:
        return len_scc[0], len_scc[1]


# file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
# G = generate_network(*read_file(file, 25))
# print(num_g_sg(G))
