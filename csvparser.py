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
#   CSV report parsing module
#
from base import LoggerFactory, ReportrConf
import pandas as pd
from datetime import datetime
from os import listdir, getcwd
from os.path import isfile, join

class Report(object):
    def __init__(self) -> None:
        self.logger = LoggerFactory.get_logger(__class__.__name__, "INFO")
        self.mypath = getcwd()+"\\tmp\\"
        self.CONF = ReportrConf()
        self.cols = self.CONF.content["columns"]
        self.name = self.CONF.content["reportName"]
        self.today = datetime.now()
        self.timestampt = self.today.strftime("%Y_%m_%d_%H-%M_%S")
        self.finaleName = f"{self.name}_{self.timestampt}.csv"
        self.dataFrames = []
    
    def make(self):
        try:
            csvFiles = [f for f in listdir(self.mypath) if isfile(join(self.mypath, f))]
            self.logger.info(f"Processing: {csvFiles}")
            for csvF in csvFiles:
                df = pd.read_csv('tmp/'+csvF, usecols=self.cols)
                df = df[self.cols]
                df.set_index('id', inplace=True)
                self.dataFrames.append(df)   
            combined = pd.concat(self.dataFrames)
            combined.to_csv(self.finaleName)
            if isfile(self.finaleName):
                self.logger.info(f"Created report {self.finaleName}")
                return self.finaleName
            else:
                self.logger.warning("Something went wrong")
                return None
        except Exception as e:
            self.logger.exception(f"Exception {e}")