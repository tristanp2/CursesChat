import curses
import threading
import queue
from datetime import datetime
from message_type_client import MessageType
from message_client import Message
from curses.textpad import Textbox, rectangle
import locale
code = locale.getpreferredencoding()

class UI:
    time_format = '%H:%M:%S'
    def __init__(self):
        self._output_queue = queue.Queue()
        self._send_queue = queue.Queue()
        self.screen = curses.initscr()
        self.scr_height, self.scr_width = self.screen.getmaxyx()
        self.current_room = ''
        curses.noecho()
        curses.flushinp()

    def start_login(self, address, retry = False):
        login_win = SubWindowWrapper(self.screen, 1, 8, 2, self.scr_width)
        login_box = ExTextbox(login_win.win)
        if retry:
            self.screen.clear()
            self.screen.addstr(3,1, 'Login failed. Please enter a different alias.')
        self.screen.addstr(1,1, 'alias: ')
        self.refresh_screen()
        login_box.edit()
        alias = login_box.gather_and_clear().strip()
        self.screen.clear()
        del login_box
        del login_win
        self.screen.addstr(1,1, 'Attempting to connect to: ' + address)
        self.screen.refresh()
        return alias.split(' ')[0]

    def end_login(self):
        self.screen.clear()

    def start_chat(self):
        if self.scr_width >= 115:
            self.input_win = SubWindowWrapper(self.screen, self.scr_height - 5, 8, self.scr_height - 3, self.scr_width - 30, 1)
            self.output_win = SubWindowWrapper(self.screen, 1, self.input_win.ulx, self.input_win.uly - 3, self.input_win.lrx, 1)
            self.info_win = SubWindowWrapper(self.screen, 3, self.output_win.lrx + 3, self.output_win.lry, self.scr_width - 3, 1)
            self.cname_win = SubWindowWrapper(self.screen, self.info_win.uly - 2, self.info_win.ulx, self.info_win.uly - 1, self.info_win.lrx)
        else:
            self.input_win = SubWindowWrapper(self.screen, self.scr_height - 5, 8, self.scr_height - 3, self.scr_width - 8, 1)
            self.output_win = SubWindowWrapper(self.screen, 1, self.input_win.ulx, self.input_win.uly - 3, self.input_win.lrx, 1)
            self.info_win = None
            self.cname_win = None

        self.screen.addstr(self.input_win.uly, 1, 'Input:')
        self.screen.addstr(self.output_win.uly, 1, 'Chat: ')
        self.refresh_screen()
        
        self.input_box = ExTextbox(self.input_win.win)
        self.output_box = ExTextbox(self.output_win.win, True)
        if self.info_win:
            self.info_box = ExTextbox(self.info_win.win, True)
        self.refresh_screen()
        self.input_thread = threading.Thread(None, self._input_loop)
        self.input_thread.daemon = True
        self.input_thread.start()
        curses.flushinp()
        self.refresh_screen()
    
    def do_exit(self, msg = None, wait = 3):
        if msg:
            self.screen.clear()
            self.screen.addstr(1,1,'Exiting because: {}'.format(msg))
            self.refresh_screen()
            wait = 3
            while wait > 0:
                self.screen.addstr(2,1,str(wait))
                self.refresh_screen()
                wait -= 1
                curses.napms(1000)        
        self.__exit_curses()

    def __exit_curses(self):
        if self.screen:
            self.screen.clear()
            self.refresh_screen()
        curses.echo()
        curses.endwin()

    def refresh_screen(self):
        self.screen.refresh()

    #empties the outgoing queue contents into a list
    def get_outgoing(self):
        out_list = []
        try:
            while True:
                msg = self._send_queue.get_nowait()
                out_list.append(msg)
        except queue.Empty:
            pass
        return out_list

    #this is run on its own thread
    def _input_loop(self):
        while True:
            self.refresh_screen()
            self.input_box.edit()
            msg = None
            input = self.input_box.gather_and_clear()
            if len(input) > 0:
                msg = self.parse_input(input)
            if msg:
                self._send_queue.put(msg)
    
    #Empties Messages from output_queue, processes them, and outputs relevant strings to window
    def update_chat(self):
        written = False
        while not self._output_queue.empty():
            written = True
            msg = self._output_queue.get()
            out_str = self.process_message(msg)
            if out_str:
                self.output_box.put_str(out_str)
        if written:
            self.input_win.focus()

    #does operation corresponding to message type
    #can return none or string depending on op
    def process_message(self, msg):
        type = msg.get_type()
        if type == MessageType.chat_message:
            string = '{}<{}>: {}'.format(msg.get_alias(), msg.get_time().strftime(self.time_format), msg.get_payload())
            return string
        elif type == MessageType.chatroom_update:
            #payload should be 'chatroom client1 client2....'
            payload = msg.get_payload()
            payload_list = payload.split(' ')
            cr = payload_list[0]
            if cr != self.current_room:
                self.current_room = cr
                self.output_box.clear()
            if self.info_win:
                self.cname_win.win.clear()
                self.cname_win.win.refresh()
                self.cname_win.win.addstr(payload_list[0])
                self.cname_win.win.refresh()
                payload_list = payload_list[1:]
                self.info_box.clear()
                for name in payload_list:
                    self.info_box.put_str(name)
                self.screen.refresh()
        else:
            pass
    
    def push_received(self, msg):
        self._output_queue.put(msg)

    def parse_input(self, string):
        trimmed = string.strip()
        msg = None
        if(trimmed[0] == '/'):
            args = trimmed.split(' ')
            if len(args) >= 1:
                try:
                    cmd_val = MessageType[args[0][1:]]
                except:
                    pass
                else:
                    mtype = cmd_val
                    time = None
                    if len(args)>1 and cmd_val in [MessageType.alias, MessageType.join, MessageType.create, MessageType.delete, MessageType.block, MessageType.unblock]:
                        payload = args[1]
                    else:
                        payload = ''
                    msg = Message(mtype, payload, time)
        else:
            msg = Message(MessageType.chat_message, trimmed, None)
        return msg

