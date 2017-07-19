import os
import sys
path = os.path.abspath(__file__)
path = path.split('\\')
path = path[:-2]
path = '\\'.join(path)
sys.path.append(path)


import socket
from shared.concurrent_queue import ConcurrentQueue
from ui import UI
from threading import Thread
from message_receiver import MessageReceiver
from message_sender import MessageSender
from time import sleep

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #asumming the server is localhost and port is 10000
        self.server_adrs = ('134.87.133.12', 10000)
        self.receiver = MessageReceiver(self.socket)
        self.sender = MessageSender(self.socket)
        self.received_queue = ConcurrentQueue()
        self.outgoing_queue = ConcurrentQueue()
        self.ui = UI()

        self.send_thread = Thread(None, self.__send_loop, 'send_t')
        self.recv_thread = Thread(None, self.__recv_loop, 'recv_t')

    def main_loop(self):
        self.alias = self.ui.start_login()
        self.socket.connect(self.server_adrs)
        self.ui.end_login()
        self.send_thread.start()
        self.recv_thread.start()
        self.ui.start_chat()
        while True:
            while not self.received_queue.isEmpty():
                msg = self.received_queue.pop()
                self.ui.parse_and_push(msg)
            outgoing = self.ui.get_outgoing()
            for m in outgoing:
                m.set_alias(self.alias)
                self.outgoing_queue.push(m)
            self.ui.update_chat()
            sleep(0.2)
    
    def __send_loop(self):
        while True:
            while not self.outgoing_queue.isEmpty():
                msg = self.outgoing_queue.pop()
                self.sender.push_message(msg)
            sleep(0.5)
            self.sender.send_message()

    def __recv_loop(self):
        while True:
            msg = self.receiver.pop_message()
            while msg != None:
                self.received_queue.push(msg)
                msg = self.receiver.pop_message()
            self.receiver.receive_message()
            pass

if __name__ == '__main__':
    cl = Client()
    cl.main_loop()
