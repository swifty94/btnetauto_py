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
#   Logger factory / Helpers classes module
#
import logging
import logging.config
from os import path
import json
logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), 'logging.ini'))

class LoggerFactory(object):

    _LOG = None

    @staticmethod
    def __create_logger(cls_name,  log_level):
        """
        A private method that interacts with the python
        logging module
        """
        # get the logging format
        # Initialize the class variable with logger object
        
        LoggerFactory._LOG = logging.getLogger(cls_name)
        # set the logging level based on selection
        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(cls_name, log_level):
        """
        A static method called by other modules to initialize logger in separate class
        """
        logger = LoggerFactory.__create_logger(cls_name, log_level)
        # return the logger object
        return logger

class JsonConf(object):
    def __init__(self, json_file) -> None:
        self.json_file = json_file
        self.logger = LoggerFactory.get_logger(__class__.__name__, "INFO")
        self.content = {}
        self.__getContent()

    def __getContent(self):
        try:
            with open(self.json_file) as f:
                data = json.load(f)
                for k, v in data.items():
                    self.content[k] = v
        except Exception as e:
            self.logger.error(f'Exception {e}', exc_info=1)
            
class UserConf(JsonConf):
    def __init__(self, json_file='user_conf.json') -> None:
        super().__init__(json_file)

class ReportrConf(JsonConf):
    def __init__(self, json_file='report_struct.json') -> None:
        super().__init__(json_file)

r = ReportrConf()