import socket
from enum import Enum
from datetime import datetime.time

class MessageType(Enum):
    command = 1
    chat_message = 2

class Message:
    _type = MessageType()
    _payload = []
    _timestamp = datetime().time

    def create_message(type, payload, timestamp):

    def __init__(self):

class Queue:
    #__lock_object = True

    def push(message):

    def send_message(message):


class MessageHandler:
    __sox = socket.socket()
    q = Queue()

    def pop_message():

    def receive_message():

    def peek_message():

class Messenger:
    __sox = new socket.socket()
    q = Queue()


    def pushMSG():

    def __sengMSG():


class Client:

    __sox = new socket.socket()
    __messenger = Messenger()
    __message_handler = MessageHandler()


    def main_loop():

    def io_loop():

    def init_thread():


    print("Hello from client.")

    def __init__():

class UI:
    __keycode = 1234;

    def __process_MSG(message):

    def __parse(string):

    def __on_key_down(keycode):
