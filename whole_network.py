from inner_MSA import *
from inter_MSA import *
import os
import csv


def file_whole(path, device_count):
    dest = dict()
    m_dest = default_MSAs_dict()

    df = pd.read_csv(path)

    for ind in df.index:
        block = block_str(str(df['origin_census_block_group'][ind]))

        block_m = MSA_id(block)
        if block_m == -1:
            continue
        #
        # if block_m in device_count.keys():
        #     device_count[block_m] += df['device_count'][ind]
        # else:
        #     device_count[block_m] = df['device_count'][ind]

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
                    dest[tmp] += dests[i]/device_count[block_m]*10000
                else:
                    dest[tmp] = dests[i]/device_count[block_m]*10000
            else:
                tmp = tuple(sorted([block, str_i]))
                if tmp in m_dest[block_m].keys():
                    m_dest[block_m][tmp] += dests[i]/df['device_count'][ind]*100
                else:
                    m_dest[block_m][tmp] = dests[i]/df['device_count'][ind]*100

    return dest, m_dest


def read_files_whole(date):
    with open("msa_device_count/"+ date.strftime('%m_%d') + ".json", "r") as outfile:
        device_count = json.load(outfile)
    dest = dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(7):
        # print(i)
        tmp_dests, tmp_m_dest = file_whole(file_str(tmp), device_count)
        merge(dest, tmp_dests)
        inner_merge(MSA_dest, tmp_m_dest)
        tmp += dt.timedelta(days=1)

    for i in device_count.keys():
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

        # for i in msa:
        #     print(i, len(self.MSAs[i].g.nodes()), self.device_count[i]/len(self.MSAs[i].g.nodes()))

        if not os.path.exists('qc/'+self.date.strftime('%m_%d')+'.csv'):
            a='x'
        else:
            a='w'
        with open('qc/'+self.date.strftime('%m_%d')+'.csv', mode=a) as edges:

            csvwriter = csv.writer(edges)

            csvwriter.writerow(['msa', 'qc', 'qcb', 'qca', 'qcf'])
            for i in qcs:
                csvwriter.writerow(i)

        msa = ['35620', '31080', '16980', '19100', '26420']
        the = [self.MSAs[i].thresholds for i in msa]
        the.sort(key=len)
        the = the[-1]
        a=self.MSAs['35620'].edge_size
        thea1 = the[:len(a)]
        a1 = [0] * (len(the)-len(a))
        thea2 = the[len(a):]
        b=self.MSAs['31080'].edge_size
        theb1 = the[:len(b)]
        b1 = [0] * (len(the)-len(b))
        theb2 = the[len(b):]
        c=self.MSAs['16980'].edge_size
        thec1 = the[:len(c)]
        c1 = [0] * (len(the)-len(c))
        thec2 = the[len(c):]
        d=self.MSAs['19100'].edge_size
        thed1 = the[:len(d)]
        d1 = [0] * (len(the)-len(d))
        thed2 = the[len(d):]
        e=self.MSAs['26420'].edge_size
        thee1 = the[:len(e)]
        e1 = [0] * (len(the)-len(e))
        thee2 = the[len(e):]

        plt.figure()
        plt.plot(thea1, a, color='blue', label='NYC')
        plt.plot(thea2, a1, '--', color='blue')
        plt.plot(theb1, b, color='orange', label='LA')
        plt.plot(theb2, b1, '--', color='orange')
        plt.plot(thec1, c, color='green', label='Chicago')
        plt.plot(thec2, c1, '--', color='green')
        plt.plot(thed1, d, color='red', label='Dallas')
        plt.plot(thed2, d1, '--', color='red')
        plt.plot(thee1, e, color='purple', label='Houston')
        plt.plot(thee2, e1, '--', color='purple')
        plt.xlabel('Thresholds')
        plt.ylabel('Number of Remaining Edges')
        plt.yscale("log")
        plt.xscale("log")
        plt.legend()
        plt.title(self.date.strftime('%m/%d')+' edge comparison')
        plt.savefig('edge_remain/'+self.date.strftime('%m_%d')+'.png')
