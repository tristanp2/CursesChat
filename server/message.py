import datetime

class Message:

    def __init__(self):
        self.clientID = -1
        self.type = MessageType()
        self.payload = ''
        self.timestamp = datetime.time.today

    def create_message(self, clientID, type, payload):
        pass
