from functions.convert_nag_networkx_to_graphviz import convert_nag_networkx_to_graphviz
import matplotlib.image as mpimg
import cairosvg
import tempfile
import logging


def plot_nag_graph(nag, show=False, axes=None):

    graph_image = convert_nag_networkx_to_graphviz(nag)

    if show:
        graph_image.view()

    if axes is not None:

        # ISSUE: Matplotlib does not support natively SVG format.
        # In consequence, we must produce a PNG of good enough quality.

        # Python Graphviz render() documentation: https://graphviz.readthedocs.io/en/stable/api.html#graphviz.render
        # OPTIMIZATION: I use graphviz.pipe() instead of render() to avoid the creation of an intermediary file.
        # ISSUE: The pythonic graphviz lib does not have any dpi or scaling parameter. Thus, I choose the SVG vectorial format and convert to PNG in a later step.
        as_bytes = graph_image.pipe(format='svg')

        # OPTIMIZATION: To convert the SVG vectorial format to PNG with good enough resolution.
        dpi = 600  # In actual fact, 300 is good enough.
        # Reference: https://cairosvg.org/documentation/
        png_file_path = tempfile.mktemp('png')
        logging.debug('png_file_path: %s', png_file_path)
        cairosvg.svg2png(bytestring=as_bytes, write_to=png_file_path, dpi=dpi)

        # Embed the image in the matplotlib axes object.
        # Reference: imshow(): https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.imshow.html
        interpolation = 'spline36'  # I did not test all interpolations but yield good enough results with this one.
        png_image = mpimg.imread(png_file_path)
        axes.imshow(png_image, aspect='equal', interpolation=interpolation)
        # Remove the grid and ticks decoration, we are only interested in the image here.
        axes.grid(False)
        axes.set_xticks([])
        axes.set_yticks([])



