from queue import Queue

class MessageReceiver:

    def __init__(self, socket):
        self.socket = socket
        self.queue = Queue()

    def pop_message(self):
        self.queue.get()

    def receive_message(self):
        data = self.socket.recv(1024)
        self.queue.put(data.decode())
