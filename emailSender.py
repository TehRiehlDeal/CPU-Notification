import smtplib
import imaplib
import email
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class emailSender():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connect(self):
        server = smtplib.SMTP_SSL('theriehldeal.com', 465)
        server.login(self.username, self.password)
        return server

    def createMessage(self, temp, targetTemp):
        msg = MIMEMultipart()

        msg['From'] = 'kevin@theriehldeal.com'
        msg['To'] = 'kevinriehl@gmail.com'
        msg['Subject'] = "Plex Server Overheating"
        msg.attach(MIMEText("Your Plex server is currently running at " + str(temp) +
                            " which is above your target temperature of " + str(targetTemp) + " please be advised", 'plain'))

        return msg
    
    def sendEmail(self, server, msg):        
        server.send_message(msg)

    def disconnect(self, server):
        server.quit()
