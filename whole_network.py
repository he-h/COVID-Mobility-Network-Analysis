from inner_MSA import *
from inter_MSA import *
import os
import csv


def file_whole(path):
    dest = dict()
    device_count = dict()
    m_dest = default_MSAs_dict()

    df = pd.read_csv(path)

    for ind in df.index:
        block = block_str(str(df['origin_census_block_group'][ind]))

        block_m = MSA_id(block)
        if block_m == -1:
            continue

        if block_m in device_count.keys():
            device_count[block_m] += df['device_count'][ind]
        else:
            device_count[block_m] = df['device_count'][ind]

        dests = parse_str(df['destination_cbgs'][ind])
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
                    dest[tmp] += dests[i]
                else:
                    dest[tmp] = dests[i]
            else:
                tmp = tuple(sorted([block, str_i]))
                if tmp in m_dest[block_m].keys():
                    m_dest[block_m][tmp] += dests[i]
                else:
                    m_dest[block_m][tmp] = dests[i]

    return device_count, dest, m_dest


def read_files_whole(date):
    device_count = dict()
    dest = dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(7):
        # print(i)
        tmp_device, tmp_dests, tmp_m_dest = file_whole(file_str(tmp))
        merge(dest, tmp_dests)
        merge(device_count, tmp_device)
        inner_merge(MSA_dest, tmp_m_dest)
        tmp += dt.timedelta(days=1)

    for i in device_count.keys():
        device_count[i] /= 7
        for j in MSA_dest[i].keys():
            MSA_dest[i][j] /= 7

    for i in dest.keys():
        dest[i] /= 7

    return device_count, dest, MSA_dest


class Nation:
    def __init__(self, date):
        print(date)
        self.date = date
        self.device_count, self.dest, self.MSA_dest = read_files_whole(date)

        self.MSAs = default_MSAs_dict()

        qcs = []

        for i in self.MSAs.keys():
            self.MSAs[i] = MSA(i, date, self.MSA_dest[i])
            qcs.append([i, self.MSAs[i].qc, self.MSAs[i].qcb, self.MSAs[i].qcc, self.MSAs[i].thresholds[-1]])

        msa = ['35620', '31080', '16980', '19100', '26420', '47900', '33100', '37980', '12060', '38060']

        for i in msa:
            print(i, len(self.MSAs[i].g.nodes()), self.device_count[i]/len(self.MSAs[i].g.nodes()))

        if not os.path.exists('qc/'+self.date.strftime('%m_%d')+'.csv'):
            with open('qc/'+self.date.strftime('%m_%d')+'.csv', mode='x') as edges:

                csvwriter = csv.writer(edges)

                csvwriter.writerow(['msa', 'qc', 'qcb', 'qca', 'qcf'])
                for i in qcs:
                    csvwriter.writerow(i)

        msa = ['35620', '31080', '16980', '19100', '26420']
        the = [self.MSAs[i].thresholds for i in msa]
        the.sort(key=len)
        the = the[-1]
        a=self.MSAs['35620'].edge_size
        a=comli(a,len(the))
        b=self.MSAs['31080'].edge_size
        b=comli(b,len(the))
        c=self.MSAs['16980'].edge_size
        c=comli(c,len(the))
        d=self.MSAs['19100'].edge_size
        d=comli(d,len(the))
        e=self.MSAs['26420'].edge_size
        e=comli(e,len(the))

        plt.figure()
        plt.plot(the, a, label='NY')
        plt.plot(the, b, label='LA')
        plt.plot(the, c, label='Chicago')
        plt.plot(the, d, label='Dallas')
        plt.plot(the, e, label='Houston')
        plt.yscale("log")
        plt.xscale("log")
        plt.legend()
        plt.title(self.date.strftime('%m/%d')+' edge comparison')
        plt.savefig('edge_remain/'+self.date.strftime('%m_%d')+'.png')
