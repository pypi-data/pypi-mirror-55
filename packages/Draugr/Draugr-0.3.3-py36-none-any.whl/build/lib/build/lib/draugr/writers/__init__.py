#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

from draugr.writers.console.terminal_writer import ConsoleWriter
from .csv_writer import CSVWriter
from .log_writer import LogWriter
from .mock_writer import MockWriter
from .tensorboard import *
