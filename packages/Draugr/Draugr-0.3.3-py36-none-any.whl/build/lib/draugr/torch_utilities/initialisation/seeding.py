#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

import numpy
import torch

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 09/10/2019
           '''

def seed(s):
  random.seed(s)
  numpy.random.seed(s)
  torch.manual_seed(s)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(s)
