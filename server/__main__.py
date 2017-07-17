#reference
#https://pymotw.com/3/socket/tcp.html
from .server import *

hostname = "localhost"
port = 8870
idcounter = 0
freeid = 1001
sendQ = 0
receiveQ = 0
CMDController = 0#CMDController()#need the class

#__int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

mainserver = Server(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

#sock = mainserver.get_sock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mainserver.sock.bind(s)

mainserver.sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_adrs = mainserver.sock.accept()

    try:
        print('connection from', client_adrs)

        while True:
            #receving 16 bytes of data
            stringdata = connection.recv(16)
            print('received {!r}'.format(stringdata))
            if stringdata:
                print('sending data back to the client')
                connection.sendall(stringdata)
            else:
                print('no data from', client_adrs)
                break

    finally:
        connection.close()

