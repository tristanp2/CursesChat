import socket
from .messenger import Messenger
from .message_handler import MessageHandler

# from enum import Enum
# from datetime import datetime.time

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #asumming the server is localhost and port is 10000
        self.server_adrs = ('134.87.133.12', 10000)
        self.messenger = Messenger(self.socket)
        self.message_handler = MessageHandler(self.socket)

        #TODO: Initialize threads.

        #TODO: Inform user login method
        print('Login in by typing /login [username]')
        print(socket.gethostbyname(socket.gethostname()))

        #TODO: start main loop thread
        self.main_loop()
        #TODO: start io loop thread
        #self.io_loop()

    def main_loop(self):

        #connect socket directly to server
        self.socket.connect(self.server_adrs)

        x = 1
        while True:
            print("Main: To infinity and beyond! " + str(x))
            x += 1
            teststring = b'client: Hello server!'
            for i in range(5):
                self.socket.sendall(teststring)
                stringdata = self.socket.recv(1024)
                print('received {!r}'.format(stringdata))
            self.socket.close()
            break

            
    def io_loop(self):
        
        x = 1
        while True:
            print("IO: To infinity and beyond! " + str(x))
            x += 1
