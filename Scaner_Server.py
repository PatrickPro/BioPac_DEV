import socket

# VARIABLES
PORT = 49505                                                # static port for QUT6
HOST = '192.168.0.5'

try:
    # create socket connection with client
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
    # Process_Close()

except:
    sc.close()
    s.close()
    # Process_Close()
    raise
