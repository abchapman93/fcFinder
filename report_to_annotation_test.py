#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 12:14:18 2017

@author: alec
"""

### From report to a single annotation
import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
import networkx as nx
import pyConTextNLP.display.html as html
from IPython.display import display, HTML
import os
import fcFinder as fc

modifiers = itemData.instantiateFromCSVtoitemData("/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/modifiers.tsv")
targets = itemData.instantiateFromCSVtoitemData(
    "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/targets.tsv")

input_report = '/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/Radiology_Annotation/Adjudication/Batch_3/corpus/Yes_28226_116465_05-29-93.txt'
report = ''
with open(input_report,'r') as f0:
    report += f0.read()

context = pyConText.ConTextDocument()

blob = TextBlob(report.lower())
count = 0
rslts = []
for s in blob.sentences:
    m = markup_sentence(s.raw, modifiers=modifiers, targets=targets)
    rslts.append(m)

for r in rslts:
    context.addMarkup(r)

marked_up = context.getSectionMarkups()[0][1]

tO = marked_up.getMarkedTargets()[0]

annotation1 = createAnnotation(marked_up,tO,'Fluid collection-definitive','Yes_28226_116465_05-29-93.txt')