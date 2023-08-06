

def convert_int_to_bit_array(integer_value):
    """
    Sources:
    - https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
    :param integer_value:
    :return:
    """
    return [int(digit) for digit in bin(integer_value)[2:]]