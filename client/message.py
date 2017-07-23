class Message:
    _type = MessageType()
    _payload = []
    _timestamp = datetime().time

    def create_message(type, payload, timestamp):
        pass