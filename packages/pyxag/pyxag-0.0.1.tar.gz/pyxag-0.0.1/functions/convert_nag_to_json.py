import jsonpickle


def convert_nag_to_json(nag):
    """Serializes the NAG nag into JSON"""
    return jsonpickle.encode(nag)


