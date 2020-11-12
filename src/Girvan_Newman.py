from nation import *
import community


if __name__ == '__main__':
    data = generate_files()
    dest = read_files(data)
    g = generate_network(dest)

    partition = community.best_partition(g, resolution=200) #resolution=50

    region_div = dict()
    for i in set(partition.values()):
        region_div[i] = set()

    for i in partition.keys():
        value = partition[i]
        region_div[value].add(i)

    area_id = dict()
    for i in region_div.keys():
        area_id[i] = tuple(statescope(region_div[i]))
        region_div[i] = list(region_div[i])

    with open("region_div/louvain_partition_b.json", "w") as outfile:
        json.dump(region_div, outfile)

    with open("region_div/louvain_partition_b_s.json", "w") as outfile:
        json.dump(area_id, outfile)