#Extended / hacked together version of the textbox included with python curses
#Added ability to scroll down and insert lines of text
#The enter key returns out of edit mode rather than ctrl-g in the original
class ExTextbox(Textbox):
    def __init__(self, win, scroll = False, insert_mode=False):
        super().__init__(win, insert_mode)
        self._scroll = scroll
        self._reached_bottom = False

    def gather_and_clear(self):
        result = self.gather()
        self.clear()
        return result

    #this exists in windows version of python curses, but not linux
    #so it is reimplemented here
    def _update_max_yx(self):
        maxy, maxx = self.win.getmaxyx()
        self.maxy = maxy - 1
        self.maxx = maxx - 1

    def edit(self):
        #hackish to make textbox return on enter press
        def exit_on_enter(ch):
            if ch == curses.ascii.NL:
                return curses.ascii.BEL
            return ch
        y, x = self.win.getyx()
        self._update_max_yx()
        if self._scroll and y == self.maxy:
            self._shift_up()
        super().edit(exit_on_enter)

    def _shift_up(self):
        y, x = 1, 0
        while y < self.maxx:
            oldch = self.win.inch(y,x)
            # The try-catch ignores the error we trigger from some curses
            # versions by trying to write into the lowest-rightmost spot
            # in the window.
            # Linux version seems to also throw overflowerrors, for reasons unknown
            try:
                if y == self.maxy:
                    self.win.addch(y,x, ' ')
                self.win.addch(y - 1, x, oldch)
            except (curses.error, OverflowError):
                pass
            
            x += 1
            if(x == self.maxx):
                x = 0
                y += 1
        self.win.refresh()

    def put_str(self, string, newline = True):
        string_enc = string.encode()
        y, x = self.win.getyx()
        if self._scroll and y == self.maxy:
            if not self._reached_bottom:
                self._reached_bottom = True
            else:
                self._shift_up()
                self.win.move(self.maxy,0)
        for ch in string_enc:
            #newlines are inserted by superclass when line runs out, so ignore nl chars
            if ch == '\n':
                continue
            self._insert_printable_char(ch)
        if(newline):
            self._insert_printable_char(curses.ascii.NL)
        self.win.refresh()

    def focus_cursor(self):
        self.win.move(self._y, self._x)

    def clear(self):
        self.win.erase()
        self.win.refresh()
    

#wrapper class to allow easier creation and handling of curses subwindows
class SubWindowWrapper:
    #Params:
    #uly, ulx: upper left coords
    #lry, lrx: lower right coords
    def __init__(self, parent_win, uly, ulx, lry, lrx, border_margin = 0):
        self.ulx = ulx
        self.uly = uly
        self.lrx = lrx
        self.lry = lry
        self.__parentWin = parent_win
        self.height = lry - uly
        self.width = lrx - ulx
        self.win = parent_win.subwin(self.height, self.width, uly, ulx)
        if border_margin > 0:
            try:
                curses.textpad.rectangle(parent_win, uly - border_margin, ulx - border_margin, lry + border_margin, lrx + border_margin)
            except curses.error:
                pass

    def get_parent(self):
        return self.__parentWin

    def focus(self):
        y, x = self.win.getyx()
        self.__parentWin.move(y + self.uly, x + self.ulx)
        self.__parentWin.refresh()

    def clear(self):
        self.win.clear()

if __name__ ==  '__main__':
    msg = Message(MessageType.chat_message, 'hello', datetime.now(), 'joe')
    ui = UI()
    print(ui.process_message(msg))
