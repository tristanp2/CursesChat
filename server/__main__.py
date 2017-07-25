#reference
#https://pymotw.com/3/socket/tcp.html
#run it with -m server on seng299 folder
from server import Server
from client import Client
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
            if cid == -1:
                print('reach maximum amount of user the server can handle')
            client = Client(cid, 'main_chatroom', connection)
            #socket: cid
            mainserver.client_sock_to_cid[connection] = cid
            #cid: socket
            mainserver.client_cid_to_sock[cid] = connection
            #cid: Client
            mainserver.client_cid_to_client[cid] = client
            mainserver.chatroom['main_chatroom'].add_client(cid)
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
                    msg = mainserver.controller.parse_input(data.decode())
                    client_id = mainserver.client_sock_to_cid[sock]
                    client = mainserver.client_cid_to_client[client_id]
                    current_chatroom = mainserver.chatroom[client.get_chatroom()]
                    filtered_list = [mainserver.client_cid_to_sock[k] for k in current_chatroom.get_cid_list()]
                    #message format should be: alias type time data
                    mainserver.broadcast_data(sock ,'{} {} {} {}'.format(msg.alias, msg.type.value, msg.timestamp, msg.payload) ,filtered_list)
            except OSError as err:
                print('OS error: {0}'.format(err))
                print('Client {} is offline'.format(sock.getpeername()))
                sock.close()
                mainserver.connected_client_socket.remove(sock)
                temp_cid = mainserver.client_sock_to_cid[sock]
                temp_client = mainserver.client_cid_to_client[temp_cid]
                temp_chatroom = mainserver.chatroom[temp_client.get_chatroom()]
                temp_chatroom.remove_client(temp_cid)
                del mainserver.client_sock_to_cid[sock]
                del mainserver.client_cid_to_sock[temp_cid]
                del mainserver.client_cid_to_client[temp_cid]
                mainserver.freeup_cid(temp_cid)
                continue

mainserver.shutdown(mainserver.socket)