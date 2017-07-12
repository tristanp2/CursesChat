import signal
import pyuv

class Server:

    def __init__(self):


    def start(self):


    def __on_read(client, data, error):
        if data is None:
            client.close()
            clients.remove(client)
            return
        client.write(data)

    def __on_connection(server, error):
        client = pyuv.TCP(server.loop)
        server.accept(client)
        clients.append(client)
        client.start_read(on_read)

    def __signal_cb(handle, signum):
        [c.close() for c in clients]
        signal_h.close()
        server.close()