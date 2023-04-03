"""
CSC111 Winter 2023 Project: ClariPy

This module contains the visualizing functions for the project
"""

from __future__ import annotations
from typing import Any, Optional

import igraph as ig
import plotly.graph_objects as go
import classes
from modules import claripy_parser, python_to_lang


class Tree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.

    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not None or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
        Return whether this tree is empty.
        """
        return self._root is None

    def __str__(self) -> str:
        """
        Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """
        Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def insert(self, subtree: Tree) -> None:
        """
        Inserts the given tree into self as a new subtree.

        Preconditions:
            - self.root is not None
        """
        self._subtrees.append(subtree)

    def get_root(self) -> any:
        """
        Returns the root item of this tree
        """
        return self._root

    def get_subtrees(self) -> list[Tree]:
        """
        Returns this tree's list of subtrees
        """
        return self._subtrees

    def add_statement(self, item: classes.Statement | classes.Expr) -> None:
        """
        Mutating helper function to recursively insert each
        statement or expression in a module's body into the tree
        """
        if not isinstance(item, (classes.Expr, classes.Statement)):
            raise Exception('File contains pesudocode not within specifications')

        if isinstance(item, (classes.Num, classes.Str, classes.List, classes.Bool)):
            typ = f'{type(item)}'.split('.')[-1].replace('\'>', '')
            subtree = Tree(typ, [])
            subtree.insert(Tree(item.evaluate({}), []))
            self.insert(subtree)
        elif isinstance(item, classes.Name):
            subtree = Tree('Variable', [])
            subtree.insert(Tree(item.id, []))
            self.insert(subtree)
        elif isinstance(item, classes.Subscript):
            subtree = Tree('List Index', [])
            lst = Tree('List', [])
            index = Tree('Index', [])
            lst.add_statement(item.lst)
            index.add_statement(item.index)
            subtree.insert(lst)
            subtree.insert(index)
            self.insert(subtree)
        elif isinstance(item, classes.BinOp):
            subtree = Tree('Binary Op.', [])
            subtree.add_statement(item.left)
            subtree.insert(Tree(item.op, []))
            subtree.add_statement(item.right)
            self.insert(subtree)
        elif isinstance(item, classes.BoolOp):
            subtree = Tree('Bool Op.', [])
            subtree.add_statement(item.left)
            subtree.insert(Tree(item.op, []))
            subtree.add_statement(item.right)
            self.insert(subtree)
        elif isinstance(item, classes.Assign):
            subtree = Tree('Assign', [])
            subtree.add_statement(item.target)
            subtree.add_statement(item.value)
            self.insert(subtree)
        elif isinstance(item, classes.Print):
            subtree = Tree('Print', [])
            subtree.add_statement(item.arg)
            self.insert(subtree)
        elif isinstance(item, classes.While):
            subtree = Tree('While Loop', [])
            cond = Tree('Condition', [])
            body = Tree('Body', [])
            cond.add_statement(item.test)
            for stm in item.body:
                body.add_statement(stm)
            subtree.insert(cond)
            subtree.insert(body)
            self.insert(subtree)
        elif isinstance(item, classes.If):
            subtree = Tree('Branch', [])
            cond = Tree('Conditon', [])
            body = Tree('If-Body', [])
            if not item.orelse:
                pass
            else:
                orelse = Tree('Orelse', [])
                for stm in item.orelse:
                    orelse.add_statement(stm)
                subtree.insert(orelse)
            cond.add_statement(item.test)
            for stm in item.body:
                body.add_statement(stm)
            subtree.insert(cond)
            subtree.insert(body)
            self.insert(subtree)


def format_module(module: classes.Module) -> Tree:
    """
    Converts an ast module class into a tree
    """
    tree = Tree('Module', [])

    for item in module.body:
        tree.add_statement(item)

    return tree


def make_graph(tree: Tree) -> ig.Graph:
    """
    Generates an igraph Graph object from the given tree by calling the helper add_node_to_graph

    Preconditions:
        - tree.get_root() is not None
    """
    g = ig.Graph()
    add_node_to_graph(g, None, tree)
    return g


def add_node_to_graph(graph: ig.Graph, parent_node: Optional[Tree], tree: Tree) -> None:
    """
    Mutating recursive helper that adds each node to the given igraph graph as a new vertex and creates an edge between
    each parent and its child

    Preconditions:
        - tree.get_root() is not None
    """
    graph.add_vertex(name=str(id(tree)), content=tree.get_root())
    if parent_node is not None:
        parent_id = graph.vs.find(name=str(id(parent_node))).index
        tree_id = graph.vs.find(name=str(id(tree))).index
        graph.add_edge(parent_id, tree_id)
    for child in tree.get_subtrees():
        add_node_to_graph(graph, tree, child)


def make_figure(graph: ig.Graph) -> go.Figure:
    """
    Turns the given graph into a plotly figure using the Reingold Tilford algorithm to generate the positions
    of each node in the tree

    Preconditions:
        - graph is not empty
    """
    fig = go.Figure()
    coords = graph.layout_reingold_tilford(mode="out", root=[0])
    ids = graph.vs['name']
    max_y = max({coord[1] for coord in coords})
    x = []
    y = []
    x_v = []
    y_v = []
    for i in range(len(coords)):
        x.append(([ids[i]], coords[i][0]))
        y.append(([ids[i]], 2 * max_y - coords[i][1]))
        x_v.append(coords[i][0])
        y_v.append(2 * max_y - coords[i][1])

    for edge in graph.es:
        xy0_index = ids.index(graph.vs[edge.source]['name'])
        xy1_index = ids.index(graph.vs[edge.target]['name'])
        x0, y0 = x[xy0_index][1], y[xy0_index][1]
        x1, y1 = x[xy1_index][1], y[xy1_index][1]
        fig.add_shape(
            type="line",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            line=dict(color='rgb(169, 169, 169)', width=1),
            layer='below'
        )

    fig.add_trace(go.Scatter(
        x=x_v,
        y=y_v,
        mode="markers+text",
        text=graph.vs['content'],
        textposition="middle center",
        marker=dict(color='rgb(169, 169, 200)', size=30),
        hoverinfo='none'
    ))

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Output Tree',
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis
                      )

    return fig


def python_to_english(filename: str) -> None:
    """
    Given a filename for a python file, create an abstract syntax tree and convert the python code
    into English pseudocode

    Preconditons:
        - '.py' in filename
        - filename represents a file with only the allowed subset of python code
    """
    with open(filename) as f:
        program = f.read()
    tree = python_to_lang.ast.parse(program)
    fig = go.Figure()
    axis = dict(showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.add_annotation(
        text=str(tree),
        showarrow=False,
        font=dict(size=16, color='black')
    )

    fig.update_layout(title='Output Pseudocode',
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      plot_bgcolor='rgba(0,0,0,0)'
                      )
    fig.show()


def english_to_python(filename: str) -> None:
    """
    Given a filename for a file with valid pseudocode, turns the pesudocode into python code using an abstract
    syntax tree, visualizing the tree with a plotly plot

    Preconditons:
        - filename represents a file with only the allowed subset of pesudocode
    """
    program = claripy_parser.parse_module(filename)
    tree = format_module(program)
    graph = make_graph(tree)
    fig = make_figure(graph)
    fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'allowed-io': ['Print.evaluate', 'tokenize'],
        'extra-imports': ['classes', 're', 'igraph', 'plotly.graph_objects'],
        'disable': ['abstract-method', 'syntax-error']
    })
