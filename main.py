from plot import *
from whole_network import *
import datedelta

# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362


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
    start = dt.date(2020, 1, 8)
    end = dt.date(2020, 9, 24)

    tmp = dt.date(2020, 1, 15)

    msa = ['1602', '1922', '3362', '4472', '5602']
    while tmp < dt.date(2020, 9, 16):
        nation = Nation(tmp)

        nation.interMSA.plot_hist()
        nation.interMSA.plot_g_sg()
        nation.interMSA.plot_g_sg_device()
        nation.interMSA.plot_msa_qc()

        for i in msa:
            nation.MSAs[i].plot_hist()
            nation.MSAs[i].plot_g_sg()
            nation.MSAs[i].plot_g_sg_device()

        tmp += datedelta.MONTH
