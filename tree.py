from typing import *

class Node:
    """
    A class to represent a node in a tree

    Attributes:
        any data: Data held by the node
        Node parent: Parent node
        List children: List of child nodes
    """
    def __init__(self, data: any):
        """
        Constructor

        Args:
            any data: Data for the node
        """
        self.data = data
        self.parent = None
        self.children = list()


    def add_child(self, data: any):
        """
        Add child node to this node

        Args:
            any data: Data for the new node
        """
        node = Node(data)
        node.parent = self
        self.children.append(node)
        return node
    

    def set_visited(self, val: bool):
        """
        Mark node as visited

        Args:
            bool visited: New value
        """
        self.visited = val