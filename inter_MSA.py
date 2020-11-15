from model import *
import powerlaw
from statistics import median
from read_file import *
import matplotlib.pyplot as plt


# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362


class InterMsaG:
    def __init__(self, date, device, dest, msa_qc):
        print(date)
        self.date = date
        self.msa_qc = msa_qc

        self.device_count = device
        self.sum_device = sum(device.values())
        self.g = generate_network(dest)

        self.flux = total_flux(self.g)

        # calculate qc and following features
        self.thresholds = np.arange(1, 150, 1)

        self.num_g, self.num_sg, self.dev_g, self.dev_sg = calc_g_sg(self.g, self.thresholds)
        index_qc, index_qcb = l_sl_value(self.num_sg)

        self.gc_node_size = self.num_g[index_qc]
        self.qc = self.thresholds[index_qc]
        self.qcb = self.thresholds[index_qcb]
        self.g_perco = generate_network_threshold(self.g, self.qc)

        self.bottleneck = calc_bottleneck_c(self.g, self.thresholds, self.qc)

        self.indegree = []
        for i in self.g.nodes():
            self.indegree.append(self.g.degree(i))
        self.indegree_median = median(self.indegree)
        self.indegree_25 = np.percentile(self.indegree, 25)
        self.indegree_75 = np.percentile(self.indegree, 75)

        self.edge_w = []
        for i in self.g.edges():
            self.edge_w.append(self.g.edges[i]['weight'])
        self.edge_w_median = median(self.edge_w)
        self.edge_w_25 = np.percentile(self.edge_w, 25)
        self.edge_w_75 = np.percentile(self.edge_w, 75)
        self.edge_w_ave = self.flux / self.g.number_of_nodes()

    def __eq__(self, other):
        return self.date == other.date

    def plot_g_sg(self):
        plt.figure()
        figure, axis_1 = plt.subplots()

        axis_1.plot(self.thresholds, self.num_sg, color='grey', label='SGC')
        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        axis_1.set_xlabel('thresholds')
        axis_1.set_ylabel('SGC Component size', color='grey')

        axis_2 = axis_1.twinx()
        axis_2.set_ylabel('GC Component size', color='dodgerblue')
        axis_2.plot(self.thresholds, self.num_g, color='dodgerblue', label='GC')
        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title('Inter MSA ' + str(self.date) + ' percolation component size')

        plt.savefig('results/interMSA/' + str(self.date) + '_g_sg_size.png')
        return

    def plot_map(self):
        return

    def plot_hist(self):
        plt.figure()

        fit = powerlaw.Fit(self.edge_w)

        fit.plot_ccdf(color='royalblue', linewidth=2)

        fit.power_law.plot_ccdf(color='cornflowerblue', linestyle='-')
        plt.title('Inter MSA ' + str(self.date) + ' CCDF')
        plt.savefig('results/interMSA/' + str(self.date) + '_hist.png')
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

        plt.title('Inter MSA ' + str(self.date) + ' percolation device count')

        plt.savefig('results/interMSA/' + str(self.date) + '_g_sg_device.png')
        return

    def plot_msa_qc(self):
        plt.figure()

        th = np.arange(1, 25, .25)
        remain_msa = []

        for i in th:
            tmp = 0
            for j in self.msa_qc.keys():
                if i < self.msa_qc[i]:
                    tmp += self.device_count[j]
            remain_msa.append(tmp)

        plt.plot(th, remain_msa)
        plt.grid(True)
        plt.xlabel('Thresholds')
        plt.ylabel('device count')

        plt.title('Sum of remaining MSAs device count ' + str(self.date))
        plt.savefig('results/interMSA/' + str(self.date) + '_MSAs_device.png')
        return
