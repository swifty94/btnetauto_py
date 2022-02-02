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
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email(object):
  """
  Class for reporting data via email once job is finished
  """
  def __init__(self):
    pass

  def send(self, attach: str) -> None:
    """
    Void method
    :param str attach - path to attachment for the email
    """
    try:        
        if True:
            for receiver in self.RECEPIENTS:                
                header = f""
                message = MIMEMultipart("alternative")
                message["Subject"] = header
                message["From"] = self.SMTP_USER
                message["To"] = receiver                                
                now = datetime.now()
                date = now.strftime("%Y_%m_%d_%H-%M_%S")
                reportPath = 'reports/'
                attach_file_name = f"_Export_{date}_.csv"                

                # Create the plain-text and HTML version of your message
                TEXT = """      
                
                """

                HTML = """
                
                """

                f = open(attach_file_name, 'r')
                attachment = MIMEText(f.read())
                attachment.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
                message.attach(attachment)      
                part1 = MIMEText(TEXT, "plain")
                part2 = MIMEText(HTML, "html")      
                message.attach(part1)
                message.attach(part2)                         
                #context = ssl._create_unverified_context()
                with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT, context=None) as server:
                    server.login(self.SMTP_USER, self.SMTP_PASS)
                    status = server.noop()[0]
                    if status == 250:
                        server.sendmail(self.SMTP_USER, receiver, message.as_string())
                        #logging.info(f'{self.cn} Email sent ')
                        #server.quit()                                                               
                    else:
                        #logging.info(f"{self.cn} SMTP session: Failed")
                        #logging.exception(f"{self.cn} Error occured during either establising SMTP session or sending an email")
                        #logging.exception(f"{self.cn} Please validate the connection to your SMTP server and/or your credentials")
                        pass
                    #os.remove(attach_file_name)
        else:
            #logging.info(f"{self.cn} SMTP is not enabled")
            pass
    except Exception as e:
        #logging.error(f"{self.cn} Exception {e}", exc_info=1)
        pass