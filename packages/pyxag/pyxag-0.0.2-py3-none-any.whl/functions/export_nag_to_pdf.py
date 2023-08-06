from functions.plot_nag import plot_nag
import matplotlib.pyplot as plt


def export_nag_to_pdf(nag, file_name=None):
    if file_name is None:
        file_name = '{0}.pdf'.format(nag.file_base_name)
    nag_figure = plot_nag(nag, show=False)
    nag_figure.savefig(file_name,
                 dpi=600,
                 orientation='portrait',
                 quality=95,
                 optimize=True,
                 papertype='a4',
                 format='pdf')
