from chatroom import Chatroom
from message import Message
from message_type import MessageType
import queue
import copy

class CMDcontroller:

    def __init__(self, client_alias_dict, client_dict, chatroom_dict):
        self.chatroom_dict = chatroom_dict
        self.client_dict = client_dict
        self.client_alias_dict = client_alias_dict
        self.outgoing_queue = queue.Queue()
        self.server_alias = 'server'
        self.main_room_name = 'main_chatroom'

    #return true if the message is permitted
    #return false if the message is not permitted
    def isPermitted(self, msg):
        type = msg.type
        payload = msg.payload
        client = self.client_dict[msg.cid]
        current_chatroom = client.get_chatroom()
        client_list = list(self.client_dict.values())
        chatroom_name_list = list(self.chatroom_dict.keys())

        if type == MessageType.alias:
            #check whether the name is taken
            for c in client_list:
                if c.get_alias() == payload:
                    return False
                else:
                    return True
        if type == MessageType.join:
            if current_chatroom == payload:
                return False
            else:
                return True
        if type == MessageType.create:
            for ch in chatroom_name_list:
                if ch == payload:
                    return False
                else:
                    return True
        if type == MessageType.delete:
            if current_chatroom != payload:
                return False
            else:
                if client != self.chatroom_dict[current_chatroom].get_moderator():
                    return False
                else:
                    return True
        return True

    def process_message(self, msg):
        type = msg.type
        client = self.client_dict[msg.cid]

        if type == MessageType.alias:
            self.set_alias(client, msg.payload)
        elif type == MessageType.chat_message:
            self.chat_message(client, msg)
        elif type == MessageType.block:
            self.block_user(client, msg.payload)
        elif type == MessageType.create:
            name = msg.payload
            self.create_chatroom(name,client)
        elif type == MessageType.delete:
            self.delete_chatroom()
        elif type == MessageType.join:
            self.join_chatroom(client, msg.payload)
        elif type == MessageType.leave:
            self.leave_chatroom(client)
        elif type == MessageType.help:
            self.help(client)
        elif type == MessageType.login:
            self.login(msg.alias, client)

    def pop_outgoing(self):
        return self.outgoing_queue.get()

    def login(self, alias, client):
        self.client_alias_dict[alias] = client.get_cid()
        self.set_alias(client, alias)
        cr = self.chatroom_dict[self.main_room_name]
        self.do_chatroom_update(cr)

    def logout(self):
        pass

    def __broadcast_data(self, message, client_list):
        for client_cid in client_list:
            client = self.client_dict[client_cid]
            msg = copy.copy(message)
            msg.cid = client.get_cid()
            self.outgoing_queue.put(msg)

    def help(self, client):
        # print options.values()?
        help_list = []
        restricted = [MessageType.chat_message.name, MessageType.chatroom_update.name, MessageType.start_server.name, MessageType.stop_server.name, MessageType.login.name, MessageType.logout.name]
        for value in MessageType:
            if value.name not in restricted:
                help_list.append(value.name)
        payload = ', /'.join(help_list)
        payload = '/' + payload
        msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, payload)
        self.outgoing_queue.put(msg)

    def chat_message(self, client, msg):
        chatroom = self.chatroom_dict[client.get_chatroom()]
        self.__broadcast_data(msg, chatroom.client)

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def __switch_chatroom(self, src_room, dest_room, client):
        src_room.remove_client(client.get_cid())
        src_deleted = False

        #if moderator leaves a chatroom, boot everyone to main
        if client == src_room.get_moderator():
            kicked_client_cids = src_room.get_cid_list()
            self.chatroom_dict[self.main_room_name].add_client_list(kicked_client_cids)
            for cid in kicked_client_cids:
                cli = self.client_dict[cid]
                cli.set_chatroom(self.main_room_name)
            del self.chatroom_dict[src_room.get_name()]
            src_deleted = True

        dest_room.add_client(client.get_cid())
        client.set_chatroom(dest_room.get_name())
        if not src_deleted:
            self.do_chatroom_update(src_room)
        else:
            self.do_chatroom_update(self.chatroom_dict[self.main_room_name])
        self.do_chatroom_update(dest_room)
      
    def leave_chatroom(self, client):
        #client can't leave main chatroom
        if client.get_chatroom() == self.main_room_name:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message,"sorry. you can not leave main chatroom. type /quit to exit the program")
            self.outgoing_queue.put(msg)
        else:
            dest_cr = self.chatroom_dict[self.main_room_name]
            src_cr = self.chatroom_dict[client.get_chatroom()]
            self.__switch_chatroom(src_cr, dest_cr, client)

    def join_chatroom(self, client, chatroom_name):
        old_chatroom = self.chatroom_dict[client.get_chatroom()]
        try:
            new_chatroom = self.chatroom_dict[chatroom_name]
        except KeyError:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Chat room ' + chatroom_name + ' not found')
            self.outgoing_queue.put(msg)
        else:
            self.__switch_chatroom(old_chatroom, new_chatroom, client)

    #Creates and pushes update messages for everyone in chatroom   
    def do_chatroom_update(self, chatroom):
        alias_list = list(map(lambda x: self.client_dict[x].get_alias(), chatroom.client))
        payload = chatroom.get_name() + ' ' + ' '.join(alias_list)
        for cid in chatroom.client:
            cli = self.client_dict[cid]
            msg = Message(cli.get_cid(), cli.get_alias(), MessageType.chatroom_update, payload)
            self.outgoing_queue.put(msg)

    def create_chatroom(self, name, client):
        new_room = self.chatroom_dict[name] = Chatroom(name)
        new_room.set_moderator(client)
        old_room = self.chatroom_dict[client.get_chatroom()]
        self.__switch_chatroom(old_room, new_room, client)

    def delete_chatroom(self):
        pass

    def set_alias(self, client, alias):
        client.set_alias(alias)
        msg = Message(client.get_cid(), client.get_alias(), MessageType.alias, client.get_alias())
        cr = self.chatroom_dict[client.get_chatroom()]
        self.do_chatroom_update(cr)
        self.outgoing_queue.put(msg)

    def block_user(self, client, block_alias):
        chatroom = self.client_dict[client.get_chatroom()]
        target_client = None
        #TODO:  Need a way to find client object by alias for this command. Maybe another dictionary? 
        #       Alternative is to iterate through the cid-client dict, but that would make this command terribly expensive 

    def unblock_user(self):
        pass

