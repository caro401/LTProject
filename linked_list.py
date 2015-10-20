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

    def list_search(self, key):  # TODO error handling
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


    def __iter__(self):
        current = self._head
        while current:
            yield current.key
            current = current.next_node

    def __str__(self):
        return " ".join([str(item) for item in self])

    # only some items in the linked list are sorted.
    def insertion_Sort(self):
        h = self.head  # h is the first (the leftmost) item in the linked list
        sortedList= h  # [position] this is the first node of the sorted list
        h = h.next_node  # start using the second item in the list as the node to introduce
        sortedList.next_node = None  # so it is a list of one thing
        print(sortedList.key, "Hello")
        while h is not None:
            currentvalue = h
            h = h.next_node
            if currentvalue.key < sortedList.key:
                currentvalue.next_node = sortedList  # make currentvalue point at sortedList
                sortedList = currentvalue  # why?
                sortedList.next_node = h  # make sortedList point at the item which currentvalue was pointing

            else:  # if currentvalue.key > sortedListed.key
                search = sortedList
                while search.next_node is not None and currentvalue.key > search.next_node.key:
                    search = search.next_node
                currentvalue.next_node = search.next_node
                search.next_node = currentvalue
        return sortedList

    def insertionSort(self):
        h = self.head  # the leftmost item in the list
        position = h  # the "previous item"  (the one you are doing the main for loop over?)
        h = h.next_node  # the current key
        while h is not None:
            currentkey = h  # the key you are currently checking against
            print(currentkey.key)
            h = h.next_node  # move on to the next item
            if currentkey.key < position.key:  # find the place to insert currentkey
                print("Found one bigger!", position.key)
                he = self.head
                while he is not None:
                    prev = he
                    if prev.next_node.key > currentkey.key:
                        self.list_insert_middle(prev, currentkey) # this returns an error, but self.list_insert...is not working
                    he = he.next_node
            else:  # currentkey is larger than position key
                position.next_node = currentkey
        # return self  # what should I return?  nothing... you are just updating the properties of your linked list

    def insertsort(self):
        main = self.head.next_node  # this is the value from the main for loop on a list (start at second item)
        while main is not None:  # while there are still unchecked items in the list
            print("main is", main.key)
            compare = self.head  # this is the thing from the inner loop on an array, start at the start of the list
            print("comparing with", compare.key)

            # this while loop will run from the start of the list until you either run out of nodes, or find one bigger than main
            while compare.next_node is not None and compare.next_node.key < main.key:  # there is a node next, and it is still smaller
                print("incrementing compare")
                compare = compare.next_node  # look at the next one
            print("loop done, compare is", compare.key)
            if compare.key > main.key:  # this catches the case where main is the smallest element in the list so far and
                                        # needs to be inserted at head of list. This is nasty, could do with being tidied
                move_node = self.list_delete(main)  # cut out main node
                print("moving (if)", move_node.key)
                self.list_insert_head(move_node.key)  # insert it at the head
            else:  # all other cases
                move_node = self.list_delete(main)  # cut out the main node
                print("moving", move_node.key)
                self.list_insert_middle(compare, move_node.key)  # insert it after the last node you found that was smaller
                                                               # main and not None
            print(self)
            main = main.next_node  # look at the next node. This works because although you have cut the pointer to main
            # by using list_delete, you made a new node with its key only, and the original main node, and its next_node
            # pointer still exist





# TODO error handling generally


if __name__ == "__main__":
    # test code goes here!
    ll = LinkedList()
    for i in [5, 2, 9,8,1,3,6,7, 14]:
        ll.list_insert_tail(i)
    print(ll)
    ll.insertsort()
    print(ll, "hello")
