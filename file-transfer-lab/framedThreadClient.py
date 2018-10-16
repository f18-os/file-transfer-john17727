#! /usr/bin/env python3

import socket, sys, re
import params
from framedSock import FramedStreamSock
from threading import Thread, Lock
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       mutex.acquire()
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fileSend = FramedStreamSock(s, debug=debug)
       while True:
           fileName = input("What is the name of the file? (Use extensions): ")
           try:
               readFile = open(fileName, "r")
               break
           except FileNotFoundError as fileError:
               print(fileError)
               print("Please try again.")

       fileName = fileName.encode()
       fileSend.sendmsg(fileName)
       for line in readFile:
           line = line.strip()
           line = line.encode()
           fileSend.sendmsg(line)
       readFile.close()
       mutex.release()

mutex = Lock()
for i in range(2):
    ClientThread(serverHost, serverPort, debug)

