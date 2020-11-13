from plot import *
from daily_ana import *


region_file = ''


'''
This function is to generate file names with multiple dates
'''


def generate_file_name(num):
    names = []
    for i in range(1, num+1):
        tmp = 'data/01/0'+str(i)+'/2020-01-0'+str(i)+'-social-distancing.csv.gz'
        names.append(tmp)

    return names


def main(file, state_id):
    dest_cbgs = read_files(file, state_id)
    G = generate_network(dest_cbgs)
    thresholds, num_g, num_sg = calc_g_sg(G)
    plot_g_sg(thresholds, num_g, num_sg)
    # bn, bn_weight = calc_bottleneck(G, thresholds, num_sg)
    # plot_map_bn(G, bn, bn_weight, state_id)

    return


if __name__ == '__main__':
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    dates = []
    device = []
    qc = []
    node_size = []
    flux = []
    indegree = []

    date = dt.date(2020, 3, 13)
    for i in range(1):
        dates.append(str(date))
        da = DailyAna(date, 1)

        device.append(da.device_count)
        qc.append(da.qc)
        node_size.append(da.gc_node_size)
        flux.append(da.flux)
        indegree.append(da.indegree_median)

        date += dt.timedelta(days=1)

    plot_device(dates, device)
    plot_qc(dates, qc)
    plot_node_size(dates, node_size)
    plot_node_indegree(date, indegree)
    plot_flux(dates, flux)

    # state_id = 48
    # path = generate_file_name(7)
    # main(path, state_id)

    # block_ids, dest_cbgs = read_files(path, 36)
    # g = generate_network(block_ids, dest_cbgs)
    # plot_hist(g)
