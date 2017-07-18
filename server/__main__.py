#reference
#https://pymotw.com/3/socket/tcp.html
#run it with -m server on seng299 folder
from .server import *

hostname = 'localhost'
port = 10000
idcounter = 0
freeid = 1001
sendQ = 0
receiveQ = 0
CMDController = 0#CMDController()#need the class

#__int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

mainserver = Server(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

#sock = mainserver.get_sock()

mainserver.socket.bind(mainserver.get_adrs())

mainserver.socket.listen(1)

while True:
    print('waiting for a connection')
    connection, client_adrs = mainserver.socket.accept()

    try:
        print('connection from', client_adrs)

        while True:
            #receving 16 bytes of data
            stringdata = connection.recv(1024)
            print('received {!r}'.format(stringdata))
            if stringdata:
                print('sending data back to the client')
                connection.sendall(stringdata)
            else:
                print('no data from', client_adrs)
                break

    finally:
        connection.close()

