import subprocess
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime
import ./credentials/credentials

targetTemp = 80.0


def runCommand(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = p.stdout.readline()
    p.kill()
    return stdout.decode('utf-8')


def sendEmail(temp, targetTemp):
    server = smtplib.SMTP_SSL('theriehldeal.com', 465)
    server.login(username, password)
    msg = MIMEMultipart()

    msg['From'] = 'kevin@theriehldeal.com'
    msg['To'] = 'kevinriehl@gmail.com'
    msg['Subject'] = "Plex Server Overheating"
    msg.attach(MIMEText("Your Plex server is currently running at " + str(temp) +
                        " which is above your target temperature of " + str(targetTemp) + " please be advised", 'plain'))
    server.send_message(msg)
    server.quit()


cmd = "sensors | grep -E 'Package id 0'"

emailSent = False

while True:
    output = runCommand(cmd)
    temp = output[16:20]

    if (float(temp) > targetTemp and emailSent is False):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, sending email! " + temp))
        sendEmail(temp, targetTemp)
        emailSent = True
    elif (float(temp) > targetTemp and emailSent is True):
        print(datetime.datetime.now().strftime("%c \n\t Server Overheating, email has been sent " + temp))
    else:
        print(datetime.datetime.now().strftime("%c \n\t Everythings fine. CPU at: " + temp))
    time.sleep(5)
