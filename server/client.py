class Client:

    def __init__(self, cid, chatroom, socket):
        self.id = cid
        self.aliasname = ''
        self.chatroom = chatroom
        self.socket = socket

    def get_chatroom(self):
        return self.chatroom

    def get_cid(self):
        return self.id

    def get_alias(self):
        return self.aliasname

    #question: does it makes sense to do it in here?
    def set_alias(self, alias):
        self.aliasname = alias

    #question: does it makes sense to do it in here?
    def set_chatroom(self, chatroom):
        self.chatroom = chatroom