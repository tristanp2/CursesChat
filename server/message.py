from datetime import datetime
from message_type import MessageType

class Message:

    #TODO: add cid
    #note: it does not handle type for now
    #TODO: will take away alias eventually
    def __init__(self ,cid ,alias, type, payload):
        self.cid = cid
        self.alias = alias
        self.type = MessageType(int(type))
        self.payload = ' '.join(payload)
        t = datetime.now()
        str_t = t.strftime('%H:%M:%S')
        self.timestamp = str_t
