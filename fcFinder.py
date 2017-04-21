#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 11:04:31 2017

@author: alec
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:02:49 2017

@author: alec
"""

import pyConTextNLP.pyConTextGraph as pyConText
from pyConTextNLP.pyConTextGraph import ConTextMarkup
import pyConTextNLP.itemData as itemData
import os
import helpers

import re
import copy
import networkx as nx
import platform
import copy
import uuid
import datetime
import time

from xml.etree.cElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from collections import namedtuple

DATADIR = os.path.join(os.path.expanduser('~'),'Box Sync','Bucher_Surgical_MIMICIII','pyConText_implement','fcFinder')
modifiers = itemData.instantiateFromCSVtoitemData(\
"/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/modifiers.tsv")
targets = itemData.instantiateFromCSVtoitemData(\
    "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/targets.tsv")

def markup_sentence(s,span=None,modifiers=modifiers, targets=targets, prune_inactive=True):
    """s is a sentence from a list of a split report.
    span is the tuple of the span of the sentence. Optional.
    Returns a named tuple where markup=markup, span=span
    NOTE: this is different than in the original pyConText library,
    where this function just returns a markup object.
    This is to allow the user to keep track of the original span from the document.
    """
    #MarkupSpanPair = namedtuple('MarkupSpanPair',['markup','span'])
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    #if i:
        #markup.setDocSpan(i) #this is an added feature that is not in the original pyConTextNLP code
    #APR 19: to make this more compatible with the original pyConText, stopped using i as an attribute of markup
    if not span:
        span = (0,len(s))
    markup.docSpan = span
    
    markup.cleanText() #add your own cleanText function in helpers
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup
    #return MarkupSpanPair(markup=markup,span=span)

def create_list_of_markups(sentences,spans=None):
    """Takes a list of sentences and returns a list of markups.
    If you are passing in document spans for each sentence, set spans = True and
    pass sentences as a list oftwo-tuples with the sentence in index 0. 
    Example:
        [ ..., ('There is a fluid collection near the abdomen.', (56, 72)), 
           (No rim enhancement can be seen.', (73, 86)),... ] 
    """

    if spans:
        markups = [markup_sentence(s=x[0],span=x[1]) for x in sentences]
    markups = [markup_sentence(x) for x in sentences]
    return markups

def create_context_doc(list_of_markups,modifiers=modifiers,targets=targets):
    """Creates a ConText document out of a list of markups."""
    context_doc = pyConText.ConTextDocument()
    for m in list_of_markups:
        context_doc.addMarkup(m)
    return context_doc


def fcPipeline(reports,preprocess=lambda x:x.lower(),splitter=lambda x:x.split('.'),
               output=None):
    """A simple, generic pipeline that can be used with the fcFinder module.
    Takes a single report as a string, ends with an output function"""
    report = preprocess(report)
    sentences = [splitter(r) for r in report]
    markups = create_list_of_markups(sentences) 
    document = create_context_doc(markups)
    
    return document
    

    
    
    
    

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")











    
