# Linked list and its methods, used in ngrams_list


class _Node:
    def __init__(self, key, data=None, freq=None, next_node=None):
        self.key = key
        self.freq = freq
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
            yield current.key, current.freq
            current = current.next_node

    def __str__(self):
        return " ".join([str(item) for item in self])

    @property
    def head(self):
        return self._head

    @property
    def size(self):
        return self._size

    @property
    def tail(self):
        return self._tail

    def list_insert_head(self, new_node):
        """
        Insert a new node (from an existing node or a key) at the head of the list.
        :param new_node: thing  to be inserted
        """
        if type(new_node) is not _Node:  # if the thing isn't already a node, make it a node
            new_node = _Node(new_node)
        new_node.next_node = self._head  # make item point to the current head of the list

        self._head = new_node  # make item be the new head of the list
        if self._size == 0:
            self._tail = self._head
        self._size += 1

    def list_insert_tail(self, new_node):  # add item (key or node) at tail of list, used in mergesort
        """
        Insert a new node at the tail of the list
        :param new_node:  thing to be inserted
        """
        n = self._tail
        if type(new_node) is not _Node:  # if the thing isn't already a node, make it a node
            self._tail = _Node(new_node)
        else:  # make it the tail
            self._tail = new_node
        if self._size != 0:
            n.next_node = self.tail  # if this is not the only item
        else:
            self._head = self._tail  # if this is the only item, make it be the first item too
        self._size += 1

    def list_insert_middle(self, prev, new_node):
        """
        Insert a new node, with key *key*, after the node *prev* in the list
        :param prev:  the _Node object to be inserted after
        :param new_node:  the key of the new node to be inserted
        """
        if type(new_node) is not _Node:
            new_node = _Node(new_node)  # make a node from key (if it is a key)
        new_node.next_node = prev.next_node  # make that node point at what the previous node is currently pointing at
        prev.next_node = new_node  # make the previous node point at the new node
        self._size += 1  # increase size by 1

    def list_delete(self, node):
        """
        Delete the specified node from the list, by changing the pointer on the node before to point at the next node.
        :param node: the _Node item you want to delete
        :return: the node you just removed
        """
        if node == self.head:
            self._head = node.next_node
        else:
            prev = self._head  # start at the head of the list
            if prev is not None:  # if there are some items in the list
                # while you haven't matched the node, and there are more nodes to look at
                while prev.next_node != node and prev.next_node is not None:
                    prev = prev.next_node  # look at the next one
                if prev.next_node is not None:  # if the node you are looking at when you broke out of the loop has a next
                    prev.next_node = node.next_node  # update pointer on prev to point at thing node was pointing at
        self._size -= 1
        # update tail
        start = self.head
        while start.next_node is not None:
            start = start.next_node
        self._tail = start
        return node

    def find_mid(self):
        """
        Used in mergesort, returns the middle node of a linked list
        :return: the middle node
        """
        x = self.head
        y = self.head
        while y is not None and y.next_node is not None:
            x = x.next_node  # x will be at the middle of the list when y reaches the end
            y = y.next_node.next_node
        return x

    def pop(self):
        """
        Remove the item at the head of list, used in mergesort
        :return: the node you just removed. If the list is empty, return None.
        """
        if self._head:
            n = self._head
            self._head = self._head.next_node
            self._size -= 1
            return n
        else:
            return None

    def swap_adjacent(self, prev=None):
        """
        Swap the two nodes immediately following the node specified. If prev is None, swap the first two nodes (since
        the head of a list has no previous node)    (so if you specify 7 in 789, you will get 798 with this method)
        :param prev: the node before the pair you want to switch
        """
        if prev is None:  # swap first and second items
            a = self.head
            b = self.head.next_node
            a.next_node = b.next_node
            self._head = b
            b.next_node = a
        else:  # normal cases
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
        (If you specify 1 and 4 in 12345, you will get 15342)
        (If two nodes are adjacent, it will swap the two nodes after the first specified node. so 34 in 12345 will be 12354)
        :param before_a: node before the first node you want to swap
        :param before_b: node before the second node you want to swap
        :return: self
        """
        if before_a is None:
            a = self.head
        else:
            a = before_a.next_node
        if a == before_b:  # ie the nodes are adjacent
            self.swap_adjacent(before_a)
            return self
        if before_a and before_a.next_node:
            a = self.list_delete(before_a.next_node)
        else:
            a = self.list_delete(self.head)

        b = self.list_delete(before_b.next_node)
        if before_a:
            self.list_insert_middle(before_a, b)
        else:
            self.list_insert_head(b)
        self.list_insert_middle(before_b, a)
        # update tail
        start = self.head
        while start.next_node is not None:
            start = start.next_node
        self._tail = start
        return self

    def insertionsort(self):
        """
        Used in ngrams_list to find the most common words
        """
        main = self.head.next_node  # the value from the main for loop on a list (start at second item)
        while main is not None:  # while there are still unchecked items in the list
            compare = self.head  # the thing from the inner loop on an array, start at the start of the list

            # this while loop will run from the start of the list until you either run out of nodes
            # or find one bigger than main
            while compare.next_node is not None and compare.next_node.key < main.key: # there is a node next, and it's still smaller
                compare = compare.next_node  # look at the next one
            if compare.key > main.key:  # this catches the case where main is the smallest element in the list so far
                                        # and needs to be inserted at head of list.
                move_node = self.list_delete(main)  # cut out main node
                self.list_insert_head(move_node)  # insert it at the head
                main = main.next_node
            else:  # all other cases (compare.key < main.key)
                temp = main
                main = main.next_node
                move_node = self.list_delete(temp)  # cut out the main node
                self.list_insert_middle(compare, move_node)  # insert it after the last node you found that was smaller
                                                             # main and not None

        # update the value of self.tail to be the biggest item!
        start = self.head
        while start.next_node is not None:
            start = start.next_node
        self._tail = start

    def binary_search(self, key):
        """
        Find the key using binary search. The list is first quicksorted before searching.
        :param key: the key to be found
        :return: node, if not found return None
        """
        self.quicksort()
        max_i = self._size - 1  # max_i & min_i mark the "boundaries" of the search. Now max_i is basically len(list)-1
        min_i = 0
        mid_i = (min_i + max_i) // 2
        splitpoint = self.head
        for i in range(min_i, mid_i):  # loop over and find the first middle point (splitpoint)
            splitpoint = splitpoint.next_node  # will loop over and stop at mid_i

        while min_i < max_i and splitpoint.key != key and splitpoint.next_node and splitpoint:
            if splitpoint.key < key:  # key is to the left of splitpoint (reachable with .next_node method)
                min_i = mid_i + 1  # move the left boundary to mid_i (focus on the right part)
                mid_i = (min_i + max_i) // 2
                if min_i == max_i:  # when min_i == max_i for i in range won't work, have to change point manually
                    # (although we have min_i< max_i in the while loop this is still possible as the loop will not break
                    # immediately when min_i == max_i)
                    splitpoint = splitpoint.next_node  # if key is in list it will be this node
                    if splitpoint.key == key:  # see if this is the key
                        return splitpoint
                    else:  # if splitpoint != key at this point, key is not in the list
                        return None

                else:  # normal cases, when min_i < max_i
                    for i in range(min_i, mid_i+1):  # will loop over and stop at the new mid_i
                        splitpoint = splitpoint.next_node
                continue  # go back to the start of while loop and see if the new splitpoint is at a reachable position to the key
            # this will break when 1.) when the key is found  2.) when min_i == max_i 3.) splitpoint.next_node is None

            else:  # key is to the right of the splitpoint (unreachable), splitpoint must be reset
                max_i = mid_i  # move the right boundary to mid_i (focus on the left part)
                mid_i = (min_i + max_i) // 2  # get a new mid_i
                splitpoint = self.head  # search for a new splitpoint from the head
                for i in range(0, mid_i):
                    splitpoint = splitpoint.next_node  # will loop over and stop at mid_i
                continue  # go back to the while loop and see if splitpoint < key

        if min_i != max_i:  # if the while loop breaks because splitpoint happens to be the key, it goes here
            return splitpoint
        else:   # if key is smaller than all items in the list, it will loop over the "else" part above and
            return None  # break when min_i == max_i and goes here (no key is found, so None is returned)

    def mergesort(self):  # this sorts on the length of the data attribute
        """
        This is a method that makes the list mergesort itself.
        :return: the sorted list
        """
        return self.mergesort_recurse(self)

    def mergesort_recurse(self, lst):  # this is the main recursive bit of mergesort
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

            left = self.mergesort_recurse(leftlist)
            right = self.mergesort_recurse(rightlist)
            lst = self.merge(left, right)
            self._head = lst.head  # update the head
            self._tail = lst.tail
            return lst

    @staticmethod
    def merge(l, r):
        # this does the merging bit of mergesort
        merged = LinkedList()
        while l.head is not None or r.head is not None:  # there are items remaining in the left sublist
            if l.head is None:  # left sublist is empty
                merged.list_insert_tail(r.pop())  # remove the node at the head of r and push it to the new ll
            elif r.head is None:   # right sublist is empty
                merged.list_insert_tail(l.pop())  # remove the node at the head of l and push to new ll
            else:  # both sublists still have stuff in
                if len(l.head.data) <= len(r.head.data):
                    # remove the node at the head of l and push to new ll
                    merged.list_insert_tail(l.pop())
                else:  # r.head < l.head
                    merged.list_insert_tail(r.pop())  # remove the node at the head of l and push to new ll
        return merged

    def quicksort(self):
        """
        Used in binary search. Sorted in reversed order (ie large to small) and on frequency.
        :return: the sorted list
        """
        return self.quicksort_recurse(self, self.head, self._tail)

    def quicksort_recurse(self, lst, start, end):  # the main recursive part of quicksort
        if start and start.key != end.key:
            pivot = self.partition(lst, start, end)
            self.quicksort_recurse(lst, start, pivot)
            self.quicksort_recurse(lst, pivot.next_node, end)

    @staticmethod
    def partition(lst, start, end):  # the partition part of quicksort
        pivot = start
        i = pivot
        iprev = i
        jprev = pivot  # track the node before j, used for swapping
        j = pivot.next_node
        while j != end.next_node and j is not None and pivot is not None:  # (assuming unique keys)
            if j.key < pivot.key:
                # swap i and j
                if i.next_node.key != j.key:
                    lst.swap(i, jprev)
                iprev = i
                i = i.next_node
            jprev = j
            j = j.next_node
        # swap pivot and j after having all the larger items to the left
        pivot.key, i.key = i.key, pivot.key
        pivot.freq, i.freq = i.freq, pivot.freq
        pivot.data, i.data = i.data, pivot.data
        return i


if __name__ == "__main__":
    # test code goes here!
    ll = LinkedList()
    for i in [5, 2, 9, 8, 1, 3, 6, 7, 14, 45, 15]:
        new_node = _Node(i, freq=i)
        ll.list_insert_tail(new_node)
    print(ll)
    print(ll.binary_search(7).key)
