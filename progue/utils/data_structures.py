""" Implement helpful data structures """


class Stack(object):
    """ No need to expose all of the operations of a list """

    def __init__(self):
        self.__storage = []

    def push(self, item):
        self.__storage.append(item)

    def pop(self):
        return self.__storage.pop()

    def peek(self):
        return self.__storage[-1]

    def empty(self):
        return 0 == len(self.__storage)

    def purge(self):
        self.__storage = []

    def size(self):
        return len(self.__storage)

    def dump_contents(self):
        print self.__storage
