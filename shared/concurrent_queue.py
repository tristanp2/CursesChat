import threading


class ConcurrentQueue:

    def __init__(self):
        self.lock = threading.Lock()
        self.items = []

    def isEmpty(self):
        self.lock.acquire()
        result = len(self.items) == 0
        self.lock.release()
        return result

    def size(self):
        self.lock.acquire()
        result = len(self.items)
        self.lock.release()
        return result

    def push(self, item):
        self.lock.acquire()
        self.items.insert(len(self.items), item)
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        if self.items == []:
            result = False
        else:
            result = self.items.pop()
        self.lock.release()
        return result


class TestConcurrentQueue():

    def is_empty(self):
        queue = ConcurrentQueue()
        assert queue.isEmpty() is True

        for x in range(0, 20):
            queue.push("Hello" + str(x))
            assert queue.isEmpty() is False

        for x in range(0, 19):
            queue.pop()
            assert queue.isEmpty() is False

        queue.pop()
        assert queue.isEmpty() is True

    def size(self):
        queue = ConcurrentQueue()
        assert queue.size() is 0

        for x in range(0, 20):
            queue.push("Hello" + str(x))
            assert queue.size() is x + 1

        for x in range(0, 19):
            queue.pop()
            assert queue.size() is 20 - 1 - x

        queue.pop()
        assert queue.size() is 0

if __name__ == '__main__':
    test = TestConcurrentQueue()
    test.is_empty()
    test.size()
