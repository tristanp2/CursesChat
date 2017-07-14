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
            result = self.items.pop(0)
        self.lock.release()
        return result


class TestConcurrentQueue():

    def is_empty(self):
        queue = ConcurrentQueue()
        assert queue.isEmpty() is True

        # 0-19
        for x in range(20):
            queue.push(x)
            assert queue.isEmpty() is False

        # 0-18
        for x in range(19):
            item = queue.pop()
            assert item is x
            assert queue.isEmpty() is False

        item = queue.pop()
        assert item is 19
        assert queue.isEmpty() is True

    def size(self):
        queue = ConcurrentQueue()
        assert queue.size() is 0

        # 0-19
        for x in range(20):
            queue.push(x)
            assert queue.size() is x + 1

        # 0-19
        for x in range(20):
            item = queue.pop()
            assert item is x
            assert queue.size() is 20 - 1 - x


if __name__ == '__main__':
    test = TestConcurrentQueue()
    test.is_empty()
    test.size()
