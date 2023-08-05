# encoding: utf-8

import numpy as np

from .heap import Heap
from .heap import HeapPair


class HeapBrother(Heap):


    pass




class HeapBrotherPair(HeapBrother, HeapPair):


    pass




class HeapBrotherPairMax(HeapBrotherPair):



    @property
    def node_max(self):

        return self._heap




    @property
    def node_min(self):
        if self.empty:
            return None

        if 1 == len(self._seq):
            return self._heap

        idx = self._seq.tail_index()

        node = self._seq.tail()
        for n in self._seq[idx+1:]:
            if n.key < node.key:
                node = n

        return node




    def swap(self, node):

        # update tree
        ancestor         = node.parent
        descendant_left  = node.child_left.children
        descendant_right = node.child_right.children

        nodes      = np.array([node, node.child_left, node.child_right])
        nodes_keys = [n.key for n in nodes]

        idx = np.argsort(nodes_keys)[::-1]
        
        root, left, right = nodes[idx]

        root.parent = ancestor
        root.setas_leaf()
        root.children.append(left)
        root.children.append(right)

        left.parent    = root
        left.children  = descendant_left
        
        right.parent   = root
        right.children = descendant_right

        # update ancestor and descendant info
        if ancestor:
            if ancestor.child_left == node:
                ancestor.child_left = root
            else:
                ancestor.child_right = root

        for n in descendant_left:
            n.parent = left

        for n in descendant_right:
            n.parent = right

        # update seq
        nodes_index = [self._seq.index(n) for n in nodes]
        nodes       = nodes[idx]
        self._seq[nodes_index] = nodes

        # update root
        if root.root():
            self._heap = root

        return root, idx



    def swap_down(self, node):

        if node.leaf():
            return []

        elif node.left_only():

            if node.key >= node.child_left.key:
                return []
            else:
                # update root
                if node.root():
                    self._heap = node.child_left

                # update seq
                nodes       = [node, node.child_left]
                nodes_index = [self._seq.index(n) for n in nodes]
                nodes       = nodes[::-1]
                self._seq[nodes_index] = nodes

                # update tree
                ancestor   = node.parent
                descendant = node.child_left.children

                # update ancestor and descendant info
                if ancestor:
                    if ancestor.child_left == node:
                        ancestor.child_left = node.child_left
                    else:
                        ancestor.child_right = node.child_left

                for n in descendant:
                    n.parent = node

                # update tree
                node.child_left.parent = ancestor
                node.child_left.setas_leaf() 
                node.child_left.children.append(node)

                node.parent   = node.child_left
                node.children = descendant

                return [node]

        else:
            root, idx = self.swap(node)

            tbd = []
            if 1 != idx[1]:
                tbd.append(root.child_left)
            if 2 != idx[2]:
                tbd.append(root.child_right)

            return tbd



    def swap_up_brother(self, node):

        if not node or node.root():
            return [], []

        elif node.parent.left_only():

            if node.parent.key >= node.key:
                return [], []
            else:
                node_parent = node.parent

                # update root
                if node_parent.root():
                    self._heap = node

                # update seq
                nodes       = [node_parent, node]
                nodes_index = [self._seq.index(n) for n in nodes]
                nodes       = nodes[::-1]
                self._seq[nodes_index] = nodes

                # update tree
                ancestor   = node_parent.parent
                descendant = node.children
                node.setas_root()
                node.setas_leaf()

                # update ancestor and descendant info
                if ancestor:
                    if ancestor.child_left == node_parent:
                        ancestor.child_left = node
                    else:
                        ancestor.child_right = node

                node_parent.setas_root()

                for n in descendant:
                    n.parent = node_parent

                # update tree
                node_parent.children = descendant

                node.child_left      = node_parent
                node.parent          = ancestor

                node_parent.parent   = node

                return [node.child_left], []

        else:
            root, idx = self.swap(node.parent)

            tbd_up      = []
            tbd_brother = []

            if 1 == idx[0]:
                tbd_up.append(root)
            
            elif 1 == idx[2]:
                tbd_brother.append(root.child_right)

            return tbd_up, tbd_brother



    def tune(self, node):

        if node.root():
            self.tune_down(node)

        elif node.leaf():
            self.tune_up_brother(node)

        elif node.child_right and node.child_right.key > node.key:
            self.tune_down(node)

        elif node.child_left and node.child_left.key > node.key:
            self.tune_down(node)

        else:
            self.tune_up_brother(node)



    def have(self, key):

        nodes = [self._heap]

        while(nodes):
            node_current = nodes.pop()

            if key == node_current.key:
                return True

            elif node_current.child_left and key == node_current.child_left.key:
                return True

            elif node_current.child_right and key == node_current.child_right.key:
                return True

            elif node_current.child_right and key < node_current.child_right.key:
                nodes.append(node_current.child_right)
                nodes.append(node_current.child_left)

            elif node_current.child_left and key < node_current.child_left.key:
                nodes.append(node_current.child_left)

        return False
