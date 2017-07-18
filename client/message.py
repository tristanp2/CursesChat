from message_type import MessageType
import datetime
class Message:
    #change this
    _type = MessageType.chat_message
    _payload = 'hello'
    _timestamp = datetime.time

    def __init__(self, type, payload, timestamp):
        pass
    def get_alias(self):
        return 'bob'
    def get_payload(self):
        return self._payload
    def get_type(self):
        return self._type
    def __init__(self):
        pass