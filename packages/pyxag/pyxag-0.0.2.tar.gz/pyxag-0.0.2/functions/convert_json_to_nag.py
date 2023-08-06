import jsonpickle


def convert_json_to_nag(json):
    nag = jsonpickle.decode(json)
    return nag
