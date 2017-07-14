import socket
from .messenger import Messenger
from .message_handler import MessageHandler

# from enum import Enum
# from datetime import datetime.time

class Client:

    def __init__(self):
        self.socket = socket.socket()
        self.messenger = Messenger(self.socket)
        self.message_handler = MessageHandler(self.socket)

        #TODO: Initialize threads.

        #TODO: start main loop thread
        #TODO: start io loop thread

    def main_loop(self):

        x = 1
        while True:
            print("Main: To infinity and beyond! " + str(x))
            x += 1
            
    def io_loop(self):
        
        x = 1
        while True:
            print("IO: To infinity and beyond! " + str(x))
            x += 1
