from .chatroom import Chatroom

class CMDcontroller:

    def __init__(self):
        self.chatroom = Chatroom()

    def isPermitted(self, client):
        pass

    def proccessCMD(self, command):
        pass