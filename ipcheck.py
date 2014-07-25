#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import urllib.request
import os.path
import os
import smtplib
import time

class IPCheck:
    def __init__(self):
        self.oldIP = None
        self.currentIP = None
        self.logFile = os.getenv('HOME') + '/.ipcheck/log'
        self.logDirectoryCheck()
        self.checkIPFile()
        self.getCurrentIP()
        self.sendIP()

    def logDirectoryCheck(self):
        if os.path.isfile(self.logFile):
            return
        else:
            try:
                os.mkdir(os.getenv('HOME') + '/.ipcheck')
            except:
                sys.exit

    def checkIPFile(self):
        if os.path.isfile('/tmp/ip.txt'):
            with open('/tmp/ip.txt', 'r') as IPFile:
                self.oldIP = IPFile.read()
        else:
            with open(self.logFile, 'a') as log:
                log.write('[WARNING] - /tmp/ip.txt does not exist. /tmp is dropped on reboot. - ' + time.asctime(time.localtime()) + '\n')
            sys.exit

    def getCurrentIP(self):
        try:
            response = urllib.request.urlopen('http://ipchicken.com')
            html = response.read()
            soup = BeautifulSoup(html)
            ip = soup.b.prettify().split('\n')
            self.currentIP = ip[1].strip()
        except:
            sys.exit

    def sendIP(self):
        if self.oldIP == (self.currentIP + '\n'):
            sys.exit
        else:
            receiver = '< enter receiving email address here >'
            sender = '< enter sending email here >'
            userpass = '< enter sending password here >'
            
            message = 'To: ' + receiver + '\n' + 'From: ' + sender + '\n' + 'Subject: New IP Address\n\n' + self.currentIP

            try:
                smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.ehlo()
                smtpObj.login(sender, userpass)
                smtpObj.sendmail(sender, receiver, message)
                smtpObj.close()
                newIPFile = open('/tmp/ip.txt', 'w')
                newIPFile.write(self.currentIP + '\n')
                newIPFile.close()
                with open(self.logFile, 'a') as log:
                    log.write('[SUCCESS] - Successfully sent IP address to ' + sender + ' - ' + time.asctime(time.localtime()) + '\n')
            except:
                try:
                    with open(self.logFile, 'a') as log:
                        log.write('[FAIL] - Failed to send IP address in email. Check code for errors - ' + time.asctime(time.localtime()) + '\n')
                except:
                    sys.exit


IPCheck()
