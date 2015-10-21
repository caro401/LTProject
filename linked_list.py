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

    def list_insert_head(self, new_node):  # TODO error handling
        """
        Insert a new node (from an existing node or a key) at the head of the list.
        :param new_node: thing  to be inserted
        :return:
        """
        if type(new_node) is not _Node:  # if the thing isnt already a node, make it a node
            new_node = _Node(new_node)
        new_node.next_node = self._head  # make item point to the current head of the list

        self._head = new_node  # make item be the new head of the list
        if self._size == 0:
            self._tail = self._head
        self._size += 1

    def list_insert_tail(self, new_node):  # add item (key or node) at tail of list, used in mergesort
        n = self._tail
        if type(new_node) is not _Node:
            self._tail = _Node(new_node)
        else:
            self._tail = new_node
        if self._size == 0:  # if this is the only item
            self._head = self._tail  # make it be the first item too
        else:
            n.next_node = self._tail  # update the pointer on the thing that used to be at the end
        self._size += 1

    def list_insert_middle(self, prev, new_node):  # TODO error handling
        """
        Insert a new node, with key *key*, after the node *prev* in the list
        :param prev:  the _Node object to be inserted after
        :param key:  the key of the new node to be inserted
        :return:
        """
        if type(new_node) is not _Node:
            new_node = _Node(new_node)  # make a node from key
        new_node.next_node = prev.next_node  # make that node point at what the previous node is currently pointing at
        prev.next_node = new_node  # make the previous node point at the new node
        self._size += 1  # increase size by 1

    def list_delete(self, node):  # TODO error handling
        """
        Delete the specified node from the list, by changing the pointer on the node before to point at the next node.
        :param node: the _Node item you want to delete
        :return: the node you just removed
        """
        prev = self._head  # start at the head of the list
        if prev is not None:  # if there are some items in the list
            # while you haven't matched the node, and there are more nodes to look at
            while prev.next_node != node and prev.next_node is not None:
                prev = prev.next_node  # look at the next one
            if prev.next_node is not None:  # if the node you are looking at when you broke out of the loop has a next
                prev.next_node = node.next_node  # update pointer on prev to point at thing node was pointing at
        return node

    def find_mid(self):  # used in mergesort, returns the middle node of a linked list
        x = self.head
        y = self.head
        while y is not None and y.next_node is not None:
            x = x.next_node
            y = y.next_node.next_node
        return x

    def pop(self):  # remove item at head of list, return it. used in mergesort
        # TODO error handling (empty list)
        n = self._head
        self._head = self._head.next_node
        self._size -= 1
        return n

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

    def mergsesort(self):
        # This is a method to make the list mergesort itself
        return self.mergesort_recurse(self)

    def mergesort_recurse(self, lst):  # something weird is happening with the list getting modified... # TODO fix this!
        # this is the main recursive bit of mergesort
        if lst.head is None or lst.head.next_node is None:  # list of 0 or 1 things - trivially sorted
            return lst
        else:
            leftlist = LinkedList(lst.head)  # the left half of the list starts here
            # find the middle node
            mid = lst.find_mid()
            if mid.next_node is not None:
                rightlist = LinkedList(mid.next_node)
                mid.next_node = None  # divide the two parts
            else:
                rightlist = LinkedList(mid)
                leftlist.head.next_node = None

            print("right half starts at", rightlist.head.key)

            print("call mergesort", leftlist.head.key)
            print("ll is now", ll)
            left = self.mergesort_recurse(leftlist)
            print("call mergesort", rightlist.head.key)
            print("ll is now", ll)
            right = self.mergesort_recurse(rightlist)
            print("merging! L {} and R {}".format(left, right))
            lst = self.merge(left, right)
            print("MERGED", lst)
            return lst

    def merge(self, l, r):
        # this does the merging bit of mergesort
        merged = LinkedList()
        print("left head {}, right head {}".format(l.head.key, r.head.key))
        while l.head is not None or r.head is not None:  # there are items remaining in the left sublist
            if l.head is None:  # left sublist is empty
                print("if!")
                merged.list_insert_tail(r.pop())  # remove the node at the head of r and push it to the new ll
            elif r.head is None:   # right sublist is empty
                print("elif")
                merged.list_insert_tail(l.pop())  # remove the node at the head of l and push to new ll
            else:  # both sublists still have stuff in
                if l.head.key <= r.head.key:
                    print("l is smaller than r")
                    merged.list_insert_tail(l.pop())  # remove the node at the head of l and push to new ll
                else:  # r.head < l.head
                    print("r is smaller?")
                    merged.list_insert_tail(r.pop())  # remove the node at the head of l and push to new ll
        print(merged)
        return merged



# TODO error handling generally


if __name__ == "__main__":
    # test code goes here!
    ll = LinkedList()
    for i in [5, 2, 9,8,1,3,6,7, 14]:
        ll.list_insert_tail(i)
    print(ll)
    befa = ll.head.next_node.next_node
    befb = ll.head.next_node.next_node.next_node.next_node
    print(befa.key, befb.key)
    ll.swap_adjacent(befa)
    print(ll)
    ll.swap(befa, befb)
    print(ll)
    ll.mergsesort()
    print(ll)
    ll.insertionSort()
    print(ll)
