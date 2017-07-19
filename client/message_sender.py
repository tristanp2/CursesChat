from shared.concurrent_queue import ConcurrentQueue

class MessageSender:

    def __init__(self, socket):
        self.socket = socket
        self.queue = ConcurrentQueue()

    def push_message(self, message):
        self.queue.push(message)

    def send_message(self):
        msg = self.queue.pop()
        if msg:
            send_str = ' '.join(msg.get_send_list())
            self.socket.send(send_str.encode())