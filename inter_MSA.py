from model import *
import powerlaw
from read_file import *
import matplotlib.pyplot as plt


# NY NJ PA 5602
# LA 4472
# Chicago 1602
# Dallas 1922
# Houston 3362


class InterMsaG:
    def __init__(self, date, device, dest):
        self.date = date
        self.device_count = device
        self.g = generate_network(dest)

        self.flux = total_flux(self.g)

        self.thresholds = np.arange(1, 150, 1)
