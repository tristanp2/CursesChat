import socket
import select
import sys
from client import Client
from chatroom import Chatroom
from message import Message
from command_controller import CMDcontroller
from message_type import MessageType
import queue
import threading

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
        send_queue = queue.Queue()
        receive_queue = queue.Queue()
        #self.send_MSGHandler = SendMessageHandler(self.socket)
        #self.receive_MSGHandler = ReceiveMessageHandler(self.socket)
        self.controller = CMDcontroller(self.client_cid_to_client, self.chatroom)
        self.send_thread = threading.Thread(None, self.__send_loop, 'send_t')
        self.send_thread.setDaemon(True)

    def __send_loop(self):
        try:
            while True:
                msg = self.controller.pop_outgoing()
                sock = self.client_cid_to_sock[msg.cid]
                string = msg.to_string()
                sock.send(string.encode())
                print(string)
        except OSError:
            print('Error in send loop')

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


    def parse_input(self, message, sock):
        cid = self.client_sock_to_cid[sock]
        args = message.split(' ')
        alias = args[0]
        type = MessageType(int(args[1]))
        payload = ' '.join(args[2:])
        #TODO: add cid as first parameter
        msg = Message(cid, alias, type, payload)
        #TODO: push to receive queue, so we dont need to return msg
        return msg

    def main_loop(self):
        self.send_thread.start()
        while True:

            read_sockets, write_sockets, error_sockets = select.select(self.connected_client_socket, [], [])

            for sock in read_sockets:
                # getting new client connection
                if sock == self.socket:
                    connection, client_adrs = self.socket.accept()
                    self.connected_client_socket.append(connection)
                    cid = self.get_free_id()
                    if cid == -1:
                        print('reach maximum amount of user the server can handle')
                    client = Client(cid, 'main_chatroom', connection)
                    # socket: cid
                    self.client_sock_to_cid[connection] = cid
                    # cid: socket
                    self.client_cid_to_sock[cid] = connection
                    # cid: Client
                    self.client_cid_to_client[cid] = client
                    self.chatroom['main_chatroom'].add_client(cid)
                    print('Client {!r} connected'.format(client_adrs))
                    # TODO: broadcast alias not this, but how can I get alias
                    # self.broadcast_data(connection, '{!r} entered chatroom'.format(client_adrs) , self.connected_client_socket)

                else:
                    try:
                        data = sock.recv(1024)
                        if data:
                            msg = self.parse_input(data.decode(), sock)
                            self.controller.process_message(msg)
                         
                    except OSError as err:
                        print('OS error: {0}'.format(err))
                        print('Client {} is offline'.format(sock.getpeername()))
                        sock.close()
                        self.connected_client_socket.remove(sock)
                        temp_cid = self.client_sock_to_cid[sock]
                        temp_client = self.client_cid_to_client[temp_cid]
                        temp_chatroom = self.chatroom[temp_client.get_chatroom()]
                        temp_chatroom.remove_client(temp_cid)
                        del self.client_sock_to_cid[sock]
                        del self.client_cid_to_sock[temp_cid]
                        del self.client_cid_to_client[temp_cid]
                        self.freeup_cid(temp_cid)
                        continue