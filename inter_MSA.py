from model import *
from plot import *
import powerlaw
from statistics import median
from matplotlib.lines import Line2D
from read_file import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import json


# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362

with open('data/pos.json', 'r') as o:
    pos = json.load(o)


class InterMsaG:
    # def __init__(self, date):#, msa_qc):
    #     print(date)
    #     self.date = date
    #     # self.msa_qc = msa_qc
    #
    #     dest = pd.read_csv(process_data_str(self.date)+'inter_msa_edge.csv')
    #
    #     device = pd.read_csv(process_data_str(self.date)+'inter_msa_device.csv')
    #     self.device_count = {}
    #     for i in device.index:
    #         self.device_count[device['msa'][i]] = device['device'][i]
    #     self.g = nx.from_pandas_edgelist(dest, 'from', 'to', 'weight', nx.Graph())
    #
    #     self.setup()

    def __init__(self, date, dest, device):#, qc):
        print(date)
        self.date = date
        self.device_count = device
        self.g = generate_network(dest)
        # self.msa_qc = qc
        self.setup()

    def setup(self):
        self.flux = total_flux(self.g)
        self.sum_device = sum(self.device_count.values())

        # calculate qc and following features

        self.thresholds, self.num_g, self.num_sg, self.num_r, self.dev_g, self.dev_sg, self.edge_size = calc_g_sg(self.g, 10, 2.5, self.device_count)
        index_qc, index_qcb = l_sl_value(self.num_sg)
        interval = self.thresholds[1] - self.thresholds[0]

        self.gc_node_size = self.num_g[index_qc]
        self.qc = self.thresholds[index_qc]
        self.qcb = self.thresholds[index_qcb]
        self.qcc = self.thresholds[[i for i, j in enumerate(self.num_r) if j == max(self.num_r)][0]]

        self.g_perco = generate_network_threshold(self.g, self.qc)
        self.g_perco_1 = generate_network_threshold(self.g, self.qcb)

        # self.bottleneck = calc_bottleneck_c(self.g, self.thresholds, self.qc)
        # self.bottleneck1 = calc_bottleneck_c(self.g, self.thresholds, self.qcb)
        self.bottleneck = calc_bn_set_diff(generate_network_threshold(self.g, self.qc-interval), generate_network_threshold(self.g, self.qc))
        self.bottleneck1 = calc_bn_set_diff(generate_network_threshold(self.g, self.qcb-interval), generate_network_threshold(self.g, self.qcb))

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

        dc = list(self.device_count.values())
        self.device_median = median(dc)
        self.device_25 = np.percentile(dc, 25)
        self.device_75 = np.percentile(dc, 75)

        self.qc_setup()

        # self.plot_map(self.g_perco, 1)
        # self.plot_map(self.g_perco_1, 0)

    def qc_setup(self):
        self.qc_m = dict()
        self.qca_m = dict()
        self.qcf_m = dict()

        df = pd.read_csv(qc_str(self.date))
        for i in df.index:
            self.qc_m[df['msa'][i]] = df['qc'][i]
            self.qca_m[df['msa'][i]] = df['qca'][i]
            self.qcf_m[df['msa'][i]] = df['qcf'][i]

    def __eq__(self, other):
        return self.date == other.date

    def result_dir(self):
        return 'results/interMSA/'+aug_str(self.date.month)+'/'+aug_str(self.date.day) + '/'

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

        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' percolation component size')

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_sg_size.png')
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

        axis_1.legend(lines, labels, loc=0)

        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' continuous component size')

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_rg_size.png')
        return

    def plot_hist(self):
        plt.figure()

        fit = powerlaw.Fit(self.edge_w)
        fig2 = fit.plot_pdf(color='peachpuff')

        fit.plot_ccdf(color='royalblue', linewidth=2, ax=fig2)

        fit.power_law.plot_ccdf(color='cornflowerblue', linestyle='--', ax=fig2)
        labels = ['CCDF', 'PDF']
        colors = ['royalblue', 'peachpuff']
        lines = [Line2D([0], [0], color=c, linewidth=2, alpha=0.85) for c in colors]
        plt.legend(lines, labels)
        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' CCDF')
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_hist.png')
        return

    def plot_g_sg_device(self):
        plt.figure()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.set_ylabel('GC device count', color='dodgerblue')
        axis_1.plot(self.thresholds, self.dev_g, color='dodgerblue', label='GC')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        axis_1.set_xlabel('thresholds')
        axis_1.set_ylabel('SGC device count', color='grey')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.dev_sg, color='grey', label='SGC')
        axis_2.set_ylabel('SGC device count', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' percolation device count')

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_sg_device.png')
        return

    def plot_msa_qc(self):
        plt.figure()

        th = np.arange(1, 50, .5)
        remain_msa = []

        for i in th:
            tmp = 0
            for j in self.qc_m.keys():
                if i < self.qc_m[j]:
                    tmp += self.device_count[j]
            remain_msa.append(tmp)

        plt.plot(th, remain_msa, color='royalblue')
        plt.grid(True)
        plt.xlabel('Thresholds')
        plt.ylabel('device count')

        plt.title('Sum of remaining MSAs device count ' + self.date.strftime('%m/%d'))
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_MSAs_device.png')
        return

    def plot_qc_map(self):
        plt.figure()

        m = Basemap(
            projection='merc',
            llcrnrlon=-130,
            llcrnrlat=25,
            urcrnrlon=-60,
            urcrnrlat=50,
            lat_ts=0,
            resolution='i',
            suppress_ticks=True)

        m.drawcountries(linewidth=3)
        m.drawstates(linewidth=0.2)
        m.drawcoastlines(linewidth=1)
        m.fillcontinents(alpha=0.3)
        # m.drawcounties(linewidth=0.1)

        x, y = [], []
        for i in pos.keys():
            x.append(pos[i][0])
            y.append(pos[i][1])
        mx, my = m(x, y)
        pos1 = dict()
        for i, j in enumerate(pos.keys()):
            pos1[j] = (mx[i], my[i])

        msas = {0:[], 10:[], 20:[], 30:[], 40:[]}
        for i in self.qc_m.keys():
            j = str(i)
            if self.qc_m[i] > 40:
                msas[40].append(j)
            elif self.qc_m[i] > 30:
                msas[30].append(j)
            elif self.qc_m[i] > 20:
                msas[20].append(j)
            elif self.qc_m[i] > 10:
                msas[10].append(j)
            else:
                msas[0].append(j)

        colors = ['wheat', 'gold', 'orange', 'darkorange', 'red']

        iter=0
        for i in msas.keys():
            tmp = nx.Graph()
            tmp.add_nodes_from(msas[i])
            nx.draw_networkx_nodes(G=tmp, pos=pos1, nodelist=tmp.nodes(), node_color=colors[iter], label=">"+str(i),
                                   node_size=[(self.device_count[i]/250)**(1/2) for i in tmp.nodes()])
            iter += 1

        plt.legend()
        plt.title('MSA qc map ' + self.date.strftime('%m/%d'))
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_MSAs_qc_map.png')
        return

    def plot_map(self, g):
        plt.figure()
        m = Basemap(
            projection='merc',
            llcrnrlon=-130,
            llcrnrlat=25,
            urcrnrlon=-60,
            urcrnrlat=50,
            lat_ts=0,
            resolution='i',
            suppress_ticks=True)

        m.drawcountries(linewidth=3)
        m.drawstates(linewidth=0.2)
        m.drawcoastlines(linewidth=1)
        m.fillcontinents(alpha=0.3)
        # m.drawcounties(linewidth=0.1)

        x, y = [], []
        for i in pos.keys():
            x.append(pos[i][0])
            y.append(pos[i][1])
        mx, my = m(x, y)
        pos1 = dict()
        for i, j in enumerate(pos.keys()):
            pos1[j] = (mx[i], my[i])

        cc = list(nx.connected_components(g))
        cc.sort(key=len, reverse=True)
        ax = plt.gca()

        g0 = g.subgraph(cc[0])
        nx.draw_networkx_nodes(G=g0, node_color='cornflowerblue', nodelist=g0.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i]/250)**(1/2) for i in g0.nodes()])
        for i, j in g0.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='cornflowerblue',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        g1 = g.subgraph(cc[1])
        nx.draw_networkx_nodes(G=g1, node_color='lightgreen', nodelist=g1.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i]/250)**(1/2) for i in g1.nodes()])
        for i, j in g1.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='lightgreen',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        g2 = g.subgraph(cc[2])
        nx.draw_networkx_nodes(G=g2, node_color='peachpuff', nodelist=g2.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i] / 250) ** (1 / 2) for i in g2.nodes()])
        for i, j in g2.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='peachpuff',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        tmp = set()
        for i in cc[3:]:
            if len(i) > 1:
                tmp |= i
        g3 = g.subgraph(tmp)
        nx.draw_networkx_nodes(G=g3, node_color='silver', nodelist=g3.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i]/250) ** (1 / 2) for i in g3.nodes()])
        for i, j in g3.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='silver',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        bn1 = nx.Graph()
        bn1.add_edges_from(self.bottleneck1)
        nx.draw_networkx_nodes(G=bn1, node_color='gold', nodelist=bn1.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i] / 250) ** (1 / 2) for i in bn1.nodes()])
        for i, j in bn1.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='gold',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        bn = nx.Graph()
        bn.add_edges_from(self.bottleneck)
        nx.draw_networkx_nodes(G=bn, node_color='r', nodelist=bn.nodes(), pos=pos1, alpha=1,
                               node_size=[(self.device_count[i]/250) ** (1 / 2) for i in bn.nodes()])
        for i, j in bn.edges():
            ax.annotate("",
                        xy=pos1[i], xycoords='data',
                        xytext=pos1[j], textcoords='data',
                        arrowprops=dict(arrowstyle="-", color='r',
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=0.3",
                                        ),
                        )

        labels = ['GC', 'SGC', 'TGC', 'Bottleneck(GC)', 'Bottleneck(non GC)', 'Rest']
        colors = ['cornflowerblue', 'lightgreen', 'peachpuff', 'r', 'gold', 'silver']
        lines = [Line2D([0], [0], color=c, linewidth=2, alpha=0.85) for c in colors]
        plt.tight_layout()
        plt.legend(lines, labels, fontsize=7, loc=4)
        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' map')
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_map.png')

        return

    def plot_w_qc_perco(self):
        colors = ['wheat', 'gold', 'orange', 'darkorange', 'red']

        color_c = {}
        for i in self.qc_m.keys():
            j = str(i)
            if self.qc_m[i] > 40:
                color_c[j] = 'red'
            elif self.qc_m[i] > 30:
                color_c[j] = 'darkorange'
            elif self.qc_m[i] > 20:
                color_c[j] = 'orange'
            elif self.qc_m[i] > 10:
                color_c[j] = 'gold'
            else:
                color_c[j] = 'wheat'

        for i in range(0, 50, 10):
            tmp_nodes = select(self.qc_m, i)
            qc_g = self.g.subgraph(tmp_nodes)
            for j in range(0, 500, 100):
                if i == j == 0:
                    continue
                tmp_g = generate_network_threshold(qc_g, j)
                plot_qc_map(tmp_g, 'qc', color_c, self.device_count, pos, i, j, self.date)

        color_c = {}
        for i in self.qca_m.keys():
            j = str(i)
            if self.qca_m[i] > 40:
                color_c[j] = 'red'
            elif self.qca_m[i] > 30:
                color_c[j] = 'darkorange'
            elif self.qca_m[i] > 20:
                color_c[j] = 'orange'
            elif self.qca_m[i] > 10:
                color_c[j] = 'gold'
            else:
                color_c[j] = 'wheat'

        for i in range(0, 50, 10):
            tmp_nodes = select(self.qca_m, i)
            qc_g = self.g.subgraph(tmp_nodes)
            for j in range(0, 500, 100):
                if i == j == 0:
                    continue
                tmp_g = generate_network_threshold(qc_g, j)
                plot_qc_map(tmp_g, 'qca', color_c, self.device_count, pos, i, j, self.date)

        color_c = {}
        for i in self.qcf_m.keys():
            j = str(i)
            if self.qcf_m[i] > 200:
                color_c[j] = 'red'
            elif self.qcf_m[i] > 150:
                color_c[j] = 'darkorange'
            elif self.qcf_m[i] > 100:
                color_c[j] = 'orange'
            elif self.qcf_m[i] > 50:
                color_c[j] = 'gold'
            else:
                color_c[j] = 'wheat'

        for i in range(0, 200, 50):
            tmp_nodes = select(self.qcf_m, i)
            qc_g = self.g.subgraph(tmp_nodes)
            for j in range(0, 500, 100):
                if i == j == 0:
                    continue
                tmp_g = generate_network_threshold(qc_g, j)
                plot_qc_map(tmp_g, 'qcf', color_c, self.device_count, pos, i, j, self.date)

        return
