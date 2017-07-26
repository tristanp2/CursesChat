from message_type_client import MessageType
import datetime
class Message:
    #change this
    time_format = '%H:%M:%S'
    end_char = chr(30)
    def __init__(self, type, payload, timestamp, alias = None):
        self._type = type       #MessageType
        self._payload = payload #str
        self._alias = alias     #str
        self._time = timestamp  #datetime

    def to_string(self):
        try:
            string = ' '.join([self._alias, str(self._type.value), self._payload])
        except:
            return ''
        else:
            return string

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