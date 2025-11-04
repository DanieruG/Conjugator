class Node: # Instead of implementing this concept all within one class, split it into two.
    def __init__(self, value) -> None:
        self.value = value # This is the value stored within the node
        self.next = None # This is the pointer, holding the index of the next item in the list.
        self.prev = None # Pointer to the previous element for DLL implementation.
        # By default, we would need to set this to None, as if it were the last element or only element, there wouldn't be anywhere else to point to.

class LinkedList():
    # The very concept of a linked list is to have a normal list, where each element is assigned a pointer to the next element.
    # What we want here are 4 methods; 1 to add to the beginning of the list; another to add to the end of the list;
    # A method to remove an element from the list, and finally one to add one to a specific index.
    
    def __init__(self) -> None:
        self.head = None # This is the first value within the list.
        self.current = None # Tracks current node
    
    def IsEmpty(self):
        if self.head is None: # If the list doesn't have a starting point, this assigns it with one
            return True
        else:
            return False
    
    def getHead(self):
        if not self.IsEmpty():
            self.current = self.head
            return self.current.value
        else:
            return None
    
    def getCurrent(self):
        return self.current.value

    def AddToStart(self, element): # To add an element to the beginning of the list
        new_node = Node(element)
        if self.IsEmpty():
            self.head = new_node
            return
        else:
            new_node.next = self.head # The new node's points to the original head element
            self.head.prev = new_node # Sets node to be moved right to have its previous node set to new node.
            self.head = new_node # The new node is now the head, pointing to the original head node.

    
    def AddToEnd(self, element): # To add an element to the end of the linked list.
        new_node = Node(element) 
        if self.IsEmpty():
            self.head = new_node
            return
        else:
            current_node = self.head
            while current_node.next is not None: # A loop to traverse all nodes until the pointer points to 'None'
                current_node = current_node.next
            current_node.next = new_node # Once the loop has found the node pointing to none, the new node is inserted in that location

            new_node.prev = current_node



     # This adds an element to the index adjacent to a specified index.
    def AddToIndex(self, element, index): # Assuming a zero-indexed linked list
        new_node = Node(element) 
        if self.IsEmpty():
            self.head = new_node
            return
        else:
            current_node = self.head
            count = 0
            while count != index and current_node != None: # Makes sure index is not skipped, and current_node isn't empty
                # index + 1 keeps it accurate to a 0 indexed list.
                current_node = current_node.next
                count += 1

            if current_node is not None: # This shoves the new node into its new position
                new_node.next = current_node.next # new node's pointer points to the current nodes' next pointer
                new_node.prev = current_node # Sets new node's previous pointer to the node its being moved in front of
                new_node.next.prev = new_node # Sets the former node's next node's previous pointer to new node.
                current_node.next = new_node # current node's next pointer finally updated to new node.
                
            else:
                print("No such index.")

    def printLL(self): # Convert into a method that will return the next element.
        current_node = self.head
        while current_node is not None:
            print(current_node.value)
            current_node = current_node.next

    def next(self):
        if self.current is None or self.current.next is None:
            return None
        # getHead() is always used to fetch the first node of the list.
        # Most of the time, it will be the second condition that is triggered to return None.
        # If self.current is ever None, then it will be an exceptional case.


        self.current = self.current.next # Very simple line.

        return self.current.value
        


    def prev(self):
        if self.current is None or self.current.prev is None:
            return None
        
        self.current = self.current.prev
        
        return self.current.value
    
    def size(self):
        current = self.head
        count = 1 # this is to account for the initial self.head
        if self.head is not None:
            while current.next != None:
                current = current.next
                count = count + 1
        else:
            return 0
        
        return count

    
    def reverseLL(self):
        current_node = self.head # Starts from beginning
        while current_node.next is not None: # Goes to last element
            current_node = current_node.next
        while current_node.prev is not None: # if this element's previous node isn't empty, then...
            print(current_node.value) # Prints the node
            current_node = current_node.prev # Sets its next to previous
        print(current_node.value) # Print outside of while loop to prevent 1st element from being skipped.                
