import networkx as nx
from read_file import *
import matplotlib.pyplot as plt

'''
This function is to generate a graph with data produced by read_file.py
'''


def generate_network(block_ids, dest_cbgs):
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(block_ids)
    # add edges
    for i in dest_cbgs:
        G.add_edge(*i, weight=dest_cbgs[i])

    return G


# file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
# G = generate_network(*read_file(file))
# nx.draw(G)
