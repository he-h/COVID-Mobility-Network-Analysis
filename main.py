from plot import *
from whole_network import *
import json
# import datedelta

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
    end = dt.date(2020, 10, 29)

    tmp = start

    msa = ['1602', '1922', '3362', '4472', '5602']
    msa_p = ['interMSA', '1602', '1922', '3362', '4472', '5602']
    dates = []
    datas = dict()
    for i in msa_p:
        datas[i] = {'edge_w': [], 'edge_w_25': [], 'edge_w_75': [],
                    'qc': [],
                    'ave': [],
                    'n_size': [],
                    'flux': [],
                    'n_in': [], 'n_in_25': [], 'n_in_75': [],
                    'd': [], 'd_25': [], 'd_75': []}
    while tmp < end:
        dates.append(tmp)
        nation = Nation(tmp)

        # nation.interMSA.plot_hist()
        # nation.interMSA.plot_g_sg()
        # nation.interMSA.plot_g_sg_device()
        # nation.interMSA.plot_msa_qc()

        datas['interMSA']['edge_w'].append(nation.interMSA.edge_w_median)
        datas['interMSA']['edge_w_25'].append(nation.interMSA.edge_w_25)
        datas['interMSA']['edge_w_75'].append(nation.interMSA.edge_w_75)
        datas['interMSA']['qc'].append(nation.interMSA.qc)
        datas['interMSA']['ave'].append(nation.interMSA.edge_w_ave)
        datas['interMSA']['n_size'].append(nation.interMSA.gc_node_size)
        datas['interMSA']['flux'].append(nation.interMSA.flux)
        datas['interMSA']['n_in'].append(nation.interMSA.indegree_median)
        datas['interMSA']['n_in_25'].append(nation.interMSA.indegree_25)
        datas['interMSA']['n_in_75'].append(nation.interMSA.indegree_75)
        datas['interMSA']['d'].append(nation.interMSA.device_median)
        datas['interMSA']['d_25'].append(nation.interMSA.device_25)
        datas['interMSA']['d_75'].append(nation.interMSA.device_75)

        # for i in msa:
        #     nation.MSAs[i].plot_hist()
        #     nation.MSAs[i].plot_g_sg()
        #     nation.MSAs[i].plot_g_sg_device()
        #     # nation.MSAs[i].plot_map()
        #
        #     datas[i]['edge_w'].append(nation.interMSA.edge_w_median)
        #     datas[i]['edge_w_25'].append(nation.interMSA.edge_w_25)
        #     datas[i]['edge_w_75'].append(nation.interMSA.edge_w_75)
        #     datas[i]['qc'].append(nation.interMSA.qc)
        #     datas[i]['ave'].append(nation.interMSA.edge_w_ave)
        #     datas[i]['n_size'].append(nation.interMSA.gc_node_size)
        #     datas[i]['flux'].append(nation.interMSA.flux)
        #     datas[i]['n_in'].append(nation.interMSA.indegree_median)
        #     datas[i]['n_in_25'].append(nation.interMSA.indegree_25)
        #     datas[i]['n_in_75'].append(nation.interMSA.indegree_75)
        #     datas[i]['d'].append(nation.interMSA.device_median)
        #     datas[i]['d_25'].append(nation.interMSA.device_25)
        #     datas[i]['d_75'].append(nation.interMSA.device_75)


        tmp += dt.timedelta(days=7)

    for i in msa_p:
        plot_edge_w(dates, datas[i]['edge_w'], datas[i]['edge_w_25'], datas[i]['edge_w_75'], i)
        plot_qc(dates, datas[i]['qc'], i)
        plot_ave_node_w(dates, datas[i]['ave'], i)
        plot_node_size(dates, datas[i]['n_size'], i)
        plot_flux(dates, datas[i]['flux'], i)
        plot_node_indegree(dates, datas[i]['n_in'], datas[i]['n_in_25'], datas[i]['n_in_75'], i)
        plot_device(dates, datas[i]['d'], datas[i]['d_25'], datas[i]['d_75'], i)
        break

    # ds = [dt.date(2020,1,15), dt.date(2020,3,23), dt.date(2020,5,15), dt.date(2020,7,15), dt.date(2020,9,15)]
    #
    # for i in ds:
    #     nation = Nation(i)
    #     with open("nations/"+i.strftime('%m_%d')+'.json', "x") as out:
    #         json.dump(nation.interMSA.cc, out)
