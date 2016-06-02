# AcqKnowledge Marker Injector
# Programmed by Patrick Proppe - version 1.0
# USE ONLY WITH: Python 2.7 + https://sourceforge.net/projects/pywin32/
import win32gui, win32process, win32con
import re
import sys, socket
import win32com.client
import time


# Variables
SERVER = '172.20.43.180'
PORT = 49501

class AcqKnowledgeWindow:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None
        self._titlebar_name = None
        self._app_name = ".*AcqKnowledge -.*"
        self._shell = win32com.client.Dispatch("WScript.Shell")
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
            print "Opening AcqKnowledge Window..."
            self.restore_window()
            self.fix_ui()
        self.set_foreground()

        self._shell.AppActivate(self._handle)

    def send_f1(self):
        self.window_tasks()
        self._shell.SendKeys("{F1}")

    def send_f2(self):
        self.window_tasks()
        self._shell.SendKeys("{F2}")

    def send_f3(self):
        self.window_tasks()
        self._shell.SendKeys("{F3}")

print >> sys.stderr, 'Do not close this window while driving simulation is running!'
acq = AcqKnowledgeWindow()
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (SERVER, PORT)

try:
    print >> sys.stderr, 'Connecting to %s port %s' % server_address
    sock.connect(server_address)

    print "Connected to Simulator PC"
    while True:
        data = sock.recv(256)
        if data == "F1":
            acq.send_f1()
            print "Received:", data
        if data == "F2":
            acq.send_f2()
            print "Received:", data
        if data == "F3":
            acq.send_f3()
            print "Received:", data
except IOError:
    print >> sys.stderr, "Can't connect to server!"

finally:
    print 'Closing socket'
    sock.close()
