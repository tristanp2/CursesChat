import socket
import queue
from ui import UI
from threading import Thread
from time import sleep

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #asumming the server is localhost and port is 10000
        self.server_adrs = ('134.87.170.182', 10000)
        self.received_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()
        self.ui = UI()

        self.send_thread = Thread(None, self.__send_loop, 'send_t')
        self.recv_thread = Thread(None, self.__recv_loop, 'recv_t')

    def main_loop(self):
        self.alias = self.ui.start_login()
        try:
            self.socket.connect(self.server_adrs)
            self.ui.end_login()
            self.send_thread.start()
            self.recv_thread.start()
            self.ui.start_chat()
            while True:
                try:
                    while True:
                        msg = self.received_queue.get_nowait()
                        self.ui.parse_and_push(msg)
                except queue.Empty:
                    pass
                outgoing = self.ui.get_outgoing()
                for m in outgoing:
                    m.set_alias(self.alias)
                    self.outgoing_queue.put(m)
                self.ui.update_chat()
                sleep(0.2)
        except OSError:
            #exit here
            pass
    
    def __send_loop(self):
        try:
            while True:
                msg = self.outgoing_queue.get()
                self.socket.send(msg.to_string().encode())
        except OSError:
            #exit here
            pass

    def __recv_loop(self):
        try:
            while True:
                data = self.socket.recv(1024)
                self.received_queue.put(data.decode())
        except OSError:
            #exit here
            pass

if __name__ == '__main__':
    cl = Client()
    cl.main_loop()
