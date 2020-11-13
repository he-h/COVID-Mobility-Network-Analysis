from read_file import *
from model import *
import networkx as nx

# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362


class MSA:
    def __init__(self, date, id, device, dest):
        print(date, id)
        self.date = date
        self.id = id

        self.device_count = device
        self.g = generate_network(dest)

        self.flux = total_flux(self.g)

        # calculate qc and following features
        self.thresholds, self.num_g, self.num_sg = calc_g_sg(self.g)
        index_qc, index_qcb = l_sl_value(self.num_sg)

        self.gc_node_size = self.num_g[index_qc]
        self.qc = self.thresholds[index_qc]
        self.qcb = self.thresholds[index_qcb]
        self.g_perco = generate_network_threshold(self.g, self.qc)

        self.bottleneck = self.bottlenecks()

        self.indegree = []
        for i in self.g.nodes():
            self.indegree.append(self.g.degree(i))
        self.indegree_median = median(self.indegree)

    def __eq__(self, other):
        return self.date == other.date and self.id == other.id

    def plot_g_sg(self):
        figure, axis_1 = plt.subplots()

        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label='1st CC')
        axis_1.vlines(self.qc, 0, self.num_g[0], linestyles='-.', color='red', label='q_c')
        axis_1.vlines(self.qcb, 0, self.num_g[0], linestyles='-.', color='orange', label='q_{c2}')
        axis_1.set_xlabel('threshold')
        axis_1.set_ylabel('size')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_sg, color='palegreen', label='2nd CC')
        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title('Cluster'+str(self.id)+' '+str(self.date)+' size of cc')

        plt.savefig('results/'+str(self.id)+'/'+str(self.date)+'_size.png')
        return

    def plot_map(self):
        return

    def plot_hist(self):
        value = list()
        plt.figure()

        for i in self.g.edges():
            value.append(self.g.edges[i]['weight'])

        ax = sns.distplot(value)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Weights')

        plt.title('Cluster'+str(self.id)+' '+str(self.date)+' histogram')

        plt.savefig('results/'+str(self.id)+'/'+str(self.date)+'_hist.png')
        return


