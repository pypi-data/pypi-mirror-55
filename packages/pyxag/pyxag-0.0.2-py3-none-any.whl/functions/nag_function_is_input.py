# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:14:19 2019

@author: david
"""

def nag_function_is_input(name):
    """
    Check wether a NAG function name is of type input
    """
    if name[0:1] == 'i':
        return True
    else:
        return False