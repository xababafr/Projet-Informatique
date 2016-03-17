# -*- coding: utf-8 -*-
# Inheritance would be a better choice instead of this decorator but
# we want to keep this code as simple as possible for the students


class Node:

    def __init__(self, data):  # next est un mot clé
        self.content = data
        self.next = None

    def __str__(self):
        return "\n\tThis node contains data whose type and content are:\n\t\t"\
            + str(type(self.content)) + " " + str(self.content)


class CustomList:

    def __init__(self):
        # ghost node
        self.first = Node(None)

    def append(self, data):
        self.insert(data, float("inf"))

    def insert_first(self, data):
        """
        Create a new Node, set data as its content and put it as the beginning
        of the list
        """
        # never erase the first (ghost) node, it is much easier to code
        # a chained list this way as you will see in this tutorial. A ghost
        # node is a Node with no content (None) put at the beginning of the
        # list. It is used as a hidden and fixed reference to the beginning
        # of the list. Beware, even if its content is None its next element
        # will most probably be a Node and not the None object unless the list
        # is empty.

        # The list will look like this:

        # Ghost-->1st "actual" node--->2nd node->...>last node-->None
        #   |               |           |              |
        #   |               |           |              |
        #   |               |           |              |
        # None         Some content     |              |
        #                           Another content    |
        #                                           Yet another one
        #
        #
        # E.g if you build a list of integers, say 42, 12 and 69
        # Ghost-->1st "real" node--->2nd node->last node-->None
        #   |               |           |              |
        #   |               |           |              |
        #   |               |           |              |
        # None             42          12             69

        # Now let's see how to insert an element at the beginning of the list

        # first create a new node and set its content to data
        new_node = Node(data)

        # then get a reference to the first node of the list with an actual
        # content. If the list contains only the ghost Node then
        # self.first.next is a reference to the None object and that's fine.
        tmp = self.first.next

        # then set new node as the first actual node
        self.first.next = new_node

        # finally set the next node of new_node to be the old first actual node
        new_node.next = tmp

    def insert(self, data, idx):
        """Encapsulate data into a Node and append it to the list"""
        if idx < 0:
            print("Can not insert at negative index")
            return False
        new_node = Node(data)
        cur_node = self.first
        node_idx = 0
        while cur_node.next is not None and node_idx != idx:
            cur_node = cur_node.next
            node_idx += 1
        tmp = cur_node.next
        new_node.next = tmp
        cur_node.next = new_node
        return True

    def insert_last(self, data):
        cur_node = self.first
        node_idx = 0
        while cur_node.next is not None:
            node_idx += 1
            cur_node = cur_node.next
        return self.insert(data, node_idx)

    def search(self, data):
        cur_node = self.first
        node_idx = 0
        while cur_node.next is not None:
            if data == cur_node.next.content:
                return node_idx
            node_idx += 1
            cur_node = cur_node.next
        return None

    def delete(self, data):
        cur_node = self.first
        prev_node = None

        while cur_node.next is not None:
            if data == cur_node.next.content:
                cur_node.next = cur_node.next.next
                return True
            prev_node = cur_node
            cur_node = cur_node.next
        if data == cur_node.content:
            prev_node.set_next(None)
            return True
        return False

    def __str__(self):
        n = self.first
        content_str = "The nodes in this list are: "
        while n is not None:
            content_str += str(n)
            n = n.next
        return content_str

