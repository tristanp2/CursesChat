import curses
import threading
import message
from shared.concurrent_queue import ConcurrentQueue
from datetime import datetime
from message_type import MessageType
from message import Message
from curses.textpad import Textbox, rectangle
class UI:
    def __init__(self):
        self._output_queue = ConcurrentQueue()
        self._send_queue = ConcurrentQueue()
        self.screen = curses.initscr()
        self.scr_height, self.scr_width = self.screen.getmaxyx()
        curses.noecho()

    def start_login(self):
        login_win = SubWindowWrapper(self.screen, 1, 8, 2, self.scr_width)
        login_box = ExTextbox(login_win.win)
        self.screen.addstr(1,1, 'alias: ')
        self.refresh_screen()
        login_box.edit()
        alias = login_box.gather_and_clear().strip()
        self.screen.clear()
        del login_box
        del login_win
        self.screen.addstr(1,1, 'Attempting login...')
        self.screen.refresh()
        return alias

    def end_login(self):
        self.screen.clear()

    def start_chat(self):        
        self.input_win = SubWindowWrapper(self.screen, self.scr_height - 5, 8, self.scr_height - 3, self.scr_width - 8, 1)
        self.output_win = SubWindowWrapper(self.screen, 1, self.input_win.ulx, self.input_win.uly - 3, self.input_win.lrx, 1)
        self.screen.addstr(self.input_win.uly, 1, 'Input:')
        self.screen.addstr(self.output_win.uly, 1, 'Chat: ')
        self.input_box = ExTextbox(self.input_win.win)
        self.output_box = ExTextbox(self.output_win.win, True)
        self.input_thread = threading.Thread(None, self._input_loop)
        self.input_thread.start()

    def refresh_screen(self):
        if self.screen.is_wintouched():
            self.screen.refresh()

    def get_outgoing(self):
        out_list = []
        while not self._send_queue.isEmpty():
            msg = self._send_queue.pop()
            out_list.append(msg)
        return out_list

    #this is run on its own thread
    def _input_loop(self):
        while True:
            self.refresh_screen()
            self.input_box.edit()
            msg = None
            input = self.input_box.gather_and_clear()
            if len(input) > 0:
                msg = self.parse_to_message(input)
            if msg:
                self._send_queue.push(msg)

    def process_message(self, message):
        type = message.get_type()
        if type == MessageType.chat_message:
            m_str = '{}<{}>: {}'.format(message.get_alias(), str(message.get_time())[:-7], message.get_payload())
            self._output_queue.push(m_str)
        elif type == MessageType.command:
            pass        

    def update_chat(self):
        written = False
        while not self._output_queue.isEmpty():
            written = True
            y,x = self.output_win.win.getyx()
            self.output_box.put_str(self._output_queue.pop())
        if written:
            self.input_win.focus()

    def parse_to_message(self, string):
        trimmed = string.strip()
        if(trimmed[0] == '/'):
            args = trimmed.split(' ')
            cmd = args[0]
            #check enum for cmd
            #if not in enum then reject
        else:
            msg = Message(MessageType.chat_message, trimmed, datetime.now().time())
        return msg


class ExTextbox(Textbox):
    def __init__(self, win, scroll = False, insert_mode=False):
        super().__init__(win, insert_mode)
        self._scroll = scroll
        self._reached_bottom = False

    def gather_and_clear(self):
        result = self.gather()
        self.clear()
        return result

    def edit(self):
        #hack to make textbox return on enter press
        def exit_on_enter(ch):
            if ch == curses.ascii.NL:
                return curses.ascii.BEL
            return ch
        y, x = self.win.getyx()
        self._update_max_yx()
        if self._scroll and y == self.maxy:
            self._shift_up()
        super().edit(exit_on_enter)

    def color_region(self, lx, rx, y, color):
        for x in range(lx, rx):
            ch = self.win.inch(y, x)
            self.win.addch(y, x, ch, color)
        self.win.refresh()
    def _shift_up(self):
        y, x = 1, 0
        while y < self.maxx:
            oldch = self.win.inch(y,x)
            # The try-catch ignores the error we trigger from some curses
            # versions by trying to write into the lowest-rightmost spot
            # in the window.
            try:
                if y == self.maxy:
                    self.win.addch(y,x, ' ')
                self.win.addch(y - 1, x, oldch)
            except curses.error:
                pass
            
            x += 1
            if(x == self.maxx):
                x = 0
                y += 1
        self.win.refresh()

    def put_str(self, string):
        y, x = self.win.getyx()
        if self._scroll and y == self.maxy:
            if not self._reached_bottom:
                self._reached_bottom = True
            else:
                self._shift_up()
                self.win.move(self.maxy,0)
        for ch in string:
            #newlines are inserted by superclass when line runs out, so ignore nl chars
            if ch == '\n':
                continue
            self._insert_printable_char(ch)
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
        self._parentWin = parent_win
        self.height = lry - uly
        self.width = lrx - ulx
        self.win = parent_win.subwin(self.height, self.width, uly, ulx)
        if border_margin > 0:
            try:
                curses.textpad.rectangle(parent_win, uly - border_margin, ulx - border_margin, lry + border_margin, lrx + border_margin)
            except curses.error:
                pass
    def get_parent(self):
        return self._parentWin
    def focus(self):
        y, x = self.win.getyx()
        self._parentWin.move(y + self.uly, x + self.ulx)
        self._parentWin.refresh()
    def clear(self):
        self.win.clear()