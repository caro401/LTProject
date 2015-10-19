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

    def __iter__(self):
        current = self._head
        while current:
            yield current.key
            current = current.next_node

    def __str__(self):
        return " ".join([str(item) for item in self])

    def binary_search(arr, k):
        insertionSort(arr)
        # k is the item that we are looking for
        # max_i and min_i are the boundaries (the indexes of the max and min value)
        max_i = len(arr) - 1
        min_i = 0
        while min_i <= max_i:  # while there are sth to search for between the boundaries
            mid_i = (min_i + max_i)//2
            if arr[mid_i] == k:  # if arr[mid_i] is k
                return mid_i
            elif k > arr[mid_i]:  # if arr[mid_i] is smaller than k
                min_i = mid_i + 1
            else:  # now we know that the mid_i item is bigger than k
                max_i = mid_i - 1
        return "key not found"  # when key is not in the list

    def insertionSort(alist):
        for index in range(1, len(alist)):
            currentvalue = alist[index]
            position = index-1
            while position >= 0 and alist[position]>currentvalue:
                alist[position + 1] = alist[position]
                position -= 1
            alist[position + 1] = currentvalue
            return alist

# TODO error handling generally


if __name__ == "__main__":
    # test code goes here!
    ll = LinkedList()
    ll.list_insert_head("fred")
    print(ll)
    ll.list_insert_head("bob")
    ll.list_insert_head("frank")
    print(ll)
    ll.list_insert_tail("charles")
    print(ll)
    ll.list_insert_middle(ll.head.next_node, "dave")
    ll.list_insert_middle(ll.head.next_node, "greg")
    print(ll)
    ll.binary_search(20)
    print(ll)
