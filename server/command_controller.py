from chatroom import Chatroom
from message import Message
from message_type import MessageType
import queue
import copy

class CMDcontroller:

    def __init__(self, client_dict, chatroom_dict):
        self.chatroom_dict = chatroom_dict
        self.client_dict = client_dict
        self.outgoing_queue = queue.Queue()
        self.server_alias = 'server'

    def isPermitted(self, client):
        pass

    def process_message(self, msg):
        type = msg.type
        client = self.client_dict[msg.cid]

        if type == MessageType.alias:
            self.set_alias(client, msg.payload)
        elif type == MessageType.chat_message:
            self.chat_message(client, msg)
        elif type == MessageType.block:
            self.block_user()
        elif type == MessageType.create:
            name = msg.payload
            self.create_chatroom(name,client)
        elif type == MessageType.delete:
            self.delete_chatroom()
        elif type == MessageType.join:
            self.join_chatroom()
        elif type == MessageType.leave:
            self.leave_chatroom(client)
        elif type == MessageType.help:
            self.help(client)
        elif type == MessageType.login:
            self.login(msg.alias, client)

    def pop_outgoing(self):
        return self.outgoing_queue.get()

    def login(self, alias, client):
        self.set_alias(client, alias)
        cr = self.chatroom_dict['main_chatroom']
        self.__do_chatroom_update(cr)

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
        restricted = [MessageType.chat_message.name, MessageType.chatroom_update.name, MessageType.start_server.name, MessageType.stop_server.name]
        for value in MessageType:
            if value.name not in restricted:
                help_list.append(value.name)
        payload = ' '.join(help_list)
        msg = Message(client.get_cid(), client.get_alias(), MessageType.help, payload)
        self.outgoing_queue.append(msg)

    def leave_chatroom(self, client, reply = False):
        #client can't leave main chatroom
        if reply and client.get_chatroom() == 'main_chatroom':
            msg = Message(client.get_cid(), self.server_alias, MessageType.chat_message,"sorry you can not leave main chatroom")
            outgoing_list.append(msg)
        #if client is creator
        lonely_chatroom = client.get_chatroom()
        if client == self.chatroom_dict[lonely_chatroom].get_moderator():
            #kick everyone out
            abandoned_crying_babies = chatroom_dict[lonely_chatroom].get_cid_list()
            chatroom_dict['main_chatroom'].add_client_list(abandoned_crying_babies)
            client_list = [cid_to_sock_dict[k] for k in abandoned_crying_babies()]
            map(lambda x: x.set_chatroom('main_chatroom'), client_list)
            del self.chatroom_dict[lonely_chatroom]
            return True
        #if client is not creator
        else:
            #if client is creator
            lonely_chatroom = client.get_chatroom()
            if client == chatroom_dict[lonely_chatroom].get_moderator():
                #kick everyone out
                abandoned_crying_babies = chatroom_dict[lonely_chatroom].get_cid_list()
                chatroom_dict['main_chatroom'].add_client_list(abandoned_crying_babies)
                client_list = [cid_to_sock_dict[k] for k in abandoned_crying_babies()]
                map(lambda x: x.set_chatroom('main_chatroom'), client_list)
                del chatroom_dict[lonely_chatroom]
                for c in client_list:
                    m = "{} left {} and join main_chatroom".format(c.get_alias(), lonely_chatroom)
                    msg = Message(client.get_cid(), client.get_alias(), MessageType.leave, m)
                    outgoing_list.append(msg)
            #if client is not creator
            else:
                lonely_chatroom.remove_client(client.get_cid())
                chatroom_dict['main_chatroom'].add_client(client.get_cid())
                m = "{} left {} and join main_chatroom".format(client.get_alias(), lonely_chatroom)
                msg = Message(client.get_cid(), client.get_alias(), MessageType.leave, m)
                outgoing_list.append(msg)


    def chat_message(self, client, msg):
        chatroom = self.chatroom_dict[client.get_chatroom()]
        self.__broadcast_data(msg, chatroom.client)

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def join_chatroom(self, client, chatroom_name):
        old_chatroom = self.chatroom_dict[client.get_chatroom()]
        self.leave_chatroom(client)
        chatroom = self.chatroom_dict[chatroom_name]
        chatroom.add_client(client.get_cid())
        client.set_chatroom(chatroom.get_name())
        self.__do_chatroom_update(chatroom)
        self.__do_chatroom_update(old_chatroom)

    #Creates and pushes update messages for everyone in chatroom   
    def __do_chatroom_update(self, chatroom):
        alias_list = list(map(lambda x: self.client_dict[x].get_alias(), chatroom.client))
        payload = chatroom.get_name() + ' ' + ' '.join(alias_list)
        for cid in chatroom.client:
            cli = self.client_dict[cid]
            msg = Message(cli.get_cid(), cli.get_alias(), MessageType.chatroom_update, payload)
            self.outgoing_queue.put(msg)

    def create_chatroom(self, name, client):
        chatroom_dict[name] = Chatroom(name)
        chatroom_dict.set_moderator(client)
        chatroom_dict.add_client(client.get_cid())

    def delete_chatroom(self):
        pass

    def set_alias(self, client, alias):
        client.set_alias(alias)
        msg = Message(client.get_cid(), client.get_alias(), MessageType.alias, client.get_alias())

    def block_user(self):
        pass

    def unblock_user(self):
        pass

