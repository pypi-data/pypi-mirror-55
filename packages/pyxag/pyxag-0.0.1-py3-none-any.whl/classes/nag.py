# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 22:09:07 2019

@author: david
"""

import logging
from builtins import ValueError
import networkx as nx
import numpy as np
import numpy.ma as ma
from functions.convert_bit_array_to_int import convert_bit_array_to_int
from functions.convert_int_to_bit_array import convert_int_to_bit_array
from functions.convert_nag_to_json import convert_nag_to_json
from functions.get_nag_function_number import get_nag_function_number
from functions.get_nag_function_type import get_nag_function_type
from functions.validate_nag_function_name import validate_nag_function_name


class Nag:

    def __init__(self, name, description=None):
        # General information
        self.name = name
        self.description = None
        self.file_base_name = None
        # Statistics
        self._constant_number = None
        self._input_number = None
        self._nand_number = None
        self._output_number = None
        self._nag_function_domain_size = None
        self._input_to_output_min_distance = None
        self._input_to_output_max_distance = None
        # Graph
        self._graph = nx.MultiDiGraph()
        # Sorted lists
        self._constant_functions = None
        self._input_functions = None
        self._nand_functions = None
        self._output_functions = None
        self._all_functions = None
        # Execution tools
        self._ett = None  # Extended Truth Table
        self._lambdas = None
        # Counters
        self.max_input_function_number = 0
        self.max_nand_function_number  = 0
        self.max_output_function_number  = 0
        self._mode = 'design'
        self._add_constant(0)
        self._add_constant(1)

    def _add_constant(self, number):
        self.assure_function("c" + str(number))

    def _pick_next_input_number(self):
        """
        BUG: to support the usage of both automatically and manually numbered items, we should query the graph to find the next truly available number.
        """
        number = self.max_input_function_number + 1
        self.max_input_function_number = number
        return number

    def _pick_next_nand_number(self):
        """
        BUG: to support the usage of both automatically and manually numbered items, we should query the graph to find the next truly available number.
        """
        number = self.max_nand_function_number + 1
        self.max_nand_function_number = number
        return number

    def _pick_next_output_number(self):
        """
        BUG: to support the usage of both automatically and manually numbered items, we should query the graph to find the next truly available number.
        """
        number = self.max_output_function_number + 1
        self.max_output_function_number = number
        return number

    def assure_function(self, function_name):
        """
        BUG: If assure already existing node, ensure we OVERWRITE it.
        """
        if not validate_nag_function_name(function_name):
            raise ValueError('Invalid NAG function name', function_name)
        if function_name not in self._graph.nodes:
            self._graph.add_node(
                function_name,
                function_type=get_nag_function_type(function_name),
                function_number=get_nag_function_number(function_name),
                shape="circle",
                label=function_name)
        return function_name

    def get_input_to_output_max_distance(self):
        """
        Returns the maximal distance between an input and output node statistic measured in numbers of intermediary NAND nodes.

        :return:
        int: the maximal distance between an input and output node.
        """
        return self._input_to_output_max_distance

    def get_input_to_output_min_distance(self):
        """
        Returns the minimal distance between an input and output node statistic measured in numbers of intermediary NAND nodes.

        :return:
        int: the minimal distance between an input and output node.
        """
        return self._input_to_output_min_distance

    def get_predecessors(self, function_name):
        """
        Return the set of direct predecessor functions to f.
        :param function_name:
        :return:
        """
        return self._graph.predecessors(function_name)

    def get_predecessors_as_list(self, function_name):
        # For NAGs, only NAND functions of multiple inputs.
        # And for NANDs, the order of inputs as no importance.
        # Hence we may convert dictionaries into lists without fear.
        # But this would no longer be true for flexible algo graphs
        # to be implemented in future classes.
        return list(self.get_predecessors(function_name))

    def get_successors(self, function_name):
        return self._graph.successors(function_name)

    def get_successors_as_list(self, function_name):
        # For NAGs, only NAND functions of multiple inputs.
        # And for NANDs, the order of inputs as no importance.
        # Hence we may convert dictionaries into lists without fear.
        # But this would no longer be true for flexible algo graphs
        # to be implemented in future classes.
        return list(self.get_successors(function_name))

    def get_successors_max_number(self, function_name):
        """
        Return the maximal function number amongst the successor of a function that are of the same type.
        Checking the type is important because function numbers are only significant within a function type.
        :param function_name: (string) the function name.
        :return: (int) the maximal function number amongst the function successors.
        """
        successors_max_number = None
        successors = self.get_successors(function_name)
        for successor in successors:
            if get_nag_function_type(successor) == get_nag_function_type(function_name):
                if successors_max_number is None or successors_max_number < get_nag_function_number(successor):
                    successors_max_number = get_nag_function_number(successor)
        return successors_max_number

    def get_successors_min_number(self, function_name):
        """
        Return the minimal function number amongst the successor of a function that are of the same type.
        Checking the type is important because function numbers are only significant within a function type.
        :param function_name: (string) the function name.
        :return: (int) the minimal function number amongst the function successors.
        """
        successors_min_number = None
        successors = self.get_successors(function_name)
        for successor in successors:
            if get_nag_function_type(successor) == get_nag_function_type(function_name):
                if successors_min_number is None or successors_min_number > get_nag_function_number(successor):
                    successors_min_number = get_nag_function_number(successor)
        return successors_min_number

    def get_predecessors_max_number(self, function_name):
        """
        Return the maximal function number amongst the predecessor of a function that are of the same type.
        Checking the type is important because function numbers are only significant within a function type.
        :param function_name: (string) the function name.
        :return: (int) the maximal function number amongst the function predecessors.
        """
        predecessors_max_number = None
        predecessors = self.get_predecessors(function_name)
        for predecessor in predecessors:
            if get_nag_function_type(predecessor) == get_nag_function_type(function_name):
                if predecessors_max_number is None or predecessors_max_number < get_nag_function_number(predecessor):
                    predecessors_max_number = get_nag_function_number(predecessor)
        return predecessors_max_number

    def get_predecessors_min_number(self, function_name):
        """
        Return the minimal function number amongst the predecessor of a function that are of the same type.
        Checking the type is important because function numbers are only significant within a function type.
        :param function_name: (string) the function name.
        :return: (int) the minimal function number amongst the function predecessors.
        """
        predecessors_min_number = None
        predecessors = self.get_predecessors(function_name)
        for predecessor in predecessors:
            if get_nag_function_type(predecessor) == get_nag_function_type(function_name):
                if predecessors_min_number is None or predecessors_min_number > get_nag_function_number(predecessor):
                    predecessors_min_number = get_nag_function_number(predecessor)
        return predecessors_min_number

    def get_statistics(self):
        report = """Constants: {0}
Inputs: {1}
NANDs: {2}
Outputs: {3}
Min. I/O distance: {4}
Max. I/O distance: {5}""".format(
            self._constant_number,
            self._input_number,
            self._nand_number,
            self._output_number,
            self._input_to_output_min_distance,
            self._input_to_output_max_distance)
        return report

    def set_design_mode(self):
        self._mode = 'design'
        # Sorted lists
        self._constant_functions = None
        self._input_functions = None
        self._nand_functions = None
        self._output_functions = None
        self._all_functions = None
        # Reset statistics
        self._constant_number = None
        self._input_number = None
        self._nand_number = None
        self._output_number = None
        self._nag_function_domain_size = None
        # Execution tooling
        self._ett = None
        self._lambdas = None
        logging.info('nag.mode: design')

    def set_execution_mode(self):
        # Populate cached sorted lists
        # TRICK: the desired sequence of c,i,n,o happens to match the alphabetical order, hence we may sort items. This trick wouldn't work in different classes with distinct function types.
        self._all_functions = sorted(self._graph.nodes, key=lambda n: (get_nag_function_type(n), get_nag_function_number(n)))
        self._constant_functions = sorted(filter(lambda i: get_nag_function_type(i) == 'c', self._graph.nodes), key=lambda n: (get_nag_function_type(n), get_nag_function_number(n)))
        self._input_functions = sorted(filter(lambda i: get_nag_function_type(i) == 'i', self._graph.nodes), key=lambda n: (get_nag_function_type(n), get_nag_function_number(n)))
        self._nand_functions = sorted(filter(lambda i: get_nag_function_type(i) == 'n', self._graph.nodes), key=lambda n: (get_nag_function_type(n), get_nag_function_number(n)))
        self._output_functions = sorted(filter(lambda i: get_nag_function_type(i) == 'o', self._graph.nodes), key=lambda n: (get_nag_function_type(n), get_nag_function_number(n)))
        # Compute statistics
        self._all_number = len(self._all_functions)
        self._constant_number = len(self._constant_functions)
        self._input_number = len(self._input_functions)
        self._nand_number = len(self._nand_functions)
        self._output_number = len(self._output_functions)
        self._nag_function_domain_size = pow(2, self._input_number)
        for i in self._input_functions:
            for o in self._output_functions:
                spl = None
                try:
                    spl = nx.shortest_path_length(self._graph, i, o)
                #except nx.exception.NetworkXNoPath:
                    #print('no big deal')
                finally:
                    if spl is not None:
                        # The unit to measure the distance is the number
                        # of nand intermediary functions. We must thus
                        # remove the output node from the path:
                        spl = spl - 1
                        if self._input_to_output_min_distance is None or self._input_to_output_min_distance > spl:
                            self._input_to_output_min_distance = spl
                        if self._input_to_output_max_distance is None or self._input_to_output_max_distance < spl:
                            self._input_to_output_max_distance = spl
        # Initialize extended truth table
        # DESIGN FLAW: For large domain functions, implement a sparse array
        self._ett = ma.masked_all(
            shape=(self._nag_function_domain_size, self._all_number),
            dtype=np.int8)
        # Configure lambdas
        self._lambdas = {}
        for function_item in self._all_functions:

            def lambda_item(nag, function_name, input_value):
                logging.error('UNDEFINED LAMBDA FUNCTION: {%s}(%s)', function_name, input_value)
                return None

            closure_default_1 = None
            closure_default_2 = None
            if get_nag_function_type(function_item) == 'c':
                constant_value = get_nag_function_number(function_item)

                def lambda_item(nag, function_name, input_value, constant_value=constant_value):
                    return_value = constant_value
                    logging.debug('%s(%s, %s) = %s', function_name, input_value, constant_value, return_value)
                    nag.set_ett_value(input_value, function_name, return_value)
                    return return_value

            if get_nag_function_type(function_item) == 'i':
                input_index = get_nag_function_number(function_item) - 1

                def lambda_item(nag, function_name, input_value, input_index=input_index):
                    return_value = input_value[input_index]
                    logging.debug('%s(%s, %s) = %s', function_name, input_value, input_index, return_value)
                    nag.set_ett_value(input_value, function_name, return_value)
                    return return_value

            if get_nag_function_type(function_item) == 'n':
                predecessors = []
                for predecessor in self.get_predecessors(function_item):
                    predecessors.append(predecessor)
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

                def lambda_item(nag, function_name, input_value, predecessor_1=predecessor_1, predecessor_2=predecessor_2):
                    return_value = (
                        0 if (nag.lambdas[predecessor_1](nag, function_name, input_value) == 1 and
                              nag.lambdas[predecessor_2](nag, function_name, input_value) == 1) else
                        1)
                    logging.debug('%s(%s, %s, %s) = %s', function_name, input_value, predecessor_1, predecessor_2, return_value)
                    nag.set_ett_value(input_value, function_name, return_value)
                    return return_value

            if get_nag_function_type(function_item) == 'o':
                predecessors = self.get_predecessors(function_item)
                predecessor_1 = next(predecessors)

                def lambda_item(nag, function_name, input_value, predecessor_1=predecessor_1):
                    return_value = nag.lambdas[predecessor_1](nag, function_name, input_value)
                    logging.debug('%s(%s, %s) = %s', function_name, input_value, predecessor_1, return_value)
                    nag.set_ett_value(input_value, function_name, return_value)
                    return return_value

            self._lambdas[function_item] = lambda_item
        # Set mode
        self._mode = 'execution'
        logging.info('nag.mode: execution')

    def execute(self, input_value):
        logging.debug('nag.execute(%s)', input_value)
        # GENERAL IDEA:
        for function_name in self.all_functions:
            lambda_function = self._lambdas[function_name]
            output_value = lambda_function(self, function_name, input_value)
        # Retrieve the output bits from ett
        return self.ett[self.convert_input_to_ett_y_index(input_value), :]

    def execute_list(self, input_list):
        output_dict = {}
        for input_value in input_list:
            output_value = self.execute(input_value)
            output_dict[input_value] = output_value
        return output_dict

    def execute_all(self):
        output_dict = {}
        for integer_value in range(0, self.nag_function_domain_size - 1):
            bit_array = convert_int_to_bit_array(integer_value)
            output_value = self.execute(bit_array)
            output_dict[bit_array] = output_value
        return output_dict

    def convert_function_name_to_ett_x_index(self, function_name):
        return self._all_functions.index(function_name)

    def convert_input_to_ett_y_index(self, input_value):
        if self.input_number == 0 and input_value is None:
            # When the NAG has no inputs (i.e. it is only based on constant values),
            # by convention the ETT is represented with a single row without inputs.
            # Hence, we must assign index 0 (but with a different meaning,
            # because 0 in this new context mean "first and only row"
            # while it means "the corresponding integer value" when it is linked
            # to usual inputs.
            return 0
        else:
            # Otherwise, in the usual case, at least one input is contained
            # in the NAG and the index positioning of the the input value
            # is equal to its corresponding integer value.
            return convert_bit_array_to_int(input_value)

    def set_ett_value(self, input_value, function_name, binary_value):
        logging.debug('set_ett_value(%s, %s, %s)', input_value, function_name, binary_value)
        input_index = self.convert_input_to_ett_y_index(input_value)
        function_index = self.convert_function_name_to_ett_x_index(function_name)
        self._ett[input_index, function_index] = binary_value

    def get_ett_value(self, input_value, function_name):
        logging.debug('get_ett_value(%s, %s)', input_value, function_name)
        input_index = self.convert_input_to_ett_y_index(input_value)
        function_index = self.convert_function_name_to_ett_x_index(function_name)
        return self._ett[input_index, function_index]

    def set_nand(self, input_1, input_2, function):
        # PARAMETERS VALIDATION
        self.assure_function(input_1)
        self.assure_function(input_2)
        self.assure_function(function)
        if get_nag_function_type(input_1) not in ['c','i','n']:
            raise ValueError('Invalid NAND input type', input_1)
        if get_nag_function_type(input_2) not in ['c','i','n']:
            raise ValueError('Invalid NAND input type', input_2)
        if get_nag_function_type(function) != 'n':
            raise ValueError('Invalid NAND function type', function)
        if (get_nag_function_type(input_1) == 'n' and 
            get_nag_function_number(input_1) >= get_nag_function_number(function)):
            raise ValueError('NAND input 1 number is greater or equal than NAND function number', input_1, function)
        if (get_nag_function_type(input_2) == 'n' and 
            get_nag_function_number(input_2) >= get_nag_function_number(function)):
            raise ValueError('NAND input 2 number is greater or equal than NAND function number', input_2, function)       
        # CLEANUP OLD PREDECESSOR EDGES IF ANY
        self.remove_vertex_inbound_edges(function)
        # FUNCTION LOGIC
        self._graph.add_edge(input_1, function, input_number=1)
        self._graph.add_edge(input_2, function, input_number=2)

    def remove_vertex_inbound_edges(self, function_name):
        """Remove all inbound edges, that is edges coming from predecessors"""
        for predecessor in self.get_predecessors_as_list(function_name):
            self._graph.remove_edge(predecessor, function_name)

    def set_output(self, input_1, function):
        # PARAMETERS VALIDATION
        self.assure_function(input_1)
        self.assure_function(function)
        if get_nag_function_type(input_1) not in ['c','i','n']:
            raise ValueError('Invalid output input type', input_1)
        if get_nag_function_type(function) != 'o':
            raise ValueError('Invalid output function type', function)
        # FUNCTION LOGIC
        self._graph.add_edge(input_1, function, input_number = 1)

    def to_json(self):
        return convert_nag_to_json(self)

    @property
    def graph(self):
        return self._graph

    @property
    def all_functions(self):
        return self._all_functions

    @property
    def all_number(self):
        """
        The number of vertices contained in the NAG graph, equal to the sum of:
        - the number of constant vertices,
        - the number of input vertices,
        - the number of NAND vertices,
        - the number of output vertices.
        :return: (int) number of vertices.
        """
        return self._all_number

    @property
    def constant_number(self):
        """
        The number of constant vertices contained in the NAG graph, always equal to 2 (0 and 1).
        :return: (int) 2.
        """
        return self._constant_number

    @property
    def input_number(self):
        """
        The number of input vertices contained in the NAG graph, between 0 (for constant functions) and n.
        :return: (int) number of input bits.
        """
        return self._input_number

    @property
    def nand_number(self):
        return self._nand_number

    @property
    def output_number(self):
        return self._output_number

    @property
    def lambdas(self):
        """The lambda functions are the dynamic pythonic functions
        that are generated by the NAG when mode is set to execution
        and that correspond to the graph node functions """
        return self._lambdas

    @property
    def ett(self):
        """ETT (Extended Truth Table)"""
        return self._ett

    @property
    def nag_function_domain_size(self):
        return self._nag_function_domain_size

    @property
    def input_number(self):
        """The number of input vertices in the NAG"""
        return self._input_number
