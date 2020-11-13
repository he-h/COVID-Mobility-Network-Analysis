from statistics import median
from nation import *
import seaborn as sns


choose = 4

file = 'region_div/region'+str(choose)+'.json'
with open(file) as json_file:
    regions = json.load(json_file)

map_data = 'region_div/region_s_'+str(choose)+'.json'
with open(file) as json_file:
    map_r = json.load(json_file)


class DailyAna:
    def __init__(self, date, id):
        print(date)
        self.date = date
        self.id = id

        # implement later as a result of MSA
        self.node_scope = regions[str(id)]
        self.map_scope = map_r[str(id)]

        self.device_count, self.dest = read_files_c(self.date, self.node_scope)
        self.g = generate_network(self.dest)

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

    def bottlenecks(self):
        g_perco_b = generate_network_threshold(self.g, self.qc - .25)
        s_cc = sorted(list(nx.connected_components(self.g_perco)), key=len, reverse=True)[1]
        l_cc = sorted(list(nx.connected_components(g_perco_b)), key=len, reverse=True)[0]
        l_cc = l_cc.difference(s_cc)

        bc = set()

        for i, j in g_perco_b.edges():
            if self.qc - .25 <= g_perco_b.edges[i, j]['weight'] < self.qc:
                if (i in s_cc and j in l_cc) or (i in l_cc and j in s_cc):
                    bc.add((i, j))

        return bc

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

