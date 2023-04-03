"""
CSC111 Winter 2023 Project: ClariPy

This module contains the visualizer for the project
"""
from __future__ import annotations

import parser
import tkinter as tk
from tkinter import filedialog
from typing import Any, Optional

import classes
import igraph as ig
import plotly.graph_objects as go
import python_to_lang


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

    def add_statement(self, item: classes.Statement | classes.Expr) -> None:
        """
        Mutating helper function to recursively insert each 
        statement or expression in a module's body into the tree
        """
        if isinstance(item, (classes.Num, classes.Str, classes.List, classes.Bool)):
            type = f'{classes.Num}'.split('.')[-1].replace('\'>', '')
            subtree = Tree(type, [])
            subtree.insert(Tree(item.evaluate({}), []))
        elif isinstance(item, classes.Name):
            subtree = Tree('Variable Name', [])
            subtree.insert(Tree(item.id, []))
        elif isinstance(item, classes.Subscript):
            subtree = Tree('List Indexing', [])
            lst = Tree('List', [])
            index = Tree('Index', [])
            lst.add_statement(item.lst)
            index.add_statement(item.index)
            subtree.insert(lst)
            subtree.insert(index)
        elif isinstance(item, classes.BinOp):
            subtree = Tree('Binary Operation', [])
            subtree.add_statement(item.left)
            subtree.insert(Tree(item.op, []))
            subtree.add_statement(item.right)
        elif isinstance(item, classes.BoolOp):
            subtree = Tree('Bool Operation', [])
            subtree.add_statement(item.left)
            subtree.insert(Tree(item.op, []))
            subtree.add_statement(item.right)
        elif isinstance(item, classes.Assign):
            subtree = Tree('Assign', [])
            subtree.add_statement(item.target)
            subtree.add_statement(item.value)
        elif isinstance(item, classes.Print):
            subtree = Tree('Print', [])
            subtree.add_statement(item.arg)
        elif isinstance(item, classes.While):
            subtree = Tree('While Loop', [])
            cond = Tree('Condition', [])
            body = Tree('Body', [])
            cond.add_statement(item.test)
            for stm in item.body:
                body.add_statement(stm)
            subtree.insert(cond)
            subtree.insert(body)
        else:
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

graph = ig.Graph()

def add_node_to_graph(graph: ig.Graph, parent_node: Optional[Any], tree: Tree) -> None:
    """
    G
    """
    graph.add_vertex(name=tree._root)
    if parent_node is not None:
        graph.add_edge(parent_node._root, tree._root)
    for child in tree._subtrees:
        add_node_to_graph(graph, node, child)



# window = tk.Tk()
# window.title('ClariPy')
# window.geometry('500x500')
# window.config(background='black')
# path = filedialog.askopenfilename(
#     initialdir='/', 
#     title='Select file',
#     filetypes=(('txt files', '*.txt'),))

# btn_ptl = tk.Button(window, text='Python to English', command=...)
# btn_ltp = tk.Button(window, text='English to Python', command=...)

# btn_ptl.grid(column = 2, row = 1)
# btn_ltp.grid(column = 1, row = 1)
# window.mainloop()