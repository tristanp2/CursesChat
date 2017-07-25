import socket
import sys
import queue
from ui import UI
import threading
from message_type_client import MessageType
from time import sleep

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #asumming the server is localhost and port is 10000
        self.server_adrs = ('134.87.133.12', 10000)
        self.received_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()
        self.ui = UI()
        self.exit_lock = threading.Lock()
        self.exit = False

        self.send_thread = threading.Thread(None, self.__send_loop, 'send_t')
        self.send_thread.setDaemon(True)
        self.recv_thread = threading.Thread(None, self.__recv_loop, 'recv_t')
        self.recv_thread.setDaemon(True)

    def main_loop(self):
        self.alias = self.ui.start_login()
        try:
            self.socket.connect(self.server_adrs)
            self.ui.end_login()
            self.send_thread.start()
            self.recv_thread.start()
            self.ui.start_chat()
            while True and not self.exit:
                try:
                    while True:
                        msg = self.received_queue.get_nowait()
                        self.ui.parse_and_push(msg)
                except queue.Empty:
                    pass
                outgoing = self.ui.get_outgoing()
                for m in outgoing:
                    if m.get_type() == MessageType.quit:
                        self.__set_exit()
                    else:
                        m.set_alias(self.alias)
                        self.outgoing_queue.put(m)
                self.ui.update_chat()
                sleep(0.2)
        except OSError:
            self.__set_exit('Exception in main loop')
        self.ui.do_exit(self.exit_msg)

    def __set_exit(self, msg = None):
        self.exit_lock.acquire()
        self.exit = True
        self.exit_msg = msg
        self.exit_lock.release()

    def __send_loop(self):
        try:
            while True and not self.exit:
                msg = self.outgoing_queue.get()
                self.socket.send(msg.to_string().encode())
        except OSError:
            self.__set_exit('Networking exception')

    def __recv_loop(self):
        try:
            while True and not self.exit:
                data = self.socket.recv(1024)
                self.received_queue.put(data.decode())
        except OSError:
            self.__set_exit('Networking exception')

if __name__ == '__main__':
    cl = Client()
    cl.main_loop()
