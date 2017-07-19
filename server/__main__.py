#reference
#https://pymotw.com/3/socket/tcp.html
#run it with -m server on seng299 folder
from .server import *

hostname = str(socket.gethostbyname(socket.gethostname()))
port = 10000
idcounter = 0
freeid = 1001
sendQ = 0
receiveQ = 0
CMDController = 0#CMDController()#need the class

#__int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

mainserver = Server(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

print('Current server ip is ' + hostname)

while True:

    read_sockets, write_sockets, error_sockets = select.select(mainserver.connected_client_socket, [], [])

    for sock in read_sockets:
        if sock == mainserver.socket:
            connection, client_adrs = mainserver.socket.accept()
            mainserver.connected_client_socket.append(connection)
            print('Client {!r} connected'.format(client_adrs))
            mainserver.broadcast_data(connection, '{!r} entered chatroom'.format(client_adrs) , mainserver.connected_client_socket)

        else:
            try:
                data = sock.recv(1024)
                if data:
                    mainserver.broadcast_data(sock ,'<{}>: {}'.format(sock.getpeername, data) ,mainserver.connected_client_socket)
            except:
                mainserver.broadcast_data(sock ,'Client {} is offline'.format(sock.getsockname) ,mainserver.connected_client_socket)
                print('Client {} is offline'.format(sock.getsockname))
                sock.close()
                mainserver.connected_client_socket.remove(sock)
                continue

mainserver.shutdown(mainserver.socket)

"""
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
"""