from model import *
import matplotlib.pyplot as plt
from statistics import median
from matplotlib.lines import Line2D
import powerlaw
import json
import networkx as nx
import csv
import datetime as dt
# import geopandas as gpd

# 35620,"New York-Newark-Jersey City, NY-NJ-PA"
# 31080,"Los Angeles-Long Beach-Anaheim, CA"
# 16980,"Chicago-Naperville-Elgin, IL-IN-WI"
# 19100,"Dallas-Fort Worth-Arlington, TX"
# 26420,"Houston-The Woodlands-Sugar Land, TX"
# 47900,"Washington-Arlington-Alexandria, DC-VA-MD-WV"
# 33100,"Miami-Fort Lauderdale-Pompano Beach, FL"
# 37980,"Philadelphia-Camden-Wilmington, PA-NJ-DE-MD"
# 12060,"Atlanta-Sandy Springs-Alpharetta, GA"
# 38060,"Phoenix-Mesa-Chandler, AZ"


with open('data/MSAname.json', 'r') as o:
    name = json.load(o)


class MSA:
    def __init__(self, id, date, dest):
        # print(date, id)
        self.date = date
        self.id = id

        self.g = generate_network(dest)

        self.flux = total_flux(self.g)

        if self.flux == 0:
            self.qc = 0
            self.qcb = 0
            self.qca = 0
            self.qcf = 0
            self.edge_w_median = 0
            self.gc_node_size = 0
            self.thresholds = [0]
            return

        # calculate qc and following features

        self.thresholds, self.num_g, self.num_sg, self.num_r, self.dev_g, self.dev_sg, self.edge_size = calc_g_sg(self.g, 0, .1, final=10000)
        index_qc, index_qcb = l_sl_value(self.num_sg)
        self.index_qc = index_qc

        self.gc_node_size = self.num_g[index_qc]
        self.qc = self.thresholds[index_qc]
        self.qcb = self.thresholds[index_qcb]
        self.qca = self.thresholds[[i for i, j in enumerate(self.num_r) if j == max(self.num_r)][0]]
        self.qcf = self.thresholds[-1]

        # self.g_perco = generate_network_threshold(self.g, self.qc)
        #
        # self.bottleneck = calc_bottleneck_c(self.g, self.thresholds, self.qc)

        # self.indegree = []
        # for i in self.g.nodes():
        #     self.indegree.append(self.g.degree(i))
        # self.indegree_median = median(self.indegree)
        # self.indegree_25 = np.percentile(self.indegree, 25)
        # self.indegree_75 = np.percentile(self.indegree, 75)
        #
        self.edge_w = np.zeros(len(self.g.edges()))
        for j,i in enumerate(self.g.edges()):
            self.edge_w[j] = self.g.edges[i]['weight']
        self.edge_w_median = median(self.edge_w)
        self.edge_w_25 = np.percentile(self.edge_w, 25)
        self.edge_w_75 = np.percentile(self.edge_w, 75)
        self.edge_w_ave = self.flux/self.g.number_of_nodes()

        # dc = list(self.device_count.values())
        # self.device_median = median(dc)
        # self.device_25 = np.percentile(dc, 25)
        # self.device_75 = np.percentile(dc, 75)

        if self.id not in ['26420', '31080', '35620', '2060']:
            return
        with open(self.date.strftime('edge_list/%m_%d'+self.id+'_raw.csv'), 'w') as m:
            csvwriter = csv.writer(m)
            csvwriter.writerow(['from', 'to', 'weight'])
            for i, j in self.g.edges:
                csvwriter.writerow([i, j, self.g.edges[i, j]['weight']])

        with open(self.date.strftime('edge_list/MSA'+self.id+'%m_%d.csv'), 'w') as e:
            g = generate_network_threshold(self.g, self.qc)
            csvwriter = csv.writer(e)
            csvwriter.writerow(['from', 'to', 'edge', 'weight'])

            cc = list(nx.connected_components(g))
            cc.sort(key=len, reverse=True)
            ax = plt.gca()

            g0 = g.subgraph(cc[0])
            for i, j in g0.edges():
                csvwriter.writerow([i, j, 'gc', self.g.edges[i, j]['weight']])

            g1 = g.subgraph(cc[1])
            for i, j in g1.edges():
                csvwriter.writerow([i, j, 'sgc', self.g.edges[i, j]['weight']])

            g2 = g.subgraph(cc[2])
            for i, j in g2.edges():
                csvwriter.writerow([i, j, 'tgc', self.g.edges[i, j]['weight']])
            tmp = set()
            for i in cc[3:]:
                if len(i) > 1:
                    tmp |= i
            g3 = g.subgraph(tmp)
            for i, j in g3.edges():
                csvwriter.writerow([i, j, 'rest', self.g.edges[i, j]['weight']])

            bn1 = nx.Graph()
            self.bottleneck = calc_bn_set_diff(generate_network_threshold(self.g, self.qc-.25), generate_network_threshold(self.g, self.qc))
            self.bottleneck1 = calc_bn_set_diff(generate_network_threshold(self.g, self.qcb-.25), generate_network_threshold(self.g, self.qcb))
            bn1.add_edges_from(self.bottleneck1)
            for i, j in bn1.edges():
                csvwriter.writerow([i, j, 'bn', self.g.edges[i, j]['weight']])

            bn = nx.Graph()
            bn.add_edges_from(self.bottleneck)
            for i, j in bn.edges():
                csvwriter.writerow([i, j, 'sbn', self.g.edges[i, j]['weight']])

    def __eq__(self, other):
        return self.date == other.date and self.id == other.id

    def plot_g_sg(self):
        plt.clf()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        # axis_1.set_ylabel('GC Component size', color='dodgerblue')
        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label='GC')
        axis_1.tick_params(axis='y', colors='dodgerblue', labelsize=16)
        axis_1.tick_params(axis='x', labelsize=18)
        # axis_1.set_xlabel('thresholds', fontsize=18)

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_sg, color='grey', label='SGC')
        axis_2.tick_params(axis='y', colors='grey', labelsize=16)
        # axis_2.set_ylabel('SGC Component size', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2
        if self.date == dt.date(2020,2,1):
            if self.id == '31080':
                axis_1.legend(lines, labels, loc=0, prop={'size':21})
            plt.title(name[str(self.id)], fontsize=26)
        else:
            axis_1.set_xlabel('thresholds', fontsize=23)
        if self.id == '31080' or self.id == '26420':
            print(self.id + str(len(self.g.nodes)) + ' ' + str(self.num_sg[self.index_qc]))

        # axis_1.legend(lines, labels, loc=0, prop={'size':16})
        plt.xlim([0, 20])
        plt.xticks(fontsize=20)



        plt.savefig('results/'+str(self.id)+self.date.strftime('/%m/%d/')+self.date.strftime('%m_%d')+'_g_sg_size.jpg')

        return

    def plot_g_sg_device(self):
        plt.clf()
        figure, axis_1 = plt.subplots()

        axis_1.plot(self.thresholds, self.dev_sg, color='grey', label='SGC')
        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        axis_1.set_xlabel('thresholds')
        axis_1.set_ylabel('SGC device count', color='grey')

        axis_2 = axis_1.twinx()
        axis_2.set_ylabel('GC device count', color='dodgerblue')
        axis_2.plot(self.thresholds, self.dev_g, color='dodgerblue', label='GC')
        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title(name[str(self.id)] + ' ' + self.date.strftime('%m/%d'))

        plt.savefig('results/' + str(self.id) + self.date.strftime('/%m/%d/') + self.date.strftime('%m_%d') + '_g_sg_device.jpg')

        return

    def plot_g_sg_c(self):
        plt.clf()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qca, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.thresholds[-1], linestyle='-.', color='orange', label=r'$q_{c2}$')
        axis_1.set_ylabel('GC Component size', color='dodgerblue')
        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label='GC')
        axis_1.set_xlabel('thresholds')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_r, color='grey', label='RGC')
        axis_2.set_ylabel('Average rest Component size', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=1)

        plt.title(name[str(self.id)] + ' ' + self.date.strftime('%m/%d'))

        plt.savefig('results/' + str(self.id) + self.date.strftime('/%m/%d/') + self.date.strftime('%m_%d') + '_g_rg_size.jpg')

        return

    def plot_hist(self):
        plt.clf()


        powerlaw.plot_ccdf(self.edge_w, linestyle='-', color='#2b8cbe', label='CCDF')
        plt.ylabel('CCDF')
        plt.xlabel(r'$W_{ij}')



        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' CCDF')
        plt.savefig('results/' + str(self.id) + self.date.strftime('/%m/%d/') + self.date.strftime('%m_%d') + '_hist.jpg')

        return
