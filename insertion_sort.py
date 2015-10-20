
class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

class unorderedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def length(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext()

    def insertionSort(h):
        if h == None:
            return None
        #Make the first node the start of the sorted list.
        sortedList= h
        h=h.next
        sortedList.next= None
        while h != None:
            curr= h
            h=h.next
            if curr.data<sortedList.data:
                #Advance the nodes
                curr.next= sortedList
                sortedList= curr
            else:
                #Search list for correct position of current.
                search= sortedList
                while search.next!= None and curr.data > search.next.data:
                    search= search.next
                #current goes after search.
                curr.next= search.next
                search.next= curr
        return sortedList

    def printList(d):
        s=''
        while d:
            s+=str(d.data)+"->"
            d=d.next
        print s[:-2]

l= unorderedList()
l.add(10)
l.add(12)
l.add(1)
l.add(4)
h= l.head
printList(h)

result= insertionSort(l.head)
d= result
printList(d)

# from http://stackoverflow.com/questions/26705235/how-do-i-implement-selectionsort-and-insertionsort-on-a-linked-list-in-python