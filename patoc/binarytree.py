from __future__ import annotations

########################### TreeNode (for binary tree) class ############################
class TreeNode:
    """Class of nodes for binary trees"""

    def __init__(self, data) -> None:
        self.data = data
        self._left = None
        self._right = None
    
    @property
    def left(self) -> TreeNode:
        return self._left
    
    @property
    def right(self) -> TreeNode:
        return self._right
    
    @left.setter
    def left(self, l: TreeNode) -> None:
        self._left = l

    @left.setter
    def right(self, r: TreeNode) -> None:
        self._right = r

########################### Binary tree class ############################
class BinaryTree:
    """Class of binary tree"""

    def __init__(self, expression) -> None:
        self._expression = expression
        self._root = None
    
    @property
    def root(self) -> TreeNode:
        return self._root