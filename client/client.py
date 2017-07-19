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
        self.server_adrs = ('localhost', 10000)
        self.receiver = MessageReceiver(self.socket)
        self.sender = MessageSender(self.socket)
        self.received_queue = ConcurrentQueue()
        self.outgoing_queue = ConcurrentQueue()
        self.ui = UI()
        #TODO: Initialize threads.
        self.io_thread = Thread(None, self.__io_loop)

    def main_loop(self):
        self.alias = self.ui.start_login()
        sleep(2)
        self.socket.connect(self.server_adrs)
        self.ui.end_login()
        self.ui.start_chat()
        while True:
            while not self.receive_queue.isEmpty():
                msg = self.receive_queue.pop()
                self.ui.process_message(msg)
            outgoing = self.ui.get_outgoing()
            for m in outgoing:
                m.set_alias(self.alias)
                self.receive_queue.push(m)
            self.ui.update_chat()
            sleep(0.5)

    #send and recieve       
    def __io_loop(self):
        #At the moment, sender and receiver classes seem pretty redundant
        #May change this in near future
        while True:
            while not self.outgoing_queue.isEmpty():
                msg = self.outgoing_queue.pop()
                self.sender.push_message(msg)
            msg = self.receiver.pop_message()
            while msg != None:
                self.received_queue.push(msg)
                self.receiver.pop_message()

            self.receiver.receive_message()
            self.sender.send_message()


if __name__ == '__main__':
    cl = Client()
    cl.main_loop()