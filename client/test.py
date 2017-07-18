import sys
import os
#path = sys.argv[0].split('\\')
path = os.path.abspath(__file__)
path = path.split('\\')
path = path[:-2]
path = '\\'.join(path)
path = path + '\\shared'
sys.path.append(path)
import ui
from time import sleep
import curses
from message import Message


if __name__ == '__main__':
    # do tests
    test_ui = ui.UI()
    msg = Message()
    elapsed = 0
    delta = 30
    while True:
        if elapsed > 1000:
            elapsed = 0
            test_ui.process_message(msg)
        test_ui.update_chat()
        elapsed += delta
        curses.napms(delta)
