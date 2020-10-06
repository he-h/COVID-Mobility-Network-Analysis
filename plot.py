import matplotlib.pyplot as plt

'''
This function is aim to plot number of element of G and SG with changing threshold described in the paper
'''


def plot_g_sg(x, g, sg):

    # fig, ax1 = plt.subplots()
    # ax1.set_xlabel('threshold')
    # ax1.set_ylabel('size')
    # ax1.plot(x, g)
    # ax1.tick_params(axis='y')
    # ax2 = ax1.twinx()
    # ax2.plot(x, sg, color='orange')
    # ax2.tick_params(axis='y')
    # fig.tight_layout()
    #
    # plt.show()

    figure, axis_1 = plt.subplots()

    axis_1.plot(x, g, color='blue', label='largest SCC')
    axis_1.set_xlabel('threshold')
    axis_1.set_ylabel('size')

    axis_2 = axis_1.twinx()
    axis_2.plot(x, sg, color='orange', label='second largest SCC')
    lines_1, labels_1 = axis_1.get_legend_handles_labels()
    lines_2, labels_2 = axis_2.get_legend_handles_labels()

    lines = lines_1 + lines_2
    labels = labels_1 + labels_2

    axis_1.legend(lines, labels, loc=0)

    plt.show()

    return


'''
This function plot the histograph of weights of edges with a logrithmic scale
'''


def plot_hist(dest_cbgs):
    value = list(dest_cbgs.values())

    plt.hist(value, label='number of weights', log=True, bins=100)
    plt.xscale('log')
    plt.legend()
    plt.show()

    return

