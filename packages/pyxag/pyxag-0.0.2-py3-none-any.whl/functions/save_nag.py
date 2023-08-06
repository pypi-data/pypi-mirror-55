from . import *


def save_nag(nag, path):
    """Save a NAG in a file"""
    with open(path, 'w') as nag_file:
        nag_json = convert_nag_to_json(nag)
        nag_file.write(nag_json)
