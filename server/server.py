import socket
import sys

class Server:

    def __init__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController):
        self.hostname = hostname
        self.port = port
        #create a TCP/IP socket
        self.sock = socket.socket(hostname, port)
        self.idcounter = idcounter
        self.freeid = freeid
        self.sendQ = sendQ
        self.receiveQ = receiveQ
        self.CMDController = CMDController

    def get_sock(self):
        return self.sock

    def process_incoming_con(self):
        pass

    def get_free_id(self):
        pass

    def accept_connection(self):
        pass

    def reject_connection(self):
        pass