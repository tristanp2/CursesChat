from queue import Queue

class MessageSender:

    def __init__(self, socket):
        self.socket = socket

    def send_message(self, message):
        send_str = ' '.join(m.get_send_list())
        self.socket.send(send_str.encode())