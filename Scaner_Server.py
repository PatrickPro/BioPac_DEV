import socket, sys
# create socket connection with client
#  this is the SERVER


# VARIABLES
PORT = 49504                                                # static port for QUT6
HOST = None

try:


    # Lookup local IP address
    HOST = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    if HOST is not None:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        print 'Waiting for connection on ', HOST, ":", PORT
        s.listen(1)                         # this is probably blocking
        ipAd = s.accept()
        print 'Connection to socket is successful for ', ipAd
    else:
        print >> sys.stderr, 'No local IP Address found!'







except KeyboardInterrupt:
    s.close()

except:
    s.close()
    raise

finally:
    # close the sockets
    print 'Closing socket'
    s.close()