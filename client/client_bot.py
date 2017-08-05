import socket
import sys
import queue
import threading
from message_type_client import MessageType
from message_client import Message
from time import sleep
from datetime import datetime

class ClientBot:
    def __init__(self, alias):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.received_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()
        self.alias = alias

    def __send_loop(self):
        try:
            while True:
                msg = self.outgoing_queue.get()
                self.sock.send(msg.to_string().encode())
        except OSError:
            pass
    def __recv_loop(self):
        try:
            while True:
                data = self.sock.recv(1024)
                m_list = self.__split_received(data.decode())
                for m in m_list:
                    self.received_queue.put(m)
        except OSError:
            pass
    def main_loop(self):
        login_message = Message(MessageType.login,'',None, None)
        send_thread = threading.Thread(None, self.__send_loop, 'send_t')
        send_thread.setDaemon(True)
        recv_thread = threading.Thread(None, self.__recv_loop, 'recv_t')
        recv_thread.setDaemon(True)
        ip = '192.168.1.68'
        server_adrs = (ip, 10000)
        login_message.set_alias(self.alias)
        self.sock.connect(server_adrs)
        recv_thread.start()
        send_thread.start()
        self.outgoing_queue.put(login_message)
        msg = Message(MessageType.chat_message, 'hello', None, self.alias)
        while True:
            try:
                try:
                    while True:
                        string = self.received_queue.get_nowait()
                        print(self.alias + ' received\n')
                except queue.Empty:
                    pass
                self.outgoing_queue.put(msg)
                print(self.alias + ' sent\n')
                sleep(10)
            except:
                print('Exception occured for ' + self.alias)
    
    def __split_received(self, received):
        return received.split(Message.end_char)[:-1]

def spawn_bots_and_run():
    numbots = 20
    thread_list = []
    for i in range(numbots):
        temp_bot = ClientBot('bot' + str(i))
        temp_t = threading.Thread(None, temp_bot.main_loop, str(i))
        thread_list.append(temp_t)

    for t in thread_list:
        t.start()
        sleep(1)
    while True:
        print('<3')
        sleep(1)


    


if __name__ == '__main__':
    spawn_bots_and_run()
