# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:15:58 2019

@author: david
"""

def nag_function_is_output(name):
    """
    Check wether a NAG function name is of type output
    """
    if name[0:1] == 'o':
        return True
    else:
        return False