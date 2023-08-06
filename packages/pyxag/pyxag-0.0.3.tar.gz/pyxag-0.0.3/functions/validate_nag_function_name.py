# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 22:09:07 2019

@author: david
"""

def validate_nag_function_name(name):
    """
    Check wether a NAG function name is valid
    """
    if (
            name is not None and
            isinstance(name, str) and 
            len(name) > 1 and
            name[1:].isdigit() and
            (
                    name[0:1] in ['i','n','o'] or
                    name in ['c0','c1']
            ) and
            name[0:2] not in ['i0','n0','o0'] 
            ):
            return True
    else:
        return False