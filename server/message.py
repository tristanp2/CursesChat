from datetime import datetime
from message_type import MessageType

class Message:

    #TODO: add cid
    #note: it does not handle type for now
    #TODO: will take away alias eventually
    #alias is author of message
    #cid is recipient
    end_char = chr(30)
    def __init__(self, cid, alias, type, payload):
        self.cid = cid
        self.alias = alias
        self.type = type
        self.payload = payload.strip()
        t = datetime.now()
        str_t = t.strftime('%H:%M:%S')
        self.timestamp = str_t

    def to_string(self):
        l = [self.alias, str(self.type.value), self.timestamp, self.payload]
        return ' '.join(l) + Message.end_char
