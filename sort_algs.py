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


def mergesort(lst):  # something weird is happening with the list getting modified... # TODO fix this!
    if lst.head is None or lst.head.next_node is None:  # list of 0 or 1 things - trivially sorted
        return lst
    else:
        leftlist = linked_list.LinkedList(lst.head)  # the left half of the list starts here
        # find the middle node
        mid = find_mid(lst)
        if mid.next_node is not None:
            rightlist = linked_list.LinkedList(mid.next_node)
            mid.next_node = None  # divide the two parts
        else:
            rightlist = linked_list.LinkedList(mid)
            leftlist.head.next_node = None

        print("right half starts at", rightlist.head.key)

        print("call mergesort", leftlist.head.key)
        print("ll is now", ll)
        left = mergesort(leftlist)
        print("call mergesort", rightlist.head.key)
        print("ll is now", ll)
        right = mergesort(rightlist)
        print("merging! L {} and R {}".format(left, right))
        lst = merge(left, right)
        print("MERGED", lst)
        return lst

def merge(l, r):
    merged = linked_list.LinkedList()
    print("left head {}, right head {}".format(l.head.key, r.head.key))
    while l.head is not None or r.head is not None:  # there are items remaining in the left sublist
        if l.head is None:  # left sublist is empty
            print("if!")
            push(merged, pop(r))  # remove the node at the head of r and push it to the new ll
        elif r.head is None:   # right sublist is empty
            print("elif")
            push(merged, pop(l))  # remove the node at the head of l and push to new ll
        else:  # both sublists still have stuff in
            if l.head.key <= r.head.key:
                print("l is smaller than r")
                push(merged, pop(l))  # remove the node at the head of l and push to new ll
            else:  # r.head < l.head
                print("r is smaller?")
                push(merged, pop(r))  # remove the node at the head of l and push to new ll
    print(merged)
    return merged

def find_mid(lst):
    x = lst.head
    y = lst.head
    while y is not None and y.next_node is not None:
        x = x.next_node
        y = y.next_node.next_node
    return x

def push(ll, node):  # add item at tail of list
    n = ll._tail
    ll._tail = node
    if ll._size == 0:  # if this is the only item
        ll._head = ll._tail  # make it be the first item too
    else:
        n.next_node= ll._tail  # update the pointer on the thing that used to be at the end
    ll._size += 1


def pop(ll):  # delete item at head of list, return it
    # TODO error handling (empty list)
    n = ll._head
    ll._head = ll._head.next_node
    ll._size -= 1
    return n


def peek(ll):  # return node at head of list
    # TODO error handling (empty)
    return ll._head.key



if __name__ == "__main__":
    # test code goes here!
    ll = linked_list.LinkedList()
    for i in [5, 2, 9,8,15, 45, 4, 1,3,6,7, 14]:
        ll.list_insert_tail(i)
    print(ll)

    quicksort(ll.head, ll._tail)
    print(ll)