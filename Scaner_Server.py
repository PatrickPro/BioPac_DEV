import socket, sys, time
from socket import error as SocketError
import errno
import select


# VARIABLES
PORT = 49501
HOST = None
connection = None
s = None


class AcqServer:

    def __init__(self):
        self.s = None
        self.connection = None

    def stopServer(self):
        if self.s is not None:
            self.s.close
            self.__init__()


    def sendStart(self):
        if self.connection is not None:
            self.connection.sendall("F1")
            self.connection.sendall("F1")
            self.connection.sendall("F1")

    def sendEnd(self):
        if self.connection is not None:
            self.connection.sendall("F3")
            self.connection.sendall("F3")
            self.connection.sendall("F3")

    def sendEvent(self):
        if self.connection is not None:
            self.connection.sendall("F2")
            self.connection.sendall("F2")
            self.connection.sendall("F2")


    def startServer(self):
        try:
            # Lookup local IP address
            HOST = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
            if HOST is not None:
                self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind((HOST,PORT))
                print 'Waiting for connection on ', HOST, ":", PORT
                self.s.listen(1)                         # this is probably blocking
                # Wait for a connection
                self.connection, client_address = self.s.accept()
                print 'Connection from', client_address
                # Control variables.


            else:
                print >> sys.stderr, 'No local IP Address found!'
        except KeyboardInterrupt:
            self.s.close()

        except:
            self.s.close()
            raise

server = AcqServer()
server.startServer()

for x in range(0,55,1):
    print x%2
    if x%2 is 0:
        server.sendStart()
    else:
        server.sendEnd()
    time.sleep(0.5)


server.stopServer()


