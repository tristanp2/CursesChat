from message_type import MessageType
import datetime
class Message:
    #change this
    _type = MessageType.chat_message
    _payload = 'hello'
    _timestamp = datetime.time

    def create_message(type, payload, timestamp):
        pass
    def get_alias():
        return 'bob'
    def get_payload():
        return _payload
    def get_type(self):
        return self._type
    def __init__(self):
        pass