# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import logging
import subprocess

import wrapt
import re
import functools

from colored import fore, back, style

import consolejs
from consolejs.expr_debug import _expr_debug, _cdebug
from consolejs.Console import Console
from consolejs.formats import format_dict, format_caller

"""
 Consolejs : A console logger for Python

"""

class ConsolejsImpl:

    def __init__(self, name) :

        self.name = name
        self._console = None
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self._level)

        self.logger_shandler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        self.logger_shandler.setFormatter(formatter)
        self.logger.addHandler(self.logger_shandler)

        self._console = Console(self.name, self.logger)
    
    @property
    def console(self):
        return self._console


