import socket
import sys

class Server:

    def __int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController):
        self.hostname = hostname
        self.port = port
        self.idcounter = idcounter
        self.freeid = freeid
        self.sendQ = sendQ
        self.receiveQ = receiveQ
        self.CMDController = CMDController

    def process_incoming_con(self):

    def get_free_id(self):

    def accept_connection(self):

    def reject_connection(self):