# Copyright (c) 2022, Kirill Rudenko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#   Inner SMPT module
#
from base import LoggerFactory, JsonConf
from os import remove, getcwd
import smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email(object):
  """
  Class for reporting data via email once job is finished
  """
  def __init__(self):
    self.CONF = JsonConf(getcwd()+'\\user_conf.json')
    self.REPORT_CONF = JsonConf(getcwd()+'\\report_struct.json')
    self.logger = LoggerFactory.get_logger(__class__.__name__, "INFO")
    self.SMTP_HOST = self.CONF.content["SMTP_HOST"]
    self.SMTP_PORT = self.CONF.content["SMTP_PORT"]
    self.SMTP_USER = self.CONF.content["SMTP_USER"]
    self.SMTP_PASS = self.CONF.content["SMTP_PASS"]
    self.recepients = self.CONF.content["recepients"]
    self.txt = self.REPORT_CONF.content["txt"]
    self.today = datetime.now()
    self.timestampt = self.today.strftime("%Y_%m_%d")

  def send(self, attach: str) -> None:
    """
    Void method
    :param str attach - path to attachment for the email
    """
    try:        
        for receiver in self.recepients:                
            header = f"Support Report {self.timestampt}"
            message = MIMEMultipart("alternative")
            message["Subject"] = header
            message["From"] = self.SMTP_USER
            message["To"] = receiver                                                
            # Create the plain-text and HTML version of your message
            f = open(attach, 'r')
            attachment = MIMEText(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=attach)
            message.attach(attachment)
            part = MIMEText(self.txt, "plain")
            message.attach(part)               
            context = ssl._create_unverified_context()
            with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT, context=context) as server:
                server.login(self.SMTP_USER, self.SMTP_PASS)
                status = server.noop()[0]
                if status == 250:
                    server.sendmail(self.SMTP_USER, receiver, message.as_string())
                    self.logger.info(f'Email sent to {receiver}')
                    server.quit()                                                               
                else:
                    self.logger.error(f"Error occured")
    except Exception as e:
        self.logger.exception(f"Exception {e}", exc_info=1)
        pass