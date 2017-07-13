import server

hostname = "localhost"
port = 8870
idcounter = 0
freeid = 1001
sendQ = con_queue
receiveQ = con_queue
CMDController = #need the class

#__int__(self, hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)
#getting error of Cannot find reference
mainserver = server.Server.__init__(hostname, port, idcounter, freeid, sendQ, receiveQ, CMDController)

#same error as about
sock = server.Server.get_sock()

