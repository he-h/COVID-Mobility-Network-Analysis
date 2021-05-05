from inner_MSA import *
from inter_MSA import *
import os
import csv
import multiprocessing as mp


def dest_store(start, end):
    dest = dict()
    m_dest = {}
    date = start-dt.timedelta(days=3)
    while date <= end+dt.timedelta(days=3):
        print(date)
        with open("msa_device_count/" + date.strftime('%m_%d') + ".json", "r") as outfile:
            device_count = json.load(outfile)
        dest[date], m_dest[date] = file_whole(file_str(date), device_count)
        date += dt.timedelta(days=1)

    return dest, m_dest


def file_whole(path, device_count):
    dest = dict()
    m_dest = default_MSAs_dict()

    df = pd.read_csv(path)

    for ind in df.index:
        block = block_str(str(df['origin_census_block_group'][ind]))

        block_m = MSA_id(block)
        if block_m == -1:
            continue

        dests = eval(df['destination_cbgs'][ind])
        for i in dests.keys():
            if dests[i] <= 2:
                continue

            str_i = block_str(str(i))

            if str_i == block:
                continue

            i_m = MSA_id(str_i)
            if i_m == -1:
                continue

            if i_m != block_m:
                tmp = tuple(sorted([block_m, i_m]))
                if tmp in dest.keys():
                    dest[tmp] += dests[i]/device_count[block_m]/7*10000
                else:
                    dest[tmp] = dests[i]/device_count[block_m]/7*10000
            else:
                tmp = tuple(sorted([block, str_i]))
                if tmp in m_dest[block_m].keys():
                    m_dest[block_m][tmp] += dests[i]/df['device_count'][ind]/7*100
                else:
                    m_dest[block_m][tmp] = dests[i]/df['device_count'][ind]/7*100

    return dest, m_dest


def read_files_whole(date):
    with open("msa_device_count/" + date.strftime('%m_%d') + ".json", "r") as outfile:
        device_count = json.load(outfile)
    dest = dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(7):
        tmp_dests, tmp_m_dest = file_whole(file_str(tmp), device_count)
        merge(dest, tmp_dests)
        inner_merge(MSA_dest, tmp_m_dest)
        tmp += dt.timedelta(days=1)

    return device_count, dest, MSA_dest


def read_files_sum(date, _dest, _m_dest):
    with open("msa_device_count/" + date.strftime('%m_%d') + ".json", "r") as outfile:
        device_count = json.load(outfile)

    dest = dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(7):
        tmp_dests, tmp_m_dest = _dest[tmp], _m_dest[tmp]
        merge(dest, tmp_dests)
        inner_merge(MSA_dest, tmp_m_dest)
        tmp += dt.timedelta(days=1)

    return device_count, dest, MSA_dest


def median_25_75(tmp):
    return np.percentile(tmp, 25), median(tmp), np.percentile(tmp, 75)


class Nation:
    def __init__(self, date, _dest, _m_dest):
        print(date)
        self.date = date
        self.device_count, self.dest, self.MSA_dest = read_files_sum(date, _dest, _m_dest)

        self.MSAs = default_MSAs_dict()

        qcs = []

        for i in self.MSAs.keys():
            self.MSAs[i] = MSA(i, date, self.MSA_dest[i])
            qcs.append([i, self.MSAs[i].qc, self.MSAs[i].qcb, self.MSAs[i].qca, self.MSAs[i].qcf, self.MSAs[i].gc_node_size, self.MSAs[i].flux/self.device_count[i], self.MSAs[i].edge_w_median])


        # if not os.path.exists('qc/'+self.date.strftime('%m_%d')+'.csv'):
        #     a='x'
        # else:
        #     a='w'
        # with open('qc/'+self.date.strftime('%m_%d')+'.csv', mode=a) as edges:
        #
        #     csvwriter = csv.writer(edges)
        #
        #     csvwriter.writerow(['msa', 'qc', 'qcb', 'qca', 'qcf', 'gc_size', 'flux', 'edge_w'])
        #     for i in qcs:
        #         csvwriter.writerow(i)

        self.interMsa = InterMsaG(self.date, self.dest, self.device_count)

        # with open(date.strftime('edge_list/%m_%d_raw.csv'), 'w') as m:
        #         csvwriter = csv.writer(m)
        #         csvwriter.writerow(['from', 'to', 'weight'])
        #         for i, j in self.interMsa.g.edges:
        #             csvwriter.writerow([i, j, self.interMsa.g.edges[i, j]['weight']])

        # msa = ['17820','35620','31080','26420','23540','24500']
        # the = [self.MSAs[i].thresholds for i in msa]
        # the.sort(key=len)
        # the = the[-1]
        # a=self.MSAs['17820'].edge_size
        # thea1 = the[:len(a)]
        # a1 = [a[-1],0]
        # thea2 = [the[len(a)-1] ,the[len(a)-1]+1]
        # b=self.MSAs['35620'].edge_size
        # theb1 = the[:len(b)]
        # b1 = [b[-1],0]
        # theb2 = [the[len(b)-1] ,the[len(b)-1]+1]
        # c=self.MSAs['31080'].edge_size
        # thec1 = the[:len(c)]
        # c1 = [c[-1],0]
        # thec2 = [the[len(c)-1] ,the[len(c)-1]+1]
        # d=self.MSAs['26420'].edge_size
        # thed1 = the[:len(d)]
        # d1 = [d[-1],0]
        # thed2 = [the[len(d)-1] ,the[len(d)-1]+1]
        # e=self.MSAs['23540'].edge_size
        # thee1 = the[:len(e)]
        # e1 = [e[-1],0]
        # thee2 = [the[len(e)-1] ,the[len(e)-1]+1]
        # f=self.MSAs['24500'].edge_size
        # thef1 = the[:len(f)]
        # f1 = [f[-1],0]
        # thef2 = [the[len(f)-1] ,the[len(f)-1]+1]
        #
        # plt.figure()
        # plt.plot(thea1, a, color='blue', label=name['17820'])
        # plt.plot(thea2, a1, '--', color='blue')
        # plt.plot(theb1, b, color='orange', label='New York City, NY')
        # plt.plot(theb2, b1, '--', color='orange')
        # plt.plot(thec1, c, color='green', label='Los Angeles, CA')
        # plt.plot(thec2, c1, '--', color='green')
        # plt.plot(thed1, d, color='red', label='Houston, TX')
        # plt.plot(thed2, d1, '--', color='red')
        # plt.plot(thee1, e, color='purple', label=name['23540'])
        # plt.plot(thee2, e1, '--', color='purple')
        # plt.plot(thef1, f, color='brown', label=name['24500'])
        # plt.plot(thef2, f1, '--', color='brown')
        # plt.xlabel('Thresholds')
        # plt.ylabel('Number of Remaining Edges')
        # plt.yscale("log")
        # plt.xscale("log")
        # if self.date < dt.date(2020,3,1):
        #     plt.legend()
        # plt.savefig('edge_remain/'+self.date.strftime('%m_%d')+'.jpg')

