import socket
import sys
import queue
from ui import UI
import threading
from message_type_client import MessageType
from message_client import Message
from time import sleep
from datetime import datetime

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #asumming the server is localhost and port is 10000
        #self.server_adrs = ('134.87.170.182', 10000)
        self.received_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()
        self.ui = UI()
        self.exit_lock = threading.Lock()
        self.exit = False
        self.login_message = Message(MessageType.login,'',None, None)

        self.send_thread = threading.Thread(None, self.__send_loop, 'send_t')
        self.send_thread.setDaemon(True)
        self.recv_thread = threading.Thread(None, self.__recv_loop, 'recv_t')
        self.recv_thread.setDaemon(True)

    def parse_received(self, string):
        args = string.split(' ')
        msg = None
        if len(args) >= 2:
            alias = args[0]
            mtype = MessageType(int(args[1]))
            time = datetime.strptime(args[2], Message.time_format)
            payload = ' '.join(args[3:])
            msg = Message(mtype, payload, time, alias)
        return msg

    def main_loop(self):
        try:
            if len(sys.argv) >= 2:
                self.server_adrs = (sys.argv[1], 10000)
            else:
                #TODO: Make different exception for this
                raise AttributeError
            alias = self.ui.start_login(self.server_adrs[0], False)
            self.login_message.set_alias(alias)
            self.socket.connect(self.server_adrs)
            self.recv_thread.start()
            self.send_thread.start()
            self.outgoing_queue.put(self.login_message)
            """
            while True:
                string = self.received_queue.get()
                msg =  self.parse_received(string)
                if msg.get_type() == MessageType.refuse:
                    alias = self.ui.start_login(self.server_adrs[0], True)
                    self.login_message.set_alias(alias)
                    self.outgoing_queue.put(self.login_message)
                elif msg.get_type() == MessageType.alias:
                    self.alias = msg.get_payload()
                    break        
            """        
            self.ui.end_login()            
            logged_in = False
            self.ui.push_received(Message(MessageType.chat_message, 'Logging in...', datetime.now(),'Client'))
            self.ui.start_chat()
            while True and not self.exit:
                try:
                    while True:
                        string = self.received_queue.get_nowait()
                        msg = self.parse_received(string)
                        type = msg.get_type()
                        if type == MessageType.alias:
                            self.alias = msg.get_payload()
                            if not logged_in:
                                logged_in = True
                        elif not logged_in and type == MessageType.refuse:
                            self.ui.push_received(Message(MessageType.chat_message, 'Login rejected. Please try a new alias using /alias command', datetime.now(),'Client'))
                        elif logged_in:
                            self.ui.push_received(msg)
                except queue.Empty:
                    pass
                outgoing = self.ui.get_outgoing()
                for m in outgoing:
                    type = m.get_type()
                    if type == MessageType.quit:
                        self.__set_exit()
                    elif not logged_in:
                        if type == MessageType.alias:
                            self.login_message.set_alias(m.get_payload())
                            self.outgoing_queue.put(self.login_message)
                    else:
                         m.set_alias(self.alias)
                         self.outgoing_queue.put(m)
                self.ui.update_chat()
                sleep(0.2)
        except OSError:
            self.__set_exit('Networking exception')
            self.ui.do_exit(self.exit_msg)
        except AttributeError:
            self.ui.do_exit(None)
            print('Please specify an IP address to connect to')
            print('Usage: client.py ip_address')
            raise
        except KeyboardInterrupt:
            self.__set_exit('Keyboard Interrupt')
            self.ui.do_exit(self.exit_msg)
        except:
            self.__set_exit('Unknown exception')
            self.ui.do_exit(self.exit_msg)
        else:
            self.ui.do_exit(self.exit_msg)

    def __set_exit(self, msg = None):
        self.exit_lock.acquire()
        self.exit = True
        self.exit_msg = msg
        self.exit_lock.release()

    def __split_received(self, received):
        return received.split(Message.end_char)[:-1]

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
                m_list = self.__split_received(data.decode())
                for m in m_list:
                    self.received_queue.put(m)
        except OSError:
            self.__set_exit('Networking exception')

if __name__ == '__main__':
    cl = Client()
    cl.main_loop()
