from shared.concurrent_queue import ConcurrentQueue

class ReceiveMessageHandler:

    def __init__(self, socket):
        self.socket = socket
        self.queue = ConcurrentQueue()

    #receive and enqueue message to the queue, later to be dequeue
    def push_message(self):
        pass

    #dequeue message from the queue, later to be send to related user
    def pull_message(self):
        pass

    #check to see whether there is any message in the queue
    def peek_message(self):
        pass