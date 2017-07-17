from .server import Server

hostname = "localhost"
port = 8870
idcounter = 0
freeid = 1001
sendQ = con_queue
receiveQ = con_queue
CMDController = CMDController()#need the class

#__int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

mainserver = Server(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

sock = Server.get_sock()

sock.listen(1)
