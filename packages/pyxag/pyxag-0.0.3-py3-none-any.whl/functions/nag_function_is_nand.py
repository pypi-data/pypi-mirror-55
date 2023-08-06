# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:15:44 2019

@author: david
"""

def nag_function_is_nand(name):
    """
    Check wether a NAG function name is of type nand
    """
    if name[0:1] == 'n':
        return True
    else:
        return False