# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:20:05 2019

@author: david
"""

from copy import copy
import numpy as np
import matplotlib.pyplot as plt


def plot_nag_ett(nag, show=False, axes=None):
    """Plot the ETT (Extended Truth Table) of a NAG"""

    #if figure is None:
    #    figure = plt.figure()

    # set up the color palette
    # use copy so that we do not mutate the global colormap instance
    # source: https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_masked.html
    palette = copy(plt.cm.gray)
    palette.set_over('r', 1.0)
    palette.set_under('g', 1.0)
    palette.set_bad('b', .2)

    if axes is None:
        axes = plt.gca()

    axes.matshow(nag.ett, cmap=palette)
    x = np.arange(nag.all_number)

    # Set ticks on both sides of axes on
    axes.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)

    axes.set(xlabel='Outputs', ylabel='Inputs', title='Extended Truth Table')
    axes.set_xticks(x)
    axes.set_xticklabels(nag.all_functions)

    # Vertical line to separate the constants from the inputs
    axes.axvline(x=nag.constant_number - .5,
               linewidth=2, color='r')
    # Vertical line to separate the inputs from the nands
    axes.axvline(x=nag.constant_number + nag.input_number - .5,
               linewidth=2, color='r')
    # Vertical line to separate the nands from the outputs
    axes.axvline(x=nag.constant_number + nag.input_number + nag.nand_number - .5,
               linewidth=2, color='r')

    if show:
        figure = plt.figure()
        figure.axes.append(axes)
        plt.show()

    return axes
