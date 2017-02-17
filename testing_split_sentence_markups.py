#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:16:19 2017

@author: alec
"""

import os
import glob
import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData


import pyConTextNLP.pyConTextGraph as pyConText
from pyConTextNLP.pyConTextGraph import ConTextMarkup
import fcFinder
import helpers
import importlib
#importlib.reload(fcFinder)
#importlib.reload(pyConText)


DATADIR = os.path.join(os.path.expanduser('~'),'desktop','PreprocessedReports','Batch_3','corpus',)
my_file_path = os.path.join(DATADIR,'Yes_28226_116465_05-29-93.txt')
modifiers = itemData.instantiateFromCSVtoitemData(\
"/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/modifiers.tsv")
targets = itemData.instantiateFromCSVtoitemData(\
    "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/targets.tsv")


f1 = open(my_file_path,'r')
clean_report = f1.read()
#print(my_file)

#split_report = helpers.my_sentence_splitter(clean_report)
#sentences = list(split_report.keys())
#spans = list(split_report.values())
#markup1 = fcFinder.markup_sentence(sentences[0],spans[0])

ConText = fcFinder.create_context_doc(clean_report)

annotations = fcFinder.fluid_collection_classifier(ConText,'Yes_28226_116465_05-29-93.txt')
#fcFinder.writeKnowtator(annotations,'Yes_28226_116465_05-29-93.txt',os.path.join(os.path.expanduser('~'),'Desktop'))