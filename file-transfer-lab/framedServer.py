#! /usr/bin/env python3


import sys, re, socket, os
sys.path.append("../lib")       # for params
import params

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

name = framedReceive(sock, debug)
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
    line = framedReceive(sock, debug)
    line = line + b'\n'
    line = line.decode()
    aFile.write(line)
    if debug: print("rec'd: ", line)
    if not line:
        if debug: print("child exiting")
        break 
aFile.close()
