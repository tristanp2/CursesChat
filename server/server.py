import socket
import select
import sys
from send_message_handler import SendMessageHandler
from receive_message_handler import ReceiveMessageHandler
from client import Client
from chatroom import Chatroom
from command_controller import CMDcontroller

class Server:

    def __init__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController):
        self.hostname = hostname
        self.port = port
        #create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_adrs = (hostname, port)
        self.idcounter = idcounter
        #create a list from 0 to 1000 id
        self.freeid = list(range(0, freeid))
        #id can be related to the client
        self.connected_client_socket = []
        #key: client socket; value: client object
        self.client = {}
        self.chatroom = {1:Chatroom('main chatroom')}
        self.send_MSGHandler = SendMessageHandler(self.socket)
        self.receive_MSGHandler = ReceiveMessageHandler(self.socket)
        self.CMDController = CMDcontroller()

    def start(self):
        self.socket.bind(self.get_adrs())
        self.socket.listen(5)
        self.connected_client_socket.append(self.socket)

    def get_adrs(self):
        return self.server_adrs

    def broadcast_data(self, sock, message, List):
        for socket in List:
            if socket != self.socket:
                try:
                    socket.send(message.encode())
                except OSError as err:
                    print('OS error: {0}'.format(err))
                    print(socket)
                    socket.close()
                    List.remove(socket)

    def process_incoming_con(self, socket):
        pass
        #stringdata = connection.recv(1024)

    def get_free_id(self):
        if len(self.freeid) > 0:
            return self.freeid[0]
        else:
            print("No free ID are available at this moment")
            return None

    def accept_connection(self):
        self.connection, self.client_adrs = self.socket.accept()

    def reject_connection(self):
        pass

    def shutdown(self, socket):
        socket.close()