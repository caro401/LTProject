class _Node:
    def __init__(self, key, data=None, next_node=None):
        self.key = key
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self, head):
        self.head = head

    def list_insert(self, item):
        """
        Insert item at the head of the list.
        :param item: _Node item to be inserted
        :return:
        """
        item.next_node = self.head  # make item point to the current head of the list
        self.head = item  # make item be the new head of the list

    def list_search(self, key):
        """
        Traverse the linked list until you find a node with the specified key
        :param key: The key you are looking for
        :return: The _Node object with the key you are looking for, or None if it is not in the list
        """
        x = self.head  # start at the head of the list
        while x is not None and x.key != key:  # while there is still a node to look at, and you don't match the key
            x = x.next_node  # look at the next node in the list
        return x  # this executes when you have run out of list, or matched the key

    def list_delete(self, node):
        """
        Delete the specified node from the list, by changing the pointer on the node before to point at the next node.
        :param node: the node you want to delete
        :return:
        """
        prev = self.head  # start at the head of the list
        if prev is not None:  # if there are some items in the list
            # while you haven't matched the node, and there are more nodes to look at
            while prev.next_node != node and prev.next_node is not None:
                prev = prev.next_node  # look at the next one
            if prev.next_node is not None:  # if the node you are looking at when you broke out of the loop has a next
                prev.next_node = node.next_node  # update pointer on prev to point at thing node was pointing at

# TODO check these work properly (not tested yet)


if __name__ == "__main__":
    # test code goes here!
    pass
