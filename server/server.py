import socket
import select
import sys
from .send_message_handler import SendMessageHandler
from .receive_message_handler import ReceiveMessageHandler
from .client import Client
from .chatroom import Chatroom
from .command_controller import CMDcontroller

class Server:

    def __init__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController):
        self.hostname = hostname
        self.port = port
        #create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_adrs = (hostname, port)
        self.idcounter = idcounter
        #we can mark used id as 'u' and free id as 'f'
        self.freeid = {}
        #id can be related to the client
        self.client = []
        self.connected_client_socket = []
        self.send_MSGHandler = SendMessageHandler(self.socket)
        self.receive_MSGHandler = ReceiveMessageHandler(self.socket)
        self.CMDController = CMDController

        self.socket.bind(self.get_adrs())
        self.socket.listen(5)
        self.connected_client_socket.append(self.socket)

    def get_adrs(self):
        return self.server_adrs

    def broadcast_data(self, sock, message, List):
        for socket in List:
            try:
                socket.send(message)
            except:
                socket.close()
                List.remove(socket)

    def process_incoming_con(self, socket):
        pass
        #stringdata = connection.recv(1024)

    def get_free_id(self):
        pass

    def accept_connection(self):
        self.connection, self.client_adrs = self.socket.accept()

    def reject_connection(self):
        pass

    def shutdown(self, socket):
        socket.close()