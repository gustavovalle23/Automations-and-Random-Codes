#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Gustavo Valle
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



# Send email with function
def sendEmail(yourEmail, password, toEmail, subject, yourMessage):
    message = MIMEMultipart()

    message['From'] = yourEmail
    message['To'] = toEmail
    message['Subject'] = subject

    message.attach(MIMEText(yourMessage, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    server.login(message['From'], password)
    server.sendmail(message['From'], message['To'], message.as_string())
    server.quit()


sendEmail('YourEmail', 'YourPassword', 'DestinationEmail', 'Subject', 'Message')



# Send email with class
class Email(object):
    def __init__(self, yourEmail, password):
        self.__yourEmail = yourEmail
        self.__password = password

    def sendEmal(self, toEmail, subject, yourMessage):
        message = MIMEMultipart()

        message['From'] = self.__yourEmail
        message['To'] = toEmail
        message['Subject'] = subject

        message.attach(MIMEText(yourMessage, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        server.login(message['From'], self.__password)
        server.sendmail(message['From'], message['To'], message.as_string())
        server.quit()


myEmail = Email('YourEmail', 'YourPassword')
myEmail.sendEmal('DestinationEmail', 'SubjectEmail', 'MessageEmail')

