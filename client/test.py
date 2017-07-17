import sys
path = sys.argv[0].split('\\')
path = path[:-2]
path = '\\'.join(path)
path = path + '\\shared'
print(path)
sys.path.append(path)
print(sys.path)
import ui
from time import sleep
import curses
from message import Message

if __name__ == '__main__':
    # do tests
    test_ui = ui.UI()
    msg = Message()
    while True:
        if test_ui.temp_login_done:
            test_ui.process_message(msg)
        sleep(1)
    print('here')