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
from base import LoggerFactory
from selenium import webdriver    
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# initialize the logger object


class WebParser:
    def __init__(self) -> None:
        self.log = LoggerFactory.get_logger(__class__.__name__, log_level="INFO")

    def create_session(self):
        options = Options()
        #options.add_argument('--headless')
        driver_type = r'./bin/chromedriver.exe'
        browser = webdriver.Chrome(executable_path=driver_type, chrome_options=options)
        self.log.info(f'Browser: Chrome \n WebDriver: {driver_type}')
        self.log.info(f'Session OPTS: {options.arguments}')
        return browser

    def login_btnet(self):
        try:
            browser = self.create_session()            
            self.log.info(f'{__class__.__name__ }] [Session Start')
            browser.get('http://btnet.friendly-tech.com/btnet/')
            username = WebDriverWait(browser, 3).until(lambda x: x.find_element(By.XPATH, '//*[@id="user"]'))
            password = WebDriverWait(browser, 3).until(lambda x: x.find_element(By.XPATH, '//*[@id="pw"]'))
            username.send_keys("Kirill Rudenko")
            password.send_keys("!KirillRu1")
            password.send_keys(Keys.ENTER)

            #   Add pause page body loads properly
            WebDriverWait(browser, 5).until(lambda x: x.find_element(By.XPATH, '/html/body'))
            
            self.log.info(f'Login success')
            #return browser
        
        except Exception as e:
            self.log.exception(f'Exception {e}', exc_info=1)                          
    

b = WebParser()
b.login_btnet()