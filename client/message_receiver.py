from shared.concurrent_queue import ConcurrentQueue

class MessageReceiver:

    def __init__(self, socket):
        self.socket = socket
        self.queue = ConcurrentQueue()
    def pop_message(self):
        if not self.queue.isEmpty():
            return self.queue.pop()
    def receive_message(self):
        data = self.socket.recv(1024)
        self.queue.push(data.decode())
