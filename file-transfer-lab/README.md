# File Transfer Lab

## framedClient.py
Asks for the name of a file to transfer to server. File must be in the same directory.
```python
fileName = input("What is the name of the file? (Use extensions): ")
aFile = open(fileName, "r")
for line in aFile:
    line = line.strip()
    line = line.encode('utf-8')
    framedSend(s, line, debug)
aFile.close()
```

## framedServer.py
Gets the information of a file from the socket and saves it as a new file. The name of the file will be *file-server.txt* to differentiate it form the original file.
```python
aFile = open("file-server.txt","w")
while True:
    payload = framedReceive(sock, debug)
    payload = payload + b'\n'
    aFile.write(payload.decode())
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    '''
    payload += b"!"             # make emphatic!
    framedSend(sock, payload, debug)
    '''
aFile.close()
```

## framedForkServer.py
Same as *framedServer.py* but with forking.
```python
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        aFile = open("file-server.txt","w")
        while True:
            payload = framedReceive(sock, debug)
            payload = payload + b'\n'
            aFile.write(payload.decode())
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)  
            '''
            framedSend(sock, payload, debug)
            '''
        aFile.close()
```

## framedSock.py
This is the origianl program provided. Nothing has been modified.