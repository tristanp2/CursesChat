import socket
import sys
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
        #we can mark used id as 'u' and free id as 'f'
        self.freeid = list(range(0,freeid))
        #id can be related to the client
        self.client_sock_to_cid = {}
        self.client_cid_to_sock = {}
        self.client_cid_to_client = {}
        self.chatroom = {}
        self.connected_client_socket = []
        #self.send_MSGHandler = SendMessageHandler(self.socket)
        #self.receive_MSGHandler = ReceiveMessageHandler(self.socket)
        self.CMDController = CMDcontroller()

    def start(self):
        self.socket.bind(self.get_adrs())
        self.socket.listen(5)
        self.connected_client_socket.append(self.socket)
        chatroom = Chatroom("main_chatroom")
        self.chatroom[chatroom.get_name()] = chatroom

    def stop(self):
        pass

    def get_adrs(self):
        return self.server_adrs

    def broadcast_data(self, sock, message, List):
        for socket in List:
            if socket != self.socket:
                try:
                    print(message)
                    socket.send(message.encode())
                except OSError as err:
                    print('OS error: {0}'.format(err))
                    print(socket)
                    #socket.close()
                    #List.remove(socket)

    def process_incoming_con(self, socket):
        pass
        #stringdata = connection.recv(1024)

    #return free client id; if no id is in the freeid list, return -1
    def get_free_id(self):
        if len(self.freeid) > 0:
            return self.freeid.pop(0)
        else:
            return -1

    #add the cid back to freeid pool
    def freeup_cid(self, cid):
        self.freeid.append(cid)

    def accept_connection(self):
        self.connection, self.client_adrs = self.socket.accept()

    def reject_connection(self):
        pass

    def shutdown(self, socket):
        socket.close()