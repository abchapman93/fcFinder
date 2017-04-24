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
#import rules
import input_output as io

DATADIR = '/Users/alec/Desktop/fcfinder_apr21'
file = os.path.join(DATADIR, 'corpus', 'Yes_74976_148937_02-28-66.txt')
outdir = os.path.join(DATADIR,'saved')
with open(file,'r') as f:
    report = f.read()
    
pipeline = fc.fc_pipeline
findings = pipeline(report)

annotations = []
for f in findings:
    annotations.append(io.createAnnotation(f,'Yes_74976_148937_02-28-66.txt'))

for a in annotations:
    XMLstring = io.write_knowtator(annotations,'Yes_74976_148937_02-28-66.txt')
    with open(os.path.join(outdir,'Yes_74976_148937_02-28-66.txt.knowtator.xml'),'w') as f0:
        f0.write(XMLstring)
#annotations = []
#for f in findings:
#    annotation = io.createAnnotation(f)
#    annotations.append(annotation)
