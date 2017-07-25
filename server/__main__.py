#reference
#https://pymotw.com/3/socket/tcp.html
#run it with -m server on seng299 folder
from server import Server
import select
import socket

hostname = str(socket.gethostbyname(socket.gethostname()))
port = 10000
idcounter = 0
freeid = 1000
sendQ = 0
receiveQ = 0
CMDController = 0#CMDController()#need the class

mainserver = Server(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)
mainserver.start()

print('Current server ip is ' + hostname)

while True:

    read_sockets, write_sockets, error_sockets = select.select(mainserver.connected_client_socket, [], [])

    for sock in read_sockets:
        #getting new client connection
        if sock == mainserver.socket:
            connection, client_adrs = mainserver.socket.accept()
            mainserver.connected_client_socket.append(connection)
            cid = mainserver.get_free_id()
            client = Client(cid, connection)
            mainserver.client[connection] = client
            print('Client {!r} connected'.format(client_adrs))
            #TODO: broadcast alias not this, but how can I get alias
            #mainserver.broadcast_data(connection, '{!r} entered chatroom'.format(client_adrs) , mainserver.connected_client_socket)

        else:
            #print('enter else')
            try:
               #print('before recv')
                data = sock.recv(1024)
                #print('after recv')
                if data:
                    msg = mainserver.CMDController.parse_input(data.decode())
                    #message format should be: alias type time data
                    mainserver.broadcast_data(sock ,'{} {} {} {}'.format(msg.alias, msg.type.value, msg.timestamp, msg.payload) ,mainserver.connected_client_socket)
            except OSError as err:
                print('OS error: {0}'.format(err))
                print('Client {} is offline'.format(sock.getpeername))
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