from typing import *

class Node:
    """
    A class to represent a node in a tree

    Attributes:
        any data: Data held by the node
        Node parent: Parent node
        List children: List of child nodes
        bool visited: Has this been visited?
    """
    def __init__(self, data: any):
        """
        Constructor

        Args:
            any data: Data for the node
        """
        self.data = data
        self.parent = None
        self.children = None
        self.visited = False


    def add_child(self, data: any):
        """
        Add child node to this node

        Args:
            any data: Data for the new node
        """
        node = Node(data)
        node.parent = self
        if self.children is None:
            self.children = [node]
        else:
            self.children.append(node)
        return node
    
    
    def set_visited(self, val: bool):
        """
        Mark node as visited

        Args:
            bool visited: New value
        """
        self.visited = val


class Tree:
    """
    Class representing a n-ary tree

    Attributes:
        Node root: Root node
    """
    def __init__(self, data):
        self.root = Node(data)