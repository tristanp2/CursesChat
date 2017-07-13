import pytest
from ..shared import concurrent_queue

#https://docs.pytest.org/en/latest/example/index.html

class TestConcurrentQueue():
    def test_is_empty(self):
        queue = ConcurrentQueue()
        assert queue.isEmpty() is True
        queue.push("Hello")
        assert queue.isEmpty() is False
        queue.pop()
        assert queue.isEmpty() is True

    def test_size(self):
        queue = ConcurrentQueue()
        assert queue.size() is 0
        queue.push("Hello")
        assert queue.size() is 1
        queue.pop()
        assert queue.size() is 0
