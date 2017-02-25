#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:52:17 2017

@author: alec
"""
import sys
import os
import glob
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText
from pyConTextNLP.pyConTextGraph import ConTextMarkup
import fcFinder as fc
import helpers

def annotate_report(file_path, output_dir, modifiers=fc.modifiers, targets=fc.targets):
    report_name = os.path.basename(file_path)
    report = ''
    with open(file_path,'r') as f0:
        report += f0.read()
    context = fc.create_context_doc(report, modifiers, targets)
    annotations = fc.fluid_collection_classifier(context,report_name)
    XML_string = fc.writeKnowtator(annotations,report_name)
    with open(os.path.join(output_dir,report_name+'.knowtator.xml'),'w') as f1:
        f1.write(XML_string)
    return

def annotate_batch(inpath, outpath):
    counter = 0
    if os.path.exists(inpath) == False or os.path.exists(outpath) == False:
        print("Please check that your path names are correct")
    else:
        print('True')
    files = glob.glob(os.path.join(inpath,"*.txt"))
    for file in files:
        annotate_report(file,outpath)
        counter += 1
    print("You annotated %d batches in %s"%(counter,outpath))
    return outpath
