from inner_MSA import *
from inter_MSA import *


def file_whole(path):
    dest = dict()
    device_count = dict()
    m_dev = default_MSAs_dict()
    m_dest = default_MSAs_dict()

    df = pd.read_csv(path)

    for ind in df.index:
        if ind == 100:
            break
        block = str(df['origin_census_block_group'][ind])

        block_m = MSA_id(block)
        if block_m == -1:
            continue

        m_dev[block_m][block] = df['device_count'][ind]

        if block_m in device_count.keys():
            device_count[block_m] += df['device_count'][ind]
        else:
            device_count[block_m] = df['device_count'][ind]

        dests = parse_str(df['destination_cbgs'][ind])
        for i in dests.keys():
            if i == block:
                continue

            i_m = MSA_id(i)
            if i_m == -1:
                continue

            if i_m != block_m:
                if (block_m, i_m) in dest.keys():
                    dest[(block_m, i_m)] += dests[i]
                else:
                    dest[(block_m, i_m)] = dests[i]
            else:
                m_dest[block_m][(block, i)] = dests[i]

    return device_count, dest, m_dev, m_dest


def read_files_whole(date):
    device_count = dict()
    dest = dict()
    MSA_device = default_MSAs_dict()
    MSA_dest = default_MSAs_dict()

    tmp = date - dt.timedelta(days=3)

    for i in range(1):
        print(i)
        tmp_device, tmp_dests, tmp_m_dev, tmp_m_dest = file_whole(file_str(tmp))
        print(i)
        merge(dest, tmp_dests)
        merge(device_count, tmp_device)
        inner_merge(MSA_device, tmp_m_dev)
        inner_merge(MSA_dest, tmp_m_dest)
        tmp += dt.timedelta(days=1)

    for i in device_count.keys():
        device_count[i] /= 7
        for j in MSA_dest[i].keys():
            MSA_dest[i][j] /= 7
        for k in MSA_device[i]:
            MSA_device[i][k] /= 7

    for i in dest.keys():
        dest[i] /= 7

    return device_count, dest, MSA_device, MSA_dest


class Nation:
    def __int__(self, date):
        self.date = date
        device_count, dest, MSA_device, MSA_dest = read_files_whole(date)

        self.MSAs = default_MSAs_dict()
        for i in self.MSAs.keys():
            self.MSAs[i] = MSA(i, date, MSA_device[i], MSA_dest[i])

        Msa_qc = default_MSAs_dict()
        for i in Msa_qc.keys():
            Msa_qc[i] = self.MSAs[i].qc

        self.interMSA = InterMsaG(date, device_count, dest, Msa_qc)
