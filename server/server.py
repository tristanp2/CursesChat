import socket
import sys

class Server:

    def __init__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController):
        self.hostname = hostname
        self.port = port
        #create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_adrs = (hostname, port)
        self.idcounter = idcounter
        self.freeid = freeid
        self.sendQ = sendQ
        self.receiveQ = receiveQ
        self.CMDController = CMDController

    def get_adrs(self):
        return self.server_adrs

    def process_incoming_con(self):
        pass

    def get_free_id(self):
        pass

    def accept_connection(self):
        self.connection, self.client_adrs = self.socket.accept()

    def reject_connection(self):
        pass