
from functions.plot_nag_ett import plot_nag_ett
from functions.plot_nag_graph import plot_nag_graph
import matplotlib.pyplot as plt

def plot_nag(nag, show=True):
    """Plot a NAG"""

    # How to display images in plots:
    # https://stackoverflow.com/questions/35692507/plot-several-image-files-in-matplotlib-subplots/35692695
    # https://matplotlib.org/gallery/lines_bars_and_markers/categorical_variables.html#sphx-glr-gallery-lines-bars-and-markers-categorical-variables-py

    nag_figure = plt.figure(figsize=(15,15))

    plt.subplots_adjust(left=.1, bottom=.1, right=.9, top=.9, wspace=.2, hspace=.2)

    # Layout
    # https://matplotlib.org/3.1.1/tutorials/intermediate/tight_layout_guide.html
    #fig.autolayout = True
    #fig.set_tight_layout(True)

    nag_figure.suptitle('NAG: {0}'.format(nag.name))

    stat_axes = nag_figure.add_subplot(311, autoscale_on=True, title='Statistics')
    stat_axes.set_axis_off()
    stat_axes.text(0.2, 0.8, nag.get_statistics(), horizontalalignment='left', verticalalignment='top', transform=stat_axes.transAxes)

    graph_axes = nag_figure.add_subplot(312, autoscale_on=True, title='NAND-based Algorithmic Graph')
    plot_nag_graph(nag, show=False, axes=graph_axes)

    ett_axes = nag_figure.add_subplot(313, autoscale_on=True, title='Extended Truth Table')
    plot_nag_ett(nag, show=False, axes=ett_axes)

    if show:
        plt.show()

    return nag_figure
