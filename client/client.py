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
from messenger import Messenger
from message_handler import MessageHandler
from time import sleep

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.messenger = Messenger(self.socket)
        self.message_handler = MessageHandler(self.socket)
        
        self.receive_queue = ConcurrentQueue()
        self.ui = UI()
        #TODO: Initialize threads.

        #TODO: start io loop thread

    def main_loop(self):
        self.alias = self.ui.do_login()
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
    def io_loop(self):
        x = 1
        while True:
            x += 1

if __name__ == '__main__':
    cl = Client()
    cl.main_loop()