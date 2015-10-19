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
    pass


if __name__ == "__main__":
    # test code goes here!
    ll = linked_list.LinkedList()
    for i in [5, 2, 9,8,1,3,6,7, 14, 54, 4655, 23, 15]:
        ll.list_insert_tail(i)
    print(ll)

    quicksort(ll.head, ll._tail)
    print(ll)