# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:15:35 2019

@author: david
"""

def nag_function_is_constant(name):
    """
    Check wether a NAG function name is of type constant
    """
    if name[0:1] == 'c':
        return True
    else:
        return False