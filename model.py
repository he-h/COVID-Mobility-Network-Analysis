import networkx as nx

'''
This function is to generate a graph with data produced by read_file.py
'''


def generate_d_network(block_ids, dest_cbgs):
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(block_ids)
    # add edges
    for i in dest_cbgs:
        G.add_edge(*i, weight=dest_cbgs[i])

    return G


'''
This function has almost same function as above but generate a undirected Graph
'''


def generate_network(block_ids, dest_cbgs, thershold=0):
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(block_ids)
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

    new_g.add_edges_from(g)

    edge_list = list(g.edges)
    for i, j in edge_list:
        if g.edges[i, j]['weight'] >= threshold:
            new_g.add_edge(i, j)

    return new_g


'''
this function is to generate percolation step of directed network with threshold
'''


def generate_d_network_threshold(g, threshold=0):
    new_g = nx.Graph()

    new_g.add_edges_from(g)

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

# file = 'data/01/01/2020-01-01-social-distancing.csv.gz'
# G = generate_network(*read_file(file, 25), 10)
# print(num_g_sg(G))
