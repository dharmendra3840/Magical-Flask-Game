#----------------------------------------------------
# bstack.py
# (Top of stack corresponds to back of list)
# CMPUT 175
# AMRITPAL SINGH
# STUDENT ID : 1815622
# REFERENCES: e-Class STACK LECTURE NOTES 
#----------------------------------------------------

class BoundedStack:
    # Creates a new empty stack:
    def __init__(self, capacity):
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity)))
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.__items = []
        self.__capacity = capacity

    # Adds a new item to the top of the stack, and returns nothing:
    def push(self, item):
        if len(self.__items) >= self.__capacity:
            raise Exception('Error: Stack is full')
        self.__items.append(item)

    # Removes and returns the top item of the stack.
    # Returns nothing if the stack is empty.
    def pop(self):
        if len(self.__items) == 0:
            raise Exception('Error: Stack is empty')
        return self.__items.pop()

    # Returns the top item of the stack, without removing it.
    def peek(self):
        if len(self.__items) == 0:
            raise Exception('Error: Stack is empty')
        return self.__items[-1]

    # Returns True if the stack is empty, and False otherwise:
    def isEmpty(self):
        return len(self.__items) == 0

    # Returns True if the stack is full, and False otherwise:
    def isFull(self):
        return len(self.__items) == self.__capacity

    # Returns the number of items in the stack:
    def size(self):
        return len(self.__items)

    # Returns the capacity of the stack:
    def capacity(self):
        return self.__capacity

    # Removes all items from the stack, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.__items = []

    # Returns a string representation of the stack:
    def __str__(self):
        str_exp = ""
        for item in (self.__items):  # Top of the stack should be last in the list
            str_exp += (str(item) + " ")
        return str_exp.strip()

    
        
