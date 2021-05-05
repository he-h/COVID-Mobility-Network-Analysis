from model import *
from plot import *
import powerlaw
from statistics import median
from matplotlib.lines import Line2D
from read_file import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import json
import csv
import os
from haversine import haversine


# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362

with open('data/pos.json', 'r') as o:
    pos = json.load(o)


def largest_size_qc(g, device_count):
    thresholds, num_g, num_sg, num_r, dev_g, dev_sg, edge_size = calc_g_sg(g, 10, 2.5, device_count)
    index_qc, index_qcb = l_sl_value(num_sg)

    if len(num_g) == 0:
        return 0, 0

    gc_node_size = num_g[index_qc]
    qc = thresholds[index_qc]

    return gc_node_size, qc


class InterMsaG:

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
        self.qca = self.thresholds[[i for i, j in enumerate(self.num_r) if j == max(self.num_r)][0]]
        self.qcf = self.thresholds[-1]

        g_perco = generate_network_threshold(self.g, self.qc)

        # self.g_perco_1 = generate_network_threshold(self.g, self.qcb)

        # self.bottleneck = calc_bottleneck_c(self.g, self.thresholds, self.qc)
        # self.bottleneck1 = calc_bottleneck_c(self.g, self.thresholds, self.qcb)
        self.bottleneck = calc_bn_set_diff(generate_network_threshold(self.g, self.qc-interval), generate_network_threshold(self.g, self.qc))
        self.bottleneck1 = calc_bn_set_diff(generate_network_threshold(self.g, self.qcb-interval), generate_network_threshold(self.g, self.qcb))
        # self.plot_map(g_perco)

        self.indegree = []
        for i in self.g.nodes():
            self.indegree.append(self.g.degree(i))
        self.indegree_median = median(self.indegree)
        self.indegree_25 = np.percentile(self.indegree, 25)
        self.indegree_75 = np.percentile(self.indegree, 75)

        self.edge_w = np.zeros(len(self.g.edges()))
        for j,i in enumerate(self.g.edges()):
            self.edge_w[j] = self.g.edges[i]['weight']
        self.edge_w_median = median(self.edge_w)
        self.edge_w_25 = np.percentile(self.edge_w, 25)
        self.edge_w_75 = np.percentile(self.edge_w, 75)
        self.edge_w_ave = self.flux / self.g.number_of_nodes()

        self.distances = []
        for i, j in self.g.edges:
            dis = haversine(pos[i], pos[j])
            self.distances += [dis]*int(self.g.edges[i,j]['weight'])
        self.distances = np.array(self.distances)

        dc = np.array(list(self.device_count.values()))
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

    def result_dir(self):
        return 'results/interMSA/'+aug_str(self.date.month)+'/'+aug_str(self.date.day) + '/'

    def plot_g_sg(self):
        plt.clf()
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

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_sg_size.jpg')
        
        return

    def plot_g_sg_log(self):
        plt.clf()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qc, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.qcb, linestyle='-.', color='orange', label=r'$q_{c2}$')
        # axis_1.set_ylabel('GC Component size', color='dodgerblue')
        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label=r'$1_{st} CC$')
        # axis_1.set_xlabel('thresholds', fontsize=18)
        axis_1.tick_params(axis='y', colors='dodgerblue')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_sg, color='grey', label=r'$2_{nd} CC$')
        # axis_2.set_ylabel('SGC Component size', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2
        if self.date == dt.date(2020,2,1):
            axis_1.legend(lines, labels, loc=0, prop={'size':17})
            plt.title('Inter MSA percolation', fontsize=22)
        else:
            axis_1.set_xlabel('thresholds', fontsize=18)

        plt.xscale('log')

        # plt.title('Inter MSA percolation', fontsize=22)

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_sg_log_size.jpg')
        
        return

    def plot_g_sg_c(self):
        plt.clf()
        figure, axis_1 = plt.subplots()

        axis_1.axvline(self.qca, linestyle='-.', color='red', label=r'$q_c$')
        axis_1.axvline(self.thresholds[-1], linestyle='-.', color='orange', label=r'$q_{c2}$')
        # axis_1.set_ylabel('GC Component size', color='dodgerblue')
        axis_1.plot(self.thresholds, self.num_g, color='dodgerblue', label='GC')
        # axis_1.set_xlabel('thresholds')

        axis_2 = axis_1.twinx()
        axis_2.plot(self.thresholds, self.num_r, color='grey', label='RGC')
        # axis_2.set_ylabel('Average rest Component size', color='grey')

        lines_1, labels_1 = axis_1.get_legend_handles_labels()
        lines_2, labels_2 = axis_2.get_legend_handles_labels()

        lines = lines_1 + lines_2
        labels = labels_1 + labels_2

        axis_1.legend(lines, labels, loc=0)

        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' continuous component size')

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_rg_size.jpg')
        
        return

    def plot_hist(self):
        plt.clf()

        powerlaw.plot_ccdf(self.edge_w, linestyle='-', color='#2b8cbe', label='CCDF')
        plt.ylabel('CCDF')
        plt.xlabel(r'$W_{ij}$')

        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' CCDF')
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_hist.jpg')
        
        return

    def plot_g_sg_device(self):
        plt.clf()
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

        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_g_sg_device.jpg')
        
        return

    def plot_msa_qc(self):
        plt.clf()

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
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_MSAs_device.jpg')
        
        return

    def plot_qc_map(self):
        plt.clf()
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        m = Basemap(
            projection='merc',
            llcrnrlon=-130,
            llcrnrlat=25,
            urcrnrlon=-60,
            urcrnrlat=50,
            lat_ts=0,
            resolution='i',
            suppress_ticks=True)

        m.readshapefile('tl_2017_us_state/tl_2017_us_state', 'states', drawbounds=True)

        x, y = [], []
        for i in pos.keys():
            x.append(pos[i][0])
            y.append(pos[i][1])
        mx, my = m(x, y)
        pos1 = dict()
        for i, j in enumerate(pos.keys()):
            pos1[j] = (mx[i], my[i])

        msas = {0:[], 3:[], 6:[], 9:[], 12:[]}
        for i in self.qc_m.keys():
            j = str(i)
            if self.qc_m[i] > 12:
                msas[12].append(j)
            elif self.qc_m[i] > 9:
                msas[9].append(j)
            elif self.qc_m[i] > 6:
                msas[6].append(j)
            elif self.qc_m[i] > 3:
                msas[3].append(j)
            else:
                msas[0].append(j)

        colors = ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000']

        iter=0
        for i in msas.keys():
            tmp = nx.Graph()
            tmp.add_nodes_from(msas[i])
            nx.draw_networkx_nodes(G=tmp, pos=pos1, nodelist=tmp.nodes(), node_color=colors[iter], label=r"$q_c$>"+str(i),
                                   node_size=[(self.device_count[i]/250)**(1/2) for i in tmp.nodes()])
            iter += 1

        plt.legend()
        plt.title('MSA qc map ' + self.date.strftime('%m/%d'))
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_MSAs_qc_map.jpg')
        
        return

    def plot_map(self, g):
        plt.clf()
        m = Basemap(
            projection='merc',
            llcrnrlon=-130,
            llcrnrlat=25,
            urcrnrlon=-60,
            urcrnrlat=50,
            lat_ts=0,
            resolution='i',
            suppress_ticks=True)

        # m.drawcountries(linewidth=3)
        # m.drawstates(linewidth=0.2)
        # m.drawcoastlines(linewidth=1)
        # m.fillcontinents(alpha=0.3)
        # m.drawcounties(linewidth=0.1)
        m.readshapefile('tl_2017_us_state/tl_2017_us_state', 'states', drawbounds=True)

        with open(self.date.strftime('edge_list/interMSA%m_%d.csv'), 'w') as e:
            csvwriter = csv.writer(e)
            csvwriter.writerow(['from', 'to', 'edge', 'weight'])

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
                csvwriter.writerow([i, j, 'gc', self.g.edges[i, j]['weight']])
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
                csvwriter.writerow([i, j, 'sgc', self.g.edges[i, j]['weight']])
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
                csvwriter.writerow([i, j, 'tgc', self.g.edges[i, j]['weight']])
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
                csvwriter.writerow([i, j, 'rest', self.g.edges[i, j]['weight']])
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
                csvwriter.writerow([i, j, 'bn', self.g.edges[i, j]['weight']])
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
                csvwriter.writerow([i, j, 'sbn', self.g.edges[i, j]['weight']])
                ax.annotate("",
                            xy=pos1[i], xycoords='data',
                            xytext=pos1[j], textcoords='data',
                            arrowprops=dict(arrowstyle="-", color='r',
                                            shrinkA=5, shrinkB=5,
                                            patchA=None, patchB=None,
                                            connectionstyle="arc3,rad=0.3",
                                            ),
                            )

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        labels = ['GC', 'SGC', 'TGC', 'Bottleneck(GC)', 'Bottleneck(non GC)', 'Rest']
        colors = ['cornflowerblue', 'lightgreen', 'peachpuff', 'r', 'gold', 'silver']
        lines = [Line2D([0], [0], color=c, linewidth=2, alpha=0.85) for c in colors]
        plt.tight_layout()
        plt.legend(lines, labels, fontsize=7, loc=4)
        plt.title('Inter MSA ' + self.date.strftime('%m/%d') + ' map')
        plt.savefig(self.result_dir() + self.date.strftime('%m_%d') + '_map.jpg')

        return

    def plot_w_qc_perco(self):
        colors = ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000']
        num = [0, 25, 50, 75, 100]

        color_c = {}
        for i in self.qc_m.keys():
            j = str(i)
            if self.qc_m[i] > 12:
                color_c[j] = '#b30000'
            elif self.qc_m[i] > 9:
                color_c[j] = '#e34a33'
            elif self.qc_m[i] > 6:
                color_c[j] = '#fc8d59'
            elif self.qc_m[i] > 3:
                color_c[j] = '#fdcc8a'
            else:
                color_c[j] = '#fef0d9'
        tmp = []
        for i in range(0, 18, 5):
            tmp_nodes = select(self.qc_m, i)
            qc_g = self.g.subgraph(tmp_nodes)
            for j in num:
                if i == j == 0:
                    continue
                tmp_g = generate_network_threshold(qc_g, j)
                if j == 0:
                    tmp.append((i, *largest_size_qc(tmp_g, self.device_count)))
                plot_qc_map(tmp_g, 'qc', color_c, self.device_count, pos, i, j, self.date, self.g)
        if not os.path.exists('perco_diff_level/'+ self.date.strftime('%m_%d')+'.csv'):
            a='x'
        else:
            a='w'
        with open('perco_diff_level/'+ self.date.strftime('%m_%d')+'.csv', mode=a) as edges:

            csvwriter = csv.writer(edges)

            csvwriter.writerow(['inner_qc_perco', 'qc', 'gc_size'])
            csvwriter.writerow([0, self.qc, self.gc_node_size])
            for i in tmp:
                csvwriter.writerow(i)

        # color_c = {}
        # for i in self.qca_m.keys():
        #     j = str(i)
        #     if self.qca_m[i] > 12:
        #         color_c[j] = 'red'
        #     elif self.qca_m[i] > 9:
        #         color_c[j] = 'darkorange'
        #     elif self.qca_m[i] > 6:
        #         color_c[j] = 'orange'
        #     elif self.qca_m[i] > 3:
        #         color_c[j] = 'gold'
        #     else:
        #         color_c[j] = 'wheat'
        #
        # for i in range(0, 18, 5):
        #     tmp_nodes = select(self.qca_m, i)
        #     qc_g = self.g.subgraph(tmp_nodes)
        #     for j in num:
        #         if i == j == 0:
        #             continue
        #         tmp_g = generate_network_threshold(qc_g, j)
        #         plot_qc_map(tmp_g, 'qca', color_c, self.device_count, pos, i, j, self.date)
        #
        # color_c = {}
        # for i in self.qcf_m.keys():
        #     j = str(i)
        #     if self.qcf_m[i] > 60:
        #         color_c[j] = 'red'
        #     elif self.qcf_m[i] > 45:
        #         color_c[j] = 'darkorange'
        #     elif self.qcf_m[i] > 30:
        #         color_c[j] = 'orange'
        #     elif self.qcf_m[i] > 15:
        #         color_c[j] = 'gold'
        #     else:
        #         color_c[j] = 'wheat'
        #
        # for i in range(0, 75, 30):
        #     tmp_nodes = select(self.qcf_m, i)
        #     qc_g = self.g.subgraph(tmp_nodes)
        #     for j in num:
        #         if i == j == 0:
        #             continue
        #         tmp_g = generate_network_threshold(qc_g, j)
        #         plot_qc_map(tmp_g, 'qcf', color_c, self.device_count, pos, i, j, self.date)

        return


