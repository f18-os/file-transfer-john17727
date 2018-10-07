# File Transfer Lab

Included are:
* framedClient.py
* framedServer.py
* framedForkServer.py
* framedSock.py
* pycache folder - Put that in there just to be safe.
* testFile.txt - A file to test the program with. Can make your own but has to be in the same directory.

## framedClient.py
Asks for the name of a file to transfer to server. File must be in the same directory.
```python
while True:
    fileName = input("What is the name of the file? (Use extensions): ")
    try:
        readFile = open(fileName, "r")
        break
    except FileNotFoundError as fileError:
        print(fileError)
        print("Please try again.")

fileName = fileName.encode()
framedSend(s, fileName, debug)
for line in readFile:
    line = line.strip()
    line = line.encode()
    framedSend(s, line, debug)
readFile.close()
```

## framedServer.py
Gets the name of the file to be transferred and checks if it is already on the server side. If there is one the server makes copy of the new one and its contents. The name of the file saved by the server will be appended with *-server* to differentiate it from the original file. Gives an error because it thinks the variable payload is a nontype but it's of type bytes, so it decodes it to a string none the less. I couldn't get rid of the error for the life of me but the program still works.
```python
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
```

## framedForkServer.py
Same as *framedServer.py* but with forking. Gives same error.
```python
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
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
                sys.exit(0)  
        aFile.close()
```

## framedSock.py
This is the origianl program provided. Nothing has been modified.