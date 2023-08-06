

def convert_bit_array_to_int(bit_array):
    result = 0
    for bit in bit_array:
        result = (result << 1) | bit
    return result
