# -*- coding: utf-8; encoding: utf-8; -*-;
"""
mailto.py

http://labs.unoh.net/2007/06/python_2.html

Known issue:
    - need some change for exceptions
"""
__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__   = "21 Nov. 2008"
__credits__ = "0x7d8 -- programming training"
__version__ = "$Revision: 0.10"

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

class MailTo:
    """
    class for sending e-mail
    """
    def __init__(self, from_addr = '', to_addr = [], subject = '', body = ''):
        """
        initialization

        arguments:
            from_addr : 'From' address
            to_addr : list of 'To' addresses
            subject : subject of the e-mali
            body : body of the e-mail
        """
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.body = body

    def CreateMessage(self, encoding):
        """
        create e-mail message including e-mail header

        arguments:
            encoding : mail encoding

        return:
            e-mail message
        """
        msg = MIMEText(self.body, 'plain', encoding)
        msg['Subject'] = self.subject
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr
        msg['Date'] = formatdate()
        return msg

    def Send(self, msg):
        """
        send e-mail using normal smtp server

        arguments:
            msg : e-mail message created by CreateMessage()
        """
        s = smtplib.SMTP()
        s.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        s.close()

    def SendViaGmail(self, msg, account, password):
        """
        send e-mail using Gmail

        arguments:
            msg : e-mail message created by CreateMessage()
            account : Gmail account
            password : password for Gmail account
        """
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(account, password)
        s.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        s.close()

