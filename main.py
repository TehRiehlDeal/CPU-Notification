import subprocess
import smtplib, imaplib
import email
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime
import credentials
import os, platform

targetTemp = 80.0

thisOS = os.name
thisPlatform = platform.system()

def runCommand(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = p.stdout.readline()
    p.kill()
    return stdout.decode('utf-8')


def sendEmail(temp, targetTemp):
    server = smtplib.SMTP_SSL('theriehldeal.com', 465)
    server.login(credentials.username, credentials.password)
    msg = MIMEMultipart()

    msg['From'] = 'kevin@theriehldeal.com'
    msg['To'] = 'kevinriehl@gmail.com'
    msg['Subject'] = "Plex Server Overheating"
    msg.attach(MIMEText("Your Plex server is currently running at " + str(temp) +
                        " which is above your target temperature of " + str(targetTemp) + " please be advised", 'plain'))
    server.send_message(msg)
    server.quit()

def getTemp(cmd, startChar, endChar):
    output = runCommand(cmd)
    temp = output[startChar:endChar]
    return temp

def readEmails():
    server = imaplib.IMAP4_SSL('theriehldeal.com', 993)
    server.login(credentials.username, credentials.password)
    server.select('inbox')

    result, data = server.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id, first_email_id, -1):
        result, data = server.fetch(str(i), '(RFC822)')

        print(data)                

if (thisPlatform == "Darwin"):
    cmd = "iStats | grep -E 'CPU temp:'"
    temp = getTemp(cmd, 24, 29)
elif (thisPlatform == "Linux"):
    cmd = "sensors | grep -E 'Package id 0'"
    temp = getTemp(cmd, 16, 20)
elif (thisPlatform == "Windows"):
    #Not Implimented yet
    cmd = ""

emailSent = False

while True:
    if (float(temp) > targetTemp and emailSent is False):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, sending email! " + temp))
        sendEmail(temp, targetTemp)
        emailSent = True
    elif (float(temp) > targetTemp and emailSent is True):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, email has been sent " + temp))
    else:
        print(datetime.datetime.now().strftime("%c \n\t Everythings fine. CPU at: " + temp))
    time.sleep(5)
