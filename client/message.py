from message_type import MessageType
import datetime
class Message:
    #change this
    def __init__(self, type, payload, timestamp, alias = None):
        self._type = type       #MessageType
        self._payload = payload #str
        self._alias = alias     #str
        self._time = timestamp  #datetime

    def to_string(self):
        return ' '.join([self._alias, str(self._type.value), self._payload])

    def get_time(self):
        return self._time

    def get_alias(self):
        return self._alias

    def set_alias(self, alias):
        self._alias = alias

    def get_payload(self):
        return self._payload

    def get_type(self):
        return self._type