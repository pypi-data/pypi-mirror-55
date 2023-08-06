from functions.get_nag_function_type import get_nag_function_type
from functions.get_nag_function_number import get_nag_function_number


def substitute_nag_function(nag, old_function, new_function, remove_old_function=True):
    """Replaces all occurences of old_function with new_function."""

    # Check the compatibility of the two functions
    if get_nag_function_type(old_function) != get_nag_function_type(new_function):
        raise ValueError('Incompatible functions', old_function, new_function)

    if get_nag_function_number(old_function) < get_nag_function_number(new_function):
        # Check that the substitution would not yield an illegal graph cycle (and fail).
        if nag.get_successors_min_number(old_function) is not None and \
                nag.get_successors_min_number(old_function) < get_nag_function_number(new_function):
            raise ValueError('Old function min successors number < new function number', old_function, new_function)

    if get_nag_function_number(old_function) > get_nag_function_number(new_function):
        # Check that the substitution would not yield an illegal graph cycle (and fail).
        if nag.get_predecessors_max_number(old_function) is not None and \
                nag.get_predecessors_max_number(old_function) > get_nag_function_number(new_function):
            raise ValueError('Old function max predecessors number > new function number', old_function, new_function)

    # It is now safe to substitute the old vertex with the new one.

    # First, set the new function with the same predecessors than the old one.
    # This is only applicable to vertex types that have predecessors, i.e. NANDs and outputs.
    if get_nag_function_type(new_function) == 'n':
        predecessors = nag.get_predecessors_as_list(old_function)
        predecessor_1 = predecessors[0]
        predecessor_2 = None
        if len(predecessors) == 1:
            # In a MultiDiGraph, a NAND vertex may have a single predecessor.
            # This happens when its two inputs are identical.
            predecessor_2 = predecessor_1
        elif len(predecessors) == 2:
            # Otherwise, when the NAND vertex has two distinct inputs,
            # it has two predecessors.
            predecessor_2 = predecessors[1]
        nag.set_nand(predecessor_1, predecessor_2, new_function)
    if get_nag_function_type(new_function) == 'o':
        predecessors = nag.get_predecessors_as_list(old_function)
        predecessor_1 = predecessors[0]
        nag.set_output(predecessor_1, new_function)

    # Second, find all successors and overwrite them with the new function as predecessor.
    for successor in nag.get_successors_as_list(old_function):
        if get_nag_function_type(successor) == 'n':
            predecessors = nag.get_predecessors_as_list(successor)
            predecessor_1 = predecessors[0]
            predecessor_2 = None
            if len(predecessors) == 1:
                # In a MultiDiGraph, a NAND vertex may have a single predecessor.
                # This happens when its two inputs are identical.
                predecessor_2 = predecessor_1
            elif len(predecessors) == 2:
                # Otherwise, when the NAND vertex has two distinct inputs,
                # it has two predecessors.
                predecessor_2 = predecessors[1]
            if predecessor_1 == old_function:
                predecessor_1 = new_function
            if predecessor_2 == old_function:
                predecessor_2 = new_function
            nag.set_nand(predecessor_1, predecessor_2, successor)
        if get_nag_function_type(successor) == 'o':
            nag.set_output(new_function, successor)

    # Finally, delete the old vertex.
    # This automatically removes all remaining adjacent edges.
    # Source: https://networkx.github.io/documentation/latest/reference/classes/generated/networkx.Graph.remove_node.html
    if remove_old_function:
        nag.graph.remove_node(old_function)


