class Client:

    def __init__(self, cid, roomname, socket):
        self.id = cid
        self.alias = ''
        self.chatroom_name = roomname
        self.socket = socket
        self.owned_rooms = []
        self.blocked_rooms = []

    def get_chatroom_name(self):
        return self.chatroom_name

    def add_created_room(self, cr_name):
        self.owned_rooms.append(cr_name)

    def get_owned_rooms(self):
        return self.owned_rooms

    def get_cid(self):
        return self.id

    def block(self, room_name):
        self.blocked_rooms.append(room_name)

    def unblock(self, room_name):
        self.blocked_rooms.remove(room_name)

    def is_blocked(self, room_name):
        return room_name in self.blocked_rooms

    def get_alias(self):
        return self.alias

    #question: does it makes sense to do it in here?
    def set_alias(self, alias):
        self.alias = alias

    #question: does it makes sense to do it in here?
    def set_chatroom_name(self, roomname):
        self.chatroom_name = roomname