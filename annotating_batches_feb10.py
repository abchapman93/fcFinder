#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:52:17 2017

@author: alec
"""
import sys
 
import os

import glob
import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData


import pyConTextNLP.pyConTextGraph as pyConText
from pyConTextNLP.pyConTextGraph import ConTextMarkup
import fcFinder as fc
import helpers
import importlib
#importlib.reload(fcFinder)
#importlib.reload(pyConText)

def preprocess_batches(inpath,outpath):
    counter = 0
    if os.path.exists(inpath) == False or os.path.exists(outpath) == False:
        print("Please check that your path names are correct")
    else:
        print('True')
    batches = glob.glob(os.path.join(inpath,'Batch*'))
    for batch in batches:
        batch_name = os.path.basename(batch)
        os.mkdir(os.path.join(outpath,batch_name))
        os.mkdir(os.path.join(outpath,batch_name,'corpus'))
        
        files = glob.glob(os.path.join(batch,"corpus","*.txt"))

        for file in files:
            with open(file,'r') as f1:
                old_report = f1.read()
                cleaned_report = helpers.preprocess(old_report)
                report_name = os.path.basename(file)
                with open(os.path.join(outpath,batch_name,'corpus',report_name),'w') as f0:
                    f0.write(cleaned_report)
                counter += 1
    print("You edited %d batches"%counter)
    return outpath
        
#preprocess_batches(os.path.join(
    #os.path.expanduser('~'),'Box Sync','Bucher_Surgical_MIMICIII','Radiology_Annotation','Adjudication'),
    #os.path.join(os.path.expanduser('~'),'Desktop','PreprocessedReports'))


DATADIR = os.path.join(os.path.expanduser('~'),'desktop','PreprocessedReports','Batch_3','corpus')
#my_file_path = os.path.join(DATADIR,'Yes_115_114585_10-31-94.txt')
outpath = os.path.join(os.path.expanduser('~'),'desktop','PreprocessedReports','Batch_3','saved')




def annotate_report(file_path, output_dir, modifiers=fc.modifiers, targets=fc.targets):
    #if not os.path.exists(os.path.join(output_dir,'saved')):
        #os.mkdir(os.path.join(output_dir,'saved'))
    #if not os.path.exists(os.path.join(output_dir,'corpus'))
        #os.mkdir(os.path.join(output_dir,'corpus'))
    report_name = os.path.basename(file_path)
    report = ''
    with open(file_path,'r') as f0:
        report += f0.read()
    #print(report_name)
    #print( report)
    context = fc.create_context_doc(report, modifiers, targets)
    #print(context.getDocumentGraph())
    annotations = fc.fluid_collection_classifier(context,report_name)
    XML_string = fc.writeKnowtator(annotations,report_name)
    with open(os.path.join(output_dir,report_name+'.knowtator.xml'),'w') as f1:
        f1.write(XML_string)
    return
#annotation1 = annotate_report(my_file_path,outpath)
def annotate_batch(inpath, outpath):
    counter = 0
    if os.path.exists(inpath) == False or os.path.exists(outpath) == False:
        print("Please check that your path names are correct")
    else:
        print('True')
    #batch_name = os.path.basename(inpath)
    #if not os.path.exists(os.path.join(outpath,batch_name,'saved')):
        #os.mkdir(os.path.join(outpath,batch_name,'saved'))

    
    files = glob.glob(os.path.join(inpath,"*.txt"))
    
    #print(files)
    for file in files:
        
        annotate_report(file,outpath)
            
        counter += 1
    print("You annotated %d batches in %s"%(counter,outpath))
    return outpath
    
#annotate_batch(DATADIR,outpath)








"""



def annotate_batches(inpath,outpath):
    counter = 0
    if os.path.exists(inpath) == False or os.path.exists(outpath) == False:
        print("Please check that your path names are correct")
    else:
        print('True')
    batches = glob.glob(os.path.join(inpath,'Batch*'))
    for batch in batches:
        batch_name = os.path.basename(batch)
        #if the batch doesn't have a folder, make one
        if not os.path.exists(os.path.join(outpath,batch_name,'saved')):
            os.mkdir(os.path.join(outpath,batch_name,'saved'))
        files = glob.glob(os.path.join(batch,"corpus","*.txt"))

        for file in files:
            report_name = os.path.basename(file)
            with open(os.path.join(outpath,batch_name,'saved',report_name),'w') as f0:
                f0.write(fcFinder(inpath,outpath))
            counter += 1
    print("You edited %d batches"%counter)
    return outpath

#findings = fcFinder(my_file_path,outpath)
"""
