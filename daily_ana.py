import datetime as dt
import networkx as nx
from model import *


class DailyAna:
    def __init__(self, date, id):
        self.date = date
        self.id = id

        self.g = nx.Graph()

    def __eq__(self, other):
        return self.date == other.date
