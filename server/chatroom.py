from client import Client

class Chatroom:

    def __init__(self):
        self.name = ''
        self.moderator = Client()
        self.client = {}
