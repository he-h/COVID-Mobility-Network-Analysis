import datetime as dt
import networkx as nx
import json
from statistics import median
from model import *
from read_file import *


choose = 4

file = 'region_div/region'+str(choose)+'.json'
with open(file) as json_file:
    regions = json.load(json_file)

map_data = 'region_div/region_s_'+str(choose)+'.json'
with open(file) as json_file:
    map_r = json.load(json_file)


class DailyAna:
    def __init__(self, date, id):
        self.date = date
        self.id = id

        self.node_scope = regions[id]
        self.map_scope = map_r[id]

        self.dest = read_files_c(self.date, self.node_scope)
        self.g = generate_network(self.dest)


    def __eq__(self, other):
        return self.date == other.date
