from classes.nag import Nag
from functions.export_nag_to_pdf import export_nag_to_pdf

# Constant functions

def get_nag_sample_constant_0():
    nag = Nag('Constant 0')
    nag.description = 'A constant function that returns 0'
    nag.file_base_name = 'sample_nag_constant_0'
    nag.set_output('c0', 'o1')
    nag.set_execution_mode()
    nag.execute(None)
    nag.execute(None)
    return nag

def get_nag_sample_constant_1():
    nag = Nag('Constant 1')
    nag.description = 'A constant function that returns 1'
    nag.file_base_name = 'sample_nag_constant_1'
    nag.set_output('c1', 'o1')
    nag.set_execution_mode()
    nag.execute(None)
    nag.execute(None)
    return nag

# Unary Functions

def get_nag_sample_unary_pipe():
    nag = Nag('Unary Pipe')
    nag.description = 'A unary pipe function, i.e. a useless function that outputs exactly what it receives'
    nag.file_base_name = 'sample_nag_unary_pipe'
    nag.set_output('i1', 'o1')
    nag.set_execution_mode()
    nag.execute([0])
    nag.execute([1])
    return nag

def get_nag_sample_unary_not():
    nag = Nag('Unary NOT')
    nag.description = 'A unary NOT function'
    nag.file_base_name = 'sample_nag_unary_not'
    nag.set_nand('i1', 'i1', 'n1')
    nag.set_output('n1', 'o1')
    nag.set_execution_mode()
    nag.execute([0])
    nag.execute([1])
    return nag

def get_nag_sample_unary_double_not():
    nag = Nag('Unary Double NOT')
    nag.description = 'A unary double NOT function, equivalent to the nothing function'
    nag.file_base_name = 'sample_nag_unary_double_not'
    nag.set_nand('i1', 'i1', 'n1')
    nag.set_nand('n1', 'n1', 'n2')
    nag.set_output('n2', 'o1')
    nag.set_execution_mode()
    nag.execute([0])
    nag.execute([1])
    return nag

# Binary functions

def get_nag_sample_binary_nand():
    nag = Nag('Binary NAND')
    nag.description = 'A binary NAND function, i.e. the building block function of NAGs'
    nag.file_base_name = 'sample_nag_binary_nand'
    nag.set_nand('i1', 'i2', 'n1')
    nag.set_output('n1', 'o1')
    nag.set_execution_mode()
    nag.execute([0, 0])
    nag.execute([0, 1])
    nag.execute([1, 0])
    nag.execute([1, 1])
    return nag

def get_nag_sample_binary_xor():
    nag = Nag('Binary XOR')
    nag.description = 'A binary XOR function'
    nag.file_base_name = 'sample_nag_binary_xor'
    nag.set_nand('i1', 'i2', 'n1')
    nag.set_nand('i1', 'n1', 'n2')
    nag.set_nand('i2', 'n1', 'n3')
    nag.set_nand('n2', 'n3', 'n4')
    nag.set_output('n4', 'o1')
    nag.set_execution_mode()
    nag.execute([0, 0])
    nag.execute([0, 1])
    nag.execute([1, 0])
    nag.execute([1, 1])
    return nag


def _export_nag_samples_to_pdf():
    # Constant functions
    export_nag_to_pdf(get_nag_sample_constant_0())
    export_nag_to_pdf(get_nag_sample_constant_1())
    # Unary functions
    export_nag_to_pdf(get_nag_sample_unary_not())
    export_nag_to_pdf(get_nag_sample_unary_pipe())
    export_nag_to_pdf(get_nag_sample_unary_double_not())
    # Binary functions
    export_nag_to_pdf(get_nag_sample_binary_nand())
    export_nag_to_pdf(get_nag_sample_binary_xor())


