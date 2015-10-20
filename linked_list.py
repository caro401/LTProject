class _Node:
    def __init__(self, key, data=None, next_node=None):
        self.key = key
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self, head=None, tail=None):
        self._head = head
        self._tail = tail
        self._size = 0

    def __iter__(self):
        current = self._head
        while current:
            yield current.key
            current = current.next_node

    def __str__(self):
        return " ".join([str(item) for item in self])

    @property
    def head(self):
        return self._head

    def list_insert_head(self, key):  # TODO error handling
        """
        Insert key at the head of the list.
        :param key: key of item to be inserted
        :return:
        """
        new_node = _Node(key)
        new_node.next_node = self._head  # make item point to the current head of the list

        self._head = new_node  # make item be the new head of the list
        if self._size == 0:
            self._tail = self._head
        self._size += 1

    def list_insert_tail(self, key):  # TODO error handling
        """
        Insert an item at the tail of the list
        :param key: key to be inserted
        :return:
        """
        n = self._tail
        self._tail = _Node(key)
        if self._size == 0:  # if this is the only item
            self._head = self._tail  # make it be the first item too
        else:
            n.next_node= self._tail  # update the pointer on the thing that used to be at the end
        self._size += 1

    def list_insert_middle(self, prev, key):  # TODO error handling
        """
        Insert a new node, with key *key*, after the node *prev* in the list
        :param prev:  the _Node object to be inserted after
        :param key:  the key of the new node to be inserted
        :return:
        """
        new_node = _Node(key)  # make a node from key
        new_node.next_node = prev.next_node  # make that node point at what the previous node is currently pointing at
        prev.next_node = new_node  # make the previous node point at the new node
        self._size += 1  # increase size by 1

    def list_search_trivial(self, key):  # TODO error handling
        """
        Traverse the linked list until you find a node with the specified key
        :param key: The key you are looking for
        :return: The _Node object with the key you are looking for, or None if it is not in the list
        """
        x = self._head  # start at the head of the list
        while x is not None and x.key != key:  # while there is still a node to look at, and you don't match the key
            x = x.next_node  # look at the next node in the list
        return x  # this executes when you have run out of list, or matched the key

    def list_delete(self, node):  # TODO error handling
        """
        Delete the specified node from the list, by changing the pointer on the node before to point at the next node.
        :param node: the _Node item you want to delete
        :return:
        """
        prev = self._head  # start at the head of the list
        if prev is not None:  # if there are some items in the list
            # while you haven't matched the node, and there are more nodes to look at
            while prev.next_node != node and prev.next_node is not None:
                prev = prev.next_node  # look at the next one
            if prev.next_node is not None:  # if the node you are looking at when you broke out of the loop has a next
                prev.next_node = node.next_node  # update pointer on prev to point at thing node was pointing at
        return node

    def swap_adjacent(self, prev=None):
        """
        Swap the two nodes immediately following the node specified. If prev is None, swap the first two nodes (since
        the head of a list has no previous node)
        :param prev: the node before the pair you want to switch
        :return:
        """
        # TODO error handling (eg when a, b are out of list)
        if prev is None:  # swap first and second items
            a = self.head
            b = self.head.next_node
            a.next_node = b.next_node
            self._head = b
            b.next_node = a
        else:
            a = prev.next_node
            b = prev.next_node.next_node
            a.next_node = b.next_node
            prev.next_node = b
            b.next_node = a
        if a.next_node is None:
            self._tail = a

    def swap(self, before_a, before_b):
        """
        Swap the nodes after the two nodes specified as arguments, by updating the pointers to them
        :param before_a: node before the first node you want to swap
        :param before_b: node before the second node you want to swap
        :return: self
        """
        # TODO error handling as above - check a and b exist
        if before_a is None:
            a = self.head
        else:
            a = before_a.next_node
        if a == before_b:  # ie the nodes are adjacent
            self.swap_adjacent(before_a)
            return self

        if before_b is None:
            b = self.head
        else:
            b = before_b.next_node
        before_a.next_node = b
        before_b.next_node = a
        a.next_node, b.next_node = b.next_node, a.next_node
        return self


    def insertionSort(self):
        main = self.head.next_node  # this is the value from the main for loop on a list (start at second item)
        while main is not None:  # while there are still unchecked items in the list
            compare = self.head  # this is the thing from the inner loop on an array, start at the start of the list

            # this while loop will run from the start of the list until you either run out of nodes, or find one bigger than main
            while compare.next_node is not None and compare.next_node.key < main.key:  # there is a node next, and it is still smaller
                compare = compare.next_node  # look at the next one
            if compare.key > main.key:  # this catches the case where main is the smallest element in the list so far and
                                        # needs to be inserted at head of list. This is nasty, could do with being tidied
                move_node = self.list_delete(main)  # cut out main node
                self.list_insert_head(move_node.key)  # insert it at the head
            else:  # all other cases
                move_node = self.list_delete(main)  # cut out the main node
                self.list_insert_middle(compare, move_node.key)  # insert it after the last node you found that was smaller
                                                               # main and not None
            # print(self)
            main = main.next_node  # look at the next node. This works because although you have cut the pointer to main
            # by using list_delete, you made a new node with its key only, and the original main node, and its next_node
            # pointer still exist


# TODO error handling generally


if __name__ == "__main__":
    # test code goes here!
    ll = LinkedList()
    for i in [5, 2, 9, 8, 1, 3, 6, 7, 14]:
        ll.list_insert_tail(i)
    print(ll)
    befa = ll.head.next_node.next_node
    befb = ll.head.next_node.next_node.next_node.next_node
    print(befa.key, befb.key)
    ll.swap_adjacent(befa)
    print(ll)
    ll.swap(befa, befb)
    print(ll)
    ll.insertionSort()
    print(ll)
