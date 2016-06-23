# AcqKnowledge Marker Injector
# Programmed by P. Proppe - version 1.0
# USE ONLY WITH: Python 2.7 + https://sourceforge.net/projects/pywin32/
import win32gui, win32process, win32con
import re
import sys, socket
import win32com.client
import time
import select

# Variables
SERVER = '172.20.22.67'
PORT = 49505

class AcqKnowledgeWindow:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None
        self._titlebar_name = None
        self._app_name = ".*AcqKnowledge -.*"
        self._shell = win32com.client.Dispatch("WScript.Shell")
        self._shell.SendKeys('%')
        self.find_window_wildcard(self._app_name)  # see if app is running
        if self._handle == None:
            print '\033[91m' + "Can't find AcqKnowledge Software - not recording?"
            print '\033[91m' + '\033[1m' + "Script execution stopped!"
            raise SystemExit()

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd
            self._titlebar_name = str(win32gui.GetWindowText(hwnd))

    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def restore_window(self):
        win32gui.ShowWindow(self._handle, win32con.SW_RESTORE)

    def fix_ui(self):
        """fix for AcqKnowledge UI not being visible after restoring from minimized status"""
        x0, y0, x1, y1 = win32gui.GetWindowRect(self._handle)
        w = x1 - x0
        h = y1 - y0
        win32gui.MoveWindow(self._handle, x0, y0, w + 1, h + 1, True)

    def window_tasks(self):
        """Combines necessary tasks for SendKeys function"""
        if self._handle != win32gui.GetForegroundWindow():
            #print "not in foreground"
            self.restore_window()
            self.fix_ui()
        self.set_foreground()

        self._shell.AppActivate(self._handle)

    def send_start_f1(self):
        self.window_tasks()
        self._shell.SendKeys("{F1}")

    def send_event_f2(self):
        self.window_tasks()
        self._shell.SendKeys("{F2}")

    def send_event_f3(self):
        self.window_tasks()
        self._shell.SendKeys("{F3}")

    def send_event_f4(self):
        self.window_tasks()
        self._shell.SendKeys("{F4}")

    def send_event_f5(self):
        self.window_tasks()
        self._shell.SendKeys("{F5}")

    def send_event_f6(self):
        self.window_tasks()
        self._shell.SendKeys("{F6}")

    def send_event_f7(self):
        self.window_tasks()
        self._shell.SendKeys("{F7}")

    def send_event_f8(self):
        self.window_tasks()
        self._shell.SendKeys("{F8}")

    def send_end_f9(self):
        self.window_tasks()
        self._shell.SendKeys("{F9}")

    def do_nothing(self):
        pass

acq = AcqKnowledgeWindow()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (SERVER, PORT)
print >> sys.stderr, 'Connecting to %s port %s' % server_address
sock.connect(server_address)
print >> sys.stderr, "Success!"
while True:
    try:
        ready_to_read, ready_to_write, in_error = \
            select.select([sock,], [sock,], [], 5)
    except select.error:
        sock.shutdown(2) # 0 = done receiving, 1 = done sending, 2 = both
        sock.close()
        # connection error event here, maybe reconnect
        print 'connection error'
        break
    if len(ready_to_read) > 0:
        data = sock.recv(256)
        if data == "":
            print >> sys.stderr, 'Connection to Simulator PC terminated!'
            print >> sys.stderr, 'Stopping...'
            break
        # do stuff with received data
        print "Received:", data

        if "F0" in data:
            # F0 command signals start of scenario
            acq.send_start_f1()
        if "F1" in data:
            # F1 command signals start_trigger (if present)
            acq.send_start_f1()
        elif "F2" in data:
            acq.send_event_f2()
        elif "F3" in data:
            acq.send_event_f3()
        elif "F4" in data:
            acq.send_event_f4()
        elif "F5" in data:
            acq.send_event_f5()
        elif "F6" in data:
            acq.send_event_f6()
        elif "F7" in data:
            acq.send_event_f7()
        elif "F8" in data:
            acq.send_event_f8()
        elif "F9" in data:
            # F9 command signals end of scenario
            acq.send_end_f9()