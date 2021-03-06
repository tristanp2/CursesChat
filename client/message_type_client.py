from enum import Enum
class MessageType(Enum):
    chat_message =  1
    alias = 2
    block = 3
    help = 4
    login = 5
    logout = 6
    create = 7
    delete = 8
    join = 9
    leave = 10
    start_server = 11
    stop_server = 12
    quit = 13
    chatroom_update = 14
    refuse = 15
    unblock = 16