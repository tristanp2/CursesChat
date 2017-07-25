#reference
#https://pymotw.com/3/socket/tcp.html
#run it with -m server on seng299 folder
from server import Server
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

mainserver.main_loop()

mainserver.shutdown(mainserver.socket)