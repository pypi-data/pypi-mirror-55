from functions.get_nag_function_type import get_nag_function_type
import networkx as nx
from graphviz import Digraph


def convert_nag_networkx_to_graphviz(nag, format='svg'):
    """
    format: 'svg' (default), 'png', 'pdf',... reference: https://www.graphviz.org/doc/info/output.html
    """
    graphviz_digraph = Digraph(format=format) #png #'finite_state_machine', filename='nag.gv')
    graphviz_digraph.attr(rankdir='LR', size='8,5')
    for vertex in nag.graph.nodes:
        if get_nag_function_type(vertex) == 'c':
            graphviz_digraph.attr('node', shape='doublecircle')
        elif get_nag_function_type(vertex) == 'i':
            graphviz_digraph.attr('node', shape='doublecircle')
        elif get_nag_function_type(vertex) == 'n':
            graphviz_digraph.attr('node', shape='circle')
        elif get_nag_function_type(vertex) == 'o':
            graphviz_digraph.attr('node', shape='doublecircle')
        else:
            graphviz_digraph.attr('node', shape='circle')
        graphviz_digraph.node(vertex)
    for edge in nag.graph.edges:
        ancestor_vertex = edge[0]
        successor_vertex = edge[1]
        graphviz_digraph.edge(ancestor_vertex, successor_vertex)
    return graphviz_digraph
