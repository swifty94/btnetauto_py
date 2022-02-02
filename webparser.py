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
#   Web parsing module
#
import time
from os import mkdir, path, getcwd
import shutil
from base import LoggerFactory, JsonConf
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
class WebParser:
    """WebParser"""
    def __init__(self) -> None:
        """
        WebParse class provides the whole report export pipeline within main() module\n
        Exported reports structure to be defined in report_struct.json file
        BTNet URL, user/pass for portal to be defined in user_conf.json\n
        param: none
        """
        self.log = LoggerFactory.get_logger(__class__.__name__, log_level="INFO")
        self.CONF = JsonConf(getcwd()+'\\user_conf.json')
        self.url = self.CONF.content["URL"]
        self.usr = self.CONF.content["USER"]
        self.passwd = self.CONF.content["PASS"]
        self.tmp_path = getcwd()+"\\tmp\\"
    
    def _make_tmp(self):
        try:
            if path.isdir(self.tmp_path):
                self.log.info(f'Removing prev tmp path {self.tmp_path}')
                shutil.rmtree(self.tmp_path, ignore_errors=True)
            self.log.info(f'Creating tmp directory {self.tmp_path}')
            mkdir(self.tmp_path)
        except Exception as e:
            self.log.exception(f"Exception - {e}", exc_info=1)

    def _create_session(self):
        """Create browser session object"""
        try:
            self._make_tmp()      
            options = Options()
            prefs = {"download.default_directory": self.tmp_path.replace('/', "\\")}
            options.add_argument('--headless')
            options.add_experimental_option("prefs", prefs)
            service = Service(r'./bin/chromedriver.exe')
            session = webdriver.Chrome(service=service, options=options)
            self.log.info(f'Browser: Chrome')
            self.log.info(f'Session opts: {options.arguments}')
            self.log.info(f'Session prefs: {options.experimental_options}')
            self.log.info('Session created')
            return session
        except Exception as e:
            self.log.exception(f"Exception - {e}")

    def login_btnet(self):
        """Login to the BTNet"""
        try:
            session = self._create_session()            
            self.log.info('login_btnet Start')
            session.get(self.url)
            username = WebDriverWait(session, 3).until(lambda x: x.find_element(By.XPATH, '//*[@id="user"]'))
            password = WebDriverWait(session, 3).until(lambda x: x.find_element(By.XPATH, '//*[@id="pw"]'))
            username.send_keys(self.usr)
            password.send_keys(self.passwd)
            password.send_keys(Keys.ENTER)
            #   Add pause page body loads properly
            WebDriverWait(session, 5).until(lambda x: x.find_element(By.XPATH, '/html/body'))
            self.log.info('login_btnet success')
            return session        
        except Exception as e:
            self.log.exception(f'Exception {e}', exc_info=1)

    def create_view_and_export(self, logon_session, priority: str):
        try:
            """
            Create proper BTs table view based on report_stuct.json
            :param logon_session: WebDriver\n
            :param priority: str: '2 - must fix' or '3 - fix'
            """
            self.log.info(f'Start BTNet View for BT priority - {priority}')
            #organization
            org = Select(logon_session.find_element(By.ID, 'sel_[organization]'))
            org.select_by_visible_text('Friendly Support')
            #status
            status = Select(logon_session.find_element(By.ID, 'sel_[status]'))
            status.select_by_visible_text('open')
            #priority
            bt_priority = Select(logon_session.find_element(By.ID, 'sel_[priority]'))
            bt_priority.select_by_visible_text(priority)
            self.log.info(f"Created BTNet View for BT priority - {priority}")
            logon_session.find_element(By.XPATH, '//*[@id="ctl00"]/div[3]/table[1]/tbody/tr/td[5]/a').click()
            self.log.info(f"Exported CSV for {priority}")
            return logon_session
        except Exception as e:
            self.log.exception(f'Exception {e}', exc_info=1)
    
    def session_die(self, session) -> None:
        """
        Kill WebDriver instance
        :param: session: WebDriver
        :return: bool
        """
        try:
            session.close()
            self.log.info(f'Session Killed')
        except Exception as e:
            self.log.exception(f'Exception {e}', exc_info=1)
            

    def main(self) -> None:
        """
        Complete main pipeline
        param: None
        return: None
        """
        try:
            self.log.info('Main pipeline - start')
            logon_session = self.login_btnet()
            self.create_view_and_export(logon_session, "2 - must fix")
            time.sleep(5)
            self.log.info('Pause 5 sec')
            self.create_view_and_export(logon_session, "3 - fix")
            self.log.info('Pause 5 sec more')
            time.sleep(5)  
            self.session_die(logon_session)
            self.log.info('Main pipeline - finish')
        except Exception as e:
            self.log.exception(f'Exception {e}', exc_info=1)
                     