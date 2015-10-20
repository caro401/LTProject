import linked_list


def quicksort(start, end):
    if start and start.key != end.key:
        print("partitioning", start.key, end.key)
        pivot = partition(start, end)
        quicksort(start, pivot)
        quicksort(pivot.next_node, end)


def partition(start, end):
    pivot = start
    i = pivot
    j = pivot.next_node
    print("j is", j.key)
    while j != end.next_node:  # assuming unique keys
        if j.key < pivot.key:
            i = i.next_node
            # swap  i and j
            print("swapping {} and {}".format(i.key,j.key))
            i.key, j.key = j.key, i.key
            i.data, j.data = j.data, i.data
            print("after swapping", ll)
        j = j.next_node
        if j:
            print("j is now", j.key)
    # swap pivot and j
    pivot.key, i.key = i.key, pivot.key
    pivot.data, i.data = i.data, pivot.data
    print("pivot {}, i {}".format(pivot.key, i.key))
    print(ll)
    return i


def mergesort(lst):
    if lst.head is None or lst.head.next_node is None:  # list of 0 or 1 things - trivially sorted
        return lst
    else:
        leftlist = linked_list.LinkedList(lst.head)  # the left half of the list starts here
        # find the middle node
        mid = find_mid(lst)
        rightlist = linked_list.LinkedList(mid.next_node)
        mid.next_node = None  # divide the two parts
        print("right half starts at", rightlist.head.key)

        print("call mergesort", leftlist.head.key)
        left = mergesort(leftlist)
        print("call mergesort", rightlist.head.key)
        right = mergesort(rightlist)
        print("merging! L {} and R {}".format(left.key, right.key))
        merged = merge(left, right)
        return merged

def merge(l, r):
    merged = linked_list.LinkedList()
    while l.head is not None or r.head is not None:  # there are items remaining in the left sublist
        if l.head is None:  # left sublist is empty
            push(merged, r.pop())  # remove the node at the head of r and push it to the new ll
        elif r.head is None:   # right sublist is empty
            push(merged, l.pop())  # remove the node at the head of l and push to new ll
        else:  # both sublists still have stuff in
            if l.head <= r.head:
                push(merged, l.pop())  # remove the node at the head of l and push to new ll
            else:  # r.head < l.head
                push(merged, r.pop())  # remove the node at the head of l and push to new ll
    print(merged)
    return merged

def find_mid(lst):
    x = lst.head
    y = lst.head
    while y is not None and y.next_node is not None:
        x = x.next_node
        y = y.next_node.next_node
    return x

def push(ll, n):  # add item at head of list
    n.next.node = ll._head
    ll._head = n
    ll._size += 1


def pop(ll):  # delete item at head of list, return it
    # TODO error handling (empty list)
    n = ll.head
    ll.head = ll.head.next_node
    ll._size -= 1
    return n


def peek(ll):  # return node at head of list
    # TODO error handling (empty)
    return ll._head.key




if __name__ == "__main__":
    # test code goes here!
    ll = linked_list.LinkedList()
    for i in [5, 2, 9,8,1,3,6,7, 14]:
        ll.list_insert_tail(i)
    print(ll)

    mergesort(ll)
    print(ll)