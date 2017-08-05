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
        current_chatroom = client.get_chatroom_name()
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
    def __refuse_empty(self, cid, msg_type):
        msg = Message(cid, self.server_alias, MessageType.chat_message, 'Command ''{}'' failed because no arguments were given'.format(msg_type.name))
        self.outgoing_queue.put(msg)

    def process_message(self, msg):
        type = msg.type
        client = self.client_dict[msg.cid]
        len_payload = len(msg.payload)

        if type == MessageType.alias:
            self.set_alias(client, msg.payload)
        elif type == MessageType.chat_message:
            self.chat_message(client, msg)
        elif type == MessageType.block:
            if len_payload == 0:
                self.__refuse_empty(msg.cid, type)
            else:
                self.block_user(client, msg.payload)
        elif type == MessageType.create:
            if len_payload == 0:
                self.__refuse_empty(msg.cid, type)
            else:
                name = msg.payload
                self.create_chatroom(name,client)
        elif type == MessageType.delete:
            self.delete_chatroom(client, msg.payload)
        elif type == MessageType.join:
            if len_payload == 0:
                self.__refuse_empty(msg.cid, type)
            else:
                self.join_chatroom(client, msg.payload)
        elif type == MessageType.leave:
            self.leave_chatroom(client)
        elif type == MessageType.help:
            self.help(client)
        elif type == MessageType.login:
            self.login(msg.alias, client)
        elif type == MessageType.block:
            self.block_user(client, msg.payload)
        elif type == MessageType.unblock:
            self.unblock_user(client, msg.payload)

    def pop_outgoing(self):
        return self.outgoing_queue.get()

    #ya this is a mess
    def login(self, alias, client):
        if len(alias) <= 2:
            msg = Message(client.get_cid(), self.server_alias, MessageType.refuse,'')
            self.outgoing_queue.put(msg)
            return
        try:
            self.client_alias_dict[alias]
        except KeyError:
            self.client_alias_dict[alias] = client.get_cid()
            client.set_alias(alias)
            msg = Message(client.get_cid(), client.get_alias(), MessageType.alias, client.get_alias())
            cr = self.chatroom_dict[self.main_room_name]
            self.outgoing_queue.put(msg)
            self.do_chatroom_update(cr)
        else:
            msg = Message(client.get_cid(), self.server_alias, MessageType.refuse,'')
            self.outgoing_queue.put(msg)

    def logout(self):
        pass

    def __broadcast_data(self, message, client_list):
        for client_cid in client_list:
            client = self.client_dict[client_cid]
            msg = copy.copy(message)
            msg.cid = client.get_cid()
            self.outgoing_queue.put(msg)

    def __server_notification(self, string, chatroom):
        msg = Message(0, self.server_alias, MessageType.chat_message, string)
        self.__broadcast_data(msg, chatroom.get_cid_list())

    def help(self, client):
        # print options.values()?
        help_list = []
        restricted = [MessageType.chat_message.name, MessageType.chatroom_update.name, MessageType.start_server.name, MessageType.stop_server.name, MessageType.login.name, MessageType.logout.name, MessageType.refuse.name]
        for value in MessageType:
            if value.name not in restricted:
                help_list.append(value.name)
        payload = ', /'.join(help_list)
        payload = '/' + payload
        msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, payload)
        self.outgoing_queue.put(msg)

    def chat_message(self, client, msg):
        chatroom = self.chatroom_dict[client.get_chatroom_name()]
        self.__broadcast_data(msg, chatroom.client)

    def __switch_chatroom(self, src_room, dest_room, client):
        src_room.remove_client(client.get_cid())
        dest_room.add_client(client.get_cid())
        
        client.set_chatroom_name(dest_room.get_name())
        self.do_chatroom_update(src_room)
        self.do_chatroom_update(dest_room)
        self.__server_notification(client.get_alias() + ' has joined the room', dest_room)
      
    def leave_chatroom(self, client):
        #client can't leave main chatroom
        if client.get_chatroom_name() == self.main_room_name:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message,"sorry. you can not leave main chatroom. type /quit to exit the program")
            self.outgoing_queue.put(msg)
        else:
            dest_cr = self.chatroom_dict[self.main_room_name]
            src_cr = self.chatroom_dict[client.get_chatroom_name()]
            self.__switch_chatroom(src_cr, dest_cr, client)

    def join_chatroom(self, client, chatroom_name):
        old_chatroom = self.chatroom_dict[client.get_chatroom_name()]
        try:
            new_chatroom = self.chatroom_dict[chatroom_name]
        except KeyError:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Chat room ' + chatroom_name + ' not found')
            self.outgoing_queue.put(msg)
        else:
            if client.is_blocked(new_chatroom.get_name()):
                msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Sorry, you are currently blocked from ' + new_chatroom.get_name())
                self.outgoing_queue.put(msg)
            else:
                self.__switch_chatroom(old_chatroom, new_chatroom, client)

    #Creates and pushes update messages for everyone in chatroom   
    def do_chatroom_update(self, chatroom):
        alias_list = list(map(lambda x: self.client_dict[x].get_alias(), chatroom.client))
        payload = chatroom.get_name() + ' ' + ' '.join(alias_list)
        for cid in chatroom.get_cid_list():
            cli = self.client_dict[cid]
            msg = Message(cli.get_cid(), cli.get_alias(), MessageType.chatroom_update, payload)
            self.outgoing_queue.put(msg)

    def create_chatroom(self, name, client):
        try:
            temp = self.chatroom_dict[name]
        except KeyError:
            new_room = self.chatroom_dict[name] = Chatroom(name)
            new_room.set_moderator(client)
            client.add_created_room(name)
            old_room = self.chatroom_dict[client.get_chatroom_name()]
            self.__switch_chatroom(old_room, new_room, client)
        else:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Chatroom ' + name + ' already exists')
            self.outgoing_queue.put(msg)

    def delete_chatroom(self, client, chatroom_name):
        try:
            target_room = self.chatroom_dict[chatroom_name]
        except KeyError:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Chat room ' + chatroom_name + ' not found')
            self.outgoing_queue.put(msg)
        else:
            if  client == None or client == target_room.get_moderator():
                if client:
                    client.remove_created_room(chatroom_name)
                kicked_client_cids = target_room.get_cid_list()
                main_room = self.chatroom_dict[self.main_room_name]
                main_room.add_client_list(kicked_client_cids)
                self.do_chatroom_update(main_room)
                self.__server_notification(chatroom_name + ' has been deleted, you have been kicked', target_room)
                for cid in kicked_client_cids:
                    cli = self.client_dict[cid]
                    cli.set_chatroom_name(self.main_room_name)
                del self.chatroom_dict[chatroom_name]
            else:
                msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'You need to be creator of a room to delete it')
                self.outgoing_queue.put(msg)

    def set_alias(self, client, alias):
        if len(alias) <= 2:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Alias must be at least 3 characters long')
            self.outgoing_queue.put(msg)
            return

        old_alias = client.get_alias()
        try:
            temp = self.client_alias_dict[alias]
        except KeyError:
            client.set_alias(alias)
            self.client_alias_dict[alias] = client.get_cid()
            msg = Message(client.get_cid(), client.get_alias(), MessageType.alias, client.get_alias())
            cr = self.chatroom_dict[client.get_chatroom_name()]
            if len(old_alias) > 0:
                self.__server_notification('Renamed ' + old_alias + ' to ' + alias, cr)
                try:
                    del self.client_alias_dict[old_alias]
                except KeyError:
                    pass
            self.do_chatroom_update(cr)
            self.outgoing_queue.put(msg)
        else:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Alias already exists')
            self.outgoing_queue.put(msg)

    def block_user(self, client, block_alias):
        roomname = client.get_chatroom_name()
        chatroom = self.chatroom_dict[roomname]
        if client == chatroom.get_moderator():
            try:
                target_client = self.client_dict[self.client_alias_dict[block_alias]]
                if target_client != client:
                    target_client.block(roomname)
                    if target_client.get_cid() in chatroom.get_cid_list():
                        dest = self.chatroom_dict[self.main_room_name]
                        self.__switch_chatroom(chatroom, dest, target_client)
                    to_client = Message(client.get_cid(), self.server_alias, MessageType.chat_message, '{} has been blocked from {}'.format(block_alias, roomname))
                    to_target = Message(target_client.get_cid(), self.server_alias, MessageType.chat_message, 'You have been blocked from {} by {}'.format(roomname, client.get_alias()))
                    self.outgoing_queue.put(to_client)
                    self.outgoing_queue.put(to_target)
                else:
                    msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'You cannot block yourself, dummy')
                    self.outgoing_queue.put(msg)
            except KeyError:
                msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Could not find user ' + block_alias)
                self.outgoing_queue.put(msg)
        else:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'You must be moderator of this room to block someone from it')
            self.outgoing_queue.put(msg)

    def unblock_user(self, client, unblock_alias):
        roomname = client.get_chatroom_name()
        chatroom = self.chatroom_dict[roomname]
        if client == chatroom.get_moderator():
            try:
                target_client = self.client_dict[self.client_alias_dict[unblock_alias]]
                if target_client != client:
                    try:
                        target_client.unblock(roomname)
                    except ValueError:
                        msg = Message(client.get_cid(),self.server_alias, MessageType.chat_message, 'User {} was not blocked from {}'.format(unblock_alias, roomname))
                        self.outgoing_queue.put(msg)
                    else:
                        to_target = Message(target_client.get_cid(), self.server_alias, MessageType.chat_message, 'You have been unblocked from ' + roomname)
                        to_client = Message(client.get_cid(), self.server_alias, MessageType.chat_message, '{} has been unblocked from {}'.format(unblock_alias, roomname))
                        self.outgoing_queue.put(to_target)
                        self.outgoing_queue.put(to_client)
                else:
                    msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'You cannot block yourself, dummy')
                    self.outgoing_queue.put(msg)
            except KeyError:
                msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'Could not find user ' + unblock_alias)
                self.outgoing_queue.put(msg)
        else:
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message, 'You must be moderator of this room to unblock someone from it')
            self.outgoing_queue.put(msg)

