# ScanerStudio Interface 1.4 light
# Programmed by S. Demmel -- version 1.0
# USE ONLY WITH SCANeRstudio v1.4
import os
#import math
import ctypes
import socket

# VARIABLES
os.chdir(os.path.abspath('../../../bin/win32/vs2013'))      # to find scaner_api dll --change for the position in SUPERVISOR
from scaner import *
PORT = 49505                                                # static port for QUT6
HOST = '192.168.0.5'
# HOST = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

parser = ScanerApiOption()
(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, options.frequency)
# why?
#Com_registerEvent("LOAD", -1)

# register export channels to get the time
Com_registerEvent('Network/IUser/ExportChannel', -1)

status = PS_DAEMON
try:
    # create socket connection with tablet/phone
    # this is the SERVER
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    print HOST
    s.listen(1)                         # this is probably blocking
    sc,ipAd = s.accept()
    print 'Connection to socket is successful for ', ipAd
    while status != PS_DEAD:
        # Process manager Run
        Process_Run()
        Process_Wait()
        #Process manager State
        old_status = status
        status = Process_GetState()
        if status != old_status:
            print state_string(status)
            if (old_status == PS_RUNNING and status == PS_DAEMON):
                # this means the scenario has been stopped after it ran
                print 'Closing socket due to end of scenario'
                sc.close()
                s.close()
        if status == PS_RUNNING:
            # Event dequeing
            event = Com_getNextEvent()
            while event:
                evtType = Com_getTypeEvent(event)
                if evtType == ET_message:
                    dEventDataInterf = Com_getMessageEventDataInterface(event)
                    msg_name = Com_getMessageEventDataStringId(event)
                    if 'Network/IUser/ExportChannel' in msg_name:
                        exChanId = Com_getShortData(dEventDataInterf,'no')
                        if exChanId == 0:
                            # we got channel 0
                            timeToExport = Com_getFloatData(dEventDataInterf,'val')
                            toSocket = "TIME;" + str(timeToExport) + "\r\n"
                            print toSocket
                            # send to tablet/phone
                            sc.sendall(toSocket)
                        if exChanId == 1:
                            # we got channel 1
                            data = Com_getFloatData(dEventDataInterf,'val') # needs to be another com_getInt or String
                            toSocket = None
                            if data is 1:
                                toSocket = "F1"
                            elif data is 2:
                                toSocket = "F2"
                            elif data is 3:
                                toSocket = "F3"

                            if toSocket is not None:
                                # send to client
                                sc.sendall(toSocket)
                    event = Com_getNextEvent()
    # here if status is = to PS_DEAD
    # close the sockets
    print 'Status is ', state_string(status)
    print 'Closing socket due to PS_DEAD status'
    sc.close()
    s.close()


except KeyboardInterrupt:
    print 'Keyboard interrupt'
    sc.close()
    s.close()
    Process_Close()

except:
    sc.close()
    s.close()
    Process_Close()
    raise
