# ScanerStudio Interface 1.6 light
# Based on S. Demmel's work
# BioPac Sync programmed by P. Proppe
# USE ONLY WITH SCANeRstudio v1.6
import os
# import math
import ctypes
import socket
import inspect

this_dir = os.path.dirname(os.path.abspath(__file__))
# to find scaner_api dll
if "1.6" in this_dir:
    print "SCANeR Version 1.6"
    os.chdir(os.path.abspath('C:/OKTAL/SCANeRstudio_1.6/APIs/bin/win32/vs2013'))
elif "1.4" in this_dir:
    print "SCANeR Version 1.4"
    os.chdir(os.path.abspath('C:/OKTAL/SCANeRstudio_1.4/APIs/bin/win32/vs2013'))
else:
    print "No SCANeR API not found"

# VARIABLES
start_of_scenario_F_command = "F1"
end_of_scenario_F_command = "F9"
from scaner import *

PORT = 49505
HOST = '172.20.22.67'

parser = ScanerApiOption()
(options, args) = parser.parse_args()
Process_InitParams(options.process_name, options.configuration, options.frequency)
# why?
# Com_registerEvent("LOAD", -1)

# register export channels to get the time
Com_registerEvent('Network/IUser/ExportChannel', -1)

status = PS_DAEMON
try:
    # create socket connection with tablet/phone
    # this is the SERVER
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print "Server running at: " + HOST
    s.listen(1)  # this is probably blocking
    sc, ipAd = s.accept()
    print 'Connection to socket is successful for ', ipAd
    old_trigger = None
    while status != PS_DEAD:
        # Process manager Run
        Process_Run()
        Process_Wait()
        # Process manager State
        old_status = status
        status = Process_GetState()
        if status != old_status:
            if (old_status == PS_RUNNING and status == PS_DAEMON):
                # this means the modules have been stopped
                print 'Closing socket due to Module stop'
                sc.close()
                s.close()
            if (old_status == PS_LOADED and status == PS_DAEMON):
                # this means the scenario has been stopped after it ran
                sc.sendall(end_of_scenario_F_command)
                print 'End of scenario detected'
            if (old_status == PS_READY and status == PS_RUNNING):
                # this means the scenario has started
                sc.sendall(start_of_scenario_F_command)
                print 'Start of scenario detected'
        if status == PS_RUNNING:
            # Event dequeing

            event = Com_getNextEvent()
            while event:
                evtType = Com_getTypeEvent(event)
                if evtType == ET_message:
                    dEventDataInterf = Com_getMessageEventDataInterface(event)
                    msg_name = Com_getMessageEventDataStringId(event)
                    if 'Network/IUser/ExportChannel' in msg_name:
                        exChanId = Com_getShortData(dEventDataInterf, 'no')
                        if exChanId == 0:
                            # we got channel 0
                            timeToExport = Com_getFloatData(dEventDataInterf, 'val')
                            toSocket = "TIME;" + str(timeToExport) + "\r\n"
                            print toSocket
                            # send to tablet/phone DISABLED
                            # sc.sendall(toSocket)
                        if exChanId == 1:
                            # we got channel 1
                            data = Com_getFloatData(dEventDataInterf, 'val')
                            if data != old_trigger:
                                # only send data if new trigger
                                toSocket = "F" + str(data)[:1]
                                # print toSocket
                                # send to tablet/phone
                                sc.sendall(toSocket)
                                old_trigger = data
                    event = Com_getNextEvent()
    # here if status is = to PS_DEAD
    # close the sockets
    print 'Status is ', (status)
    print 'Closing socket due to PS_DEAD status'
    sc.close()
    s.close()


except KeyboardInterrupt:
    print 'Keyboard interrupt'
    sc.close()
    s.close()
    Process_Close()

except:
    if 'sc' in vars():
        sc.close()
        s.close()
        Process_Close()
        raise
    print "No modules running - shutting down"