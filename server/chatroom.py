from client import Client

class Chatroom:

    def __init__(self, name):
        self.name = name
        # key as cid and value as alias
        self.moderator = {}
        self.client = []

    #return true if client exist in chatroom instance
    def check_client(self, cid):
        #check and get the client object
        if 1 not in self.client:
            return False
        else:
            return True

    def get_cid_list(self):
        return self.client

    def add_client(self, cid):
        self.client.append(cid)

    def remove_client(self, cid):
        self.client.remove(cid)