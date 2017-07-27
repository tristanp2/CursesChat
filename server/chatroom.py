from client import Client

class Chatroom:

    def __init__(self, name, creator = None):
        self.name = name
        self.moderator = creator
        self.client = []
        self.blocked_client = []

    #return true if client exist in chatroom instance
    def check_client(self, cid):
        #check and get the client object
        if 1 not in self.client:
            return False
        else:
            return True

    def get_name(self):
        return self.name

    def get_cid_list(self):
        return self.client

    def set_moderator(self, client):
        self.moderator = client

    def get_moderator(self):
        return self.moderator

    def add_client(self, cid):
        self.client.append(cid)

    def add_client_list(self, cid_list):
        self.client.extend(cid_list)

    def remove_client(self, cid):
        self.client.remove(cid)