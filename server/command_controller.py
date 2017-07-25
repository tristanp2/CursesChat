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

        def login(arg):
            pass

        def logout(arg):
            pass

        def list_cmd():
            # print options.values()?
            pass

        def leave_chatroom(arg):
            pass

        def start_server(arg):
            pass

        def stop_server(arg):
            pass

        def join_chatroom(arg):
            pass

        def create_chatroom(arg):
            name = arg


        def delete_chatroom(arg):
            pass

        def set_alias(arg):
            pass

        def block_user(arg):
            pass

        def unblock_user(arg):
            pass

