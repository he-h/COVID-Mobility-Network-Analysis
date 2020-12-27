from model import *
import matplotlib.pyplot as plt
from statistics import median
from matplotlib.lines import Line2D
import powerlaw
import json
import networkx as nx
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

# https://www.nature.com/articles/nature09182?page=19
# https://arxiv.org/pdf/0903.3178.pdf

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
            print(id)
            self.qc = 0
            self.qcb = 0
            self.qcc = 0
            self.thresholds = [0]
            return

        # calculate qc and following features

        self.thresholds, self.num_g, self.num_sg, self.num_r, self.dev_g, self.dev_sg, self.edge_size = calc_g_sg(self.g, 2, .25)
        index_qc, index_qcb = l_sl_value(self.num_sg)

        self.gc_node_size = self.num_g[index_qc]
        self.qc = self.thresholds[index_qc]
        self.qcb = self.thresholds[index_qcb]
        self.qcc = self.thresholds[[i for i, j in enumerate(self.num_r) if j == max(self.num_r)][0]]

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
        # self.edge_w = []
        # for i in self.g.edges():
        #     self.edge_w.append(self.g.edges[i]['weight'])
        # self.edge_w_median = median(self.edge_w)
        # self.edge_w_25 = np.percentile(self.edge_w, 25)
        # self.edge_w_75 = np.percentile(self.edge_w, 75)
        # self.edge_w_ave = self.flux/self.g.number_of_nodes()
        #
        # dc = list(self.device_count.values())
        # self.device_median = median(dc)
        # self.device_25 = np.percentile(dc, 25)
        # self.device_75 = np.percentile(dc, 75)

    def __eq__(self, other):
        return self.date == other.date and self.id == other.id

    def plot_g_sg(self):
        plt.figure()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        axis_1.set_ylabel('GC Component size', color='dodgerblue')
        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label='GC')
        axis_1.set_xlabel('thresholds')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_sg, color='grey', label='SGC')
        axis_2.set_ylabel('SGC Component size', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title(name[str(self.id)]+' '+self.date.strftime('%m/%d'))

        plt.savefig('results/'+str(self.id)+'/'+self.date.strftime('%m_%d')+'_g_sg_size.png')
        return

    def plot_g_sg_device(self):
        plt.figure()
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

        plt.savefig('results/' + str(self.id) + '/' + self.m + '_g_sg_device.png')
        return

    def plot_g_sg_c(self):
        plt.figure()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qcc, linestyle='-.', color='red', label=r'$q_c$')
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

        plt.savefig('results/' + str(self.id) + '/' + self.date.strftime('%m_%d') + '_g_rg_size.png')
        return
