from chatroom import Chatroom
from message import Message
from message_type import MessageType

class CMDcontroller:

    def __init__(self, client_dict, chatroom_dict):
        self.chatroom_dict = chatroom_dict
        self.client_dict = client_dict
        self.outgoing_list = []
    #    self.chatroom = Chatroom()

    def isPermitted(self, client):
        pass

    #alias messagetype payload
    #tristan 1 how are you

    def parse_input(self, message):
        args = message.split(' ')
        alias = args[0]
        type = args[1]
        payload = args[2:]
        #TODO: add cid as first parameter
        msg = Message(alias, type, payload)
        #TODO: push to receive queue, so we dont need to return msg
        return msg


    def process_message(self, msg):
        type = msg.type

        if type == MessageType.alias:
            pass
        elif type == MessageType.block:
            self.block_user()
        elif type == MessageType.create:
            client = msg.alias
            name = msg.payload
            self.create_chatroom(name,client)
        elif type == MessageType.delete:
            self.delete_chatroom()
        elif type == MessageType.join:
            self.join_chatroom()
        elif type == MessageType.leave:
            client = self.client_dict[msg.cid]
            self.leave_chatroom(client)
        elif type == MessageType.help:
            self.help(self.client_dict[msg.cid])
        elif type == MessageType.login:
            self.login(msg.alias, client)

    def get_outgoing(self):
        outgoing_copy = self.outgoing_list.copy()
        self.outgoing_list.clear()
        return outgoing_copy

    def login(self, name, client):
        client.set_alias(name)

    def logout(self):
        pass

    def help(self, client):
        # print options.values()?
        help_list = []
        restricted = [MessageType.chat_message.name, MessageType.chatroom_update.name, MessageType.start_server.name, MessageType.stop_server.name]
        for value in MessageType:
            if value.name not in restricted:
                help_list.append(value.name)
        payload = ' '.join(help_list)
        msg = Message(client.alias, MessageType.help, payload)
        self.outgoing_list.append(msg)

    def leave_chatroom(self, client, chatroom_dict, cid_to_sock_dict):
        #client can't leave main chatroom
        if client.get_chatroom() == 'main_chatroom':
            m = "sorry you can not leave main chatroom"
            msg = Message(client.get_cid(), client.get_alias(), 10, m)
            outgoing_list.append(msg)
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
                    msg = Message(client.get_cid(), client.get_alias(), 10, m)
                    outgoing_list.append(msg)
            #if client is not creator
            else:
                lonely_chatroom.remove_client(client.get_cid())
                chatroom_dict['main_chatroom'].add_client(client.get_cid())
                m = "{} left {} and join main_chatroom".format(client.get_alias(), lonely_chatroom)
                msg = Message(client.get_cid(), client.get_alias(), 10, m)
                outgoing_list.append(msg)



    def start_server(self):
        pass

    def stop_server(self):
        pass

    def join_chatroom(self):
        pass


    def create_chatroom(self, name, client):
        chatroom_dict[name] = Chatroom(name)
        chatroom_dict.set_moderator(client)
        chatroom_dict.add_client(client.get_cid())

    def delete_chatroom(self):
        pass

    def set_alias(self):
        pass

    def block_user(self):
        pass

    def unblock_user(self):
        pass

