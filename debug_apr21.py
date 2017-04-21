#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:37:55 2017

@author: alec
"""

import os
import sys
sys.path.append(os.path.join(os.getcwd(),'..'))
import fcFinder as fc
import helpers
import rules
import input_output as io

DATADIR = '/Users/alec/Desktop/fcfinder_apr21'
file = os.path.join(DATADIR, 'corpus', 'Yes_74976_148937_02-28-66.txt')
outdir = os.path.join(DATADIR,'saved')
with open(file,'r') as f:
    report = f.read()
    
pipeline = fc.my_pipeline
findings = pipeline(report)

