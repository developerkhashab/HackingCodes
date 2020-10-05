#!usr/bin/env python3

import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.4", 4444))
connection.send(b"the target machine is sending a message")

recieved_data = connection.recv(1024)
print(recieved_data)
connection.close()
