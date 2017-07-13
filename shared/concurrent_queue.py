import threading


class ConcurrentQueue:

    def __init__(self):
        self.lock = Lock()
        self.items = []

    def isEmpty(self):
        lock.acquire()
        result = self.items = []
        lock.release()
        return result

    def size(self):
        lock.acquire()
        result = len(self.items)
        lock.release()
        return result

    def push(self, item):
        lock.acquire()
        self.items.insert(len(self.items), item)
        lock.release()

    def pop(self, item):
        lock.acquire()
        if self.items == []:
            result = False
        else:
            result = self.items.pop()
        lock.release()
        return result
