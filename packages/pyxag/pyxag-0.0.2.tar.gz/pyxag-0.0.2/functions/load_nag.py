from . import *


def load_nag(nag, path):
    """Load a NAG from a file"""
    with open(path, 'r') as nag_file:
        nag_json = nag_file.read()
        nag = convert_json_to_nag(nag_json)
        return nag
