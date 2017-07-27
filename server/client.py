class Client:

    def __init__(self, cid, chatroom, socket):
        self.id = cid
        self.aliasname = ''
        self.chatroom = chatroom
        self.socket = socket
        self.owned_rooms = []

    def get_chatroom(self):
        return self.chatroom

    def add_created_room(self, cr_name):
        self.owned_rooms.append(cr_name)

    def get_owned_rooms(self):
        return self.owned_rooms

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