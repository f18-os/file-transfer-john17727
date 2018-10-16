#! /usr/bin/env python3

import sys, os, socket, params, time
from threading import Thread, Lock
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
        mutex.acquire()
        name = self.fsock.receivemsg()
        name = name.decode()
        name = name[:-4]
        name = name + "-server.txt"
        if os.path.isfile(name):
            name = name[:-4]
            name = name + "(1).txt"
            count = 2;
            while os.path.isfile(name):
                name = name[:-7]
                name = name + "(" + str(count) + ").txt"
                count += 1

        aFile = open(name,"w")
        while True:
            line = self.fsock.receivemsg()
            line = line + b'\n'
            line = line.decode()
            aFile.write(line)
            if debug: print("rec'd: ", line)
            if not line:
                if debug: print("child exiting")
                break 
        aFile.close()
        mutex.release()

mutex = Lock()
while True:
    sock, addr = lsock.accept()
    ServerThread(sock, debug)

