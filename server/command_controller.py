from chatroom import Chatroom
from message import Message

class CMDcontroller:

    def __init__(self):
        pass
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


    def proccessCMD(self, command):
        pass

        #TODO: parse the message

        #TODO: push it to the recieve queue

    def login(self, name, client):
        client.set_alias(name)

    def logout(self):
        pass

    def list_cmd(self):
        # print options.values()?
        pass

    def leave_chatroom(self, client, chatroom_dict, cid_to_sock_dict):
        #client can't leave main chatroom
        if client.get_chatroom() == 'main_chatroom':
            msg = Message(client.get_cid(), client.get_alias(), 1 ,"sorry you can not leave main chatroom")
            outgoing_list.append(msg)
        #if client is creator
        lonely_chatroom = client.get_chatroom()
        if client == chatroom_dict[lonely_chatroom].get_moderator():
            #kick everyone out
            abandoned_crying_babies = chatroom_dict[lonely_chatroom].get_cid_list()
            chatroom_dict['main_chatroom'].add_client_list(abandoned_crying_babies)
            client_list = [cid_to_sock_dict[k] for k in abandoned_crying_babies()]
            map(lambda x: x.set_chatroom('main_chatroom'), client_list)
            del chatroom_dict[lonely_chatroom]
            return True
        #if client is not creator
        else:
            lonely_chatroom.remove_client(client.get_cid())
            chatroom_dict['main_chatroom'].add_client(client.get_cid())
            client.set_chatroom('main_chatroom')
            return True

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def join_chatroom(self):
        pass


    def create_chatroom(self, name, client, chatroom_dict):
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

