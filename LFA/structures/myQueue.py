class MyQueue:

    def __init__(self):
        self.__queue = []

    def enqueue(self, data):
        return self.__queue.insert(0, data)

    def dequeue(self):
        if len(self.__queue) > 0:
            return self.__queue.pop()

    def size(self):
        return len(self.__queue)

    def printQueue(self):
        return self.__queue

    def peek(self):
        return self.__queue[0] if len(self.__queue) > 0 else None

    def __str__(self):
        return str(self.__queue)[1:-1]

    def toList(self):
        list = []
        for x in self.__queue:
            list.append(x)
        return list
