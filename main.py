import subprocess
import time
import datetime
import credentials
import os, platform
from emailSender import emailSender

targetTemp = 80.0

thisOS = os.name
thisPlatform = platform.system()

email = emailSender(credentials.username, credentials.password)

def runCommand(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = p.stdout.readline()
    p.kill()
    return stdout.decode('utf-8')

def getTemp(cmd, startChar, endChar):
    output = runCommand(cmd)
    temp = output[startChar:endChar]
    return temp

emailSent = False

while True:
    if (thisPlatform == "Darwin"):
        cmd = "iStats | grep -E 'CPU temp:'"
        temp = getTemp(cmd, 24, 28)
    elif (thisPlatform == "Linux"):
        cmd = "sensors | grep -E 'Package id 0'"
        temp = getTemp(cmd, 16, 20)
    elif (thisPlatform == "Windows"):
        #Not Implimented yet
        cmd = ""

    #readEmails()
    if (float(temp) > targetTemp and emailSent is False):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, sending email! " + temp))
        server = email.connect()
        email.sendEmail(server, email.createMessage(temp, targetTemp))
        email.disconnect(server)
        emailSent = True
    elif (float(temp) > targetTemp and emailSent is True):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, email has been sent " + temp))
    else:
        print(datetime.datetime.now().strftime("%c \n\t Everythings fine. CPU at: " + temp))
    time.sleep(5)
