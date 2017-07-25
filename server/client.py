class Client:

    def __init__(self, cid, chatroomid, socket):
        self.id = cid
        self.aliasname = ''
        self.chatroomid = chatroomid
        self.chatroom = ''
        self.socket = socket

    def get_chatroom_id(self):
        return self.chatroomid

    def get_cid(self):
        return self.id

    def get_alias(self):
        return self.aliasname

    def get_clientinchatroom(self):
        return self.chatroom

    #question: does it makes sense to do it in here?
    def set_alias(self, alias):
        self.aliasname = alias

    #question: does it makes sense to do it in here?
    def set_chatroom(self, chatroom):
        self.chatroom = chatroom