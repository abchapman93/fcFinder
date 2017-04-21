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
#from rules import markup_conditions, markup_classifier

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
    if not span:
        span = (0,len(s))
    markup.docSpan = span
    
    markup.cleanText() #add your own cleanText function in helpers
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    markup.markupClass = markup_classifier(markup)
    return markup
    #return MarkupSpanPair(markup=markup,span=span)

def create_list_of_markups(sentences,spans=False):
    """Takes a list of sentences and returns a list of markups.
    If you are passing in document spans for each sentence, set spans = True and
    pass sentences as a list oftwo-tuples with the sentence in index 0. 
    Example:
        [ ..., ('There is a fluid collection near the abdomen.', (56, 72)), 
           (No rim enhancement can be seen.', (73, 86)),... ] 
    """

    if spans:
        markups = [markup_sentence(s=x[0],span=x[1]) for x in sentences]
    else:
        markups = [markup_sentence(x) for x in sentences]
    return markups

def create_context_doc(list_of_markups,modifiers=modifiers,targets=targets):
    """Creates a ConText document out of a list of markups."""
    context_doc = pyConText.ConTextDocument()
    for m in list_of_markups:
        context_doc.addMarkup(m)
    return context_doc
    

class markup_conditions(object):
    """This class creates the conditions of interest for a markup.
    A rule-based classifier can then assign a class to a markup based on rules
    pertaining to these conditions.
    """
    def __init__(self,markup=None, target_values=[['fluid_collection']], target=None,
                 tag_objects=[], definitive=False, historical=False,probable=False, negated=False,
                 indication=False, anatomy=False, pseudoanatomy=False):
        self.markup=markup
        self.tag_objects=tag_objects
        self.target_values=target_values
        self.target=target
        self.definitive=definitive
        self.historical=historical
        self.probable=probable
        self.negated=negated
        self.indication=indication
        self.anatomy=anatomy
        self.pseudoanatomy=pseudoanatomy
        
        self.set_target()
        if self.target:
            self.set_anatomy()
            self.set_definitive()
            self.set_negated()
            self.set_indication()
            self.set_pseudoanatomy()

    def set_target(self): #These rules should be customized
        for tag_object in self.markup.nodes():
            if tag_object.getCategory() in self.target_values: #could be changed for multiple target values
                self.target = tag_object
    def set_anatomy(self):
        if self.markup.isModifiedByCategory(self.target,'anatomy'):
            self.anatomy = True
    def set_definitive(self):
        if self.markup.isModifiedByCategory(self.target,'definitive_existence'):
            self.definitive = True
    def set_negated(self):
        if self.markup.isModifiedByCategory(self.target,'definite_negated_existence'):
            self.negated = True
    def set_indication(self):
        if self.markup.isModifiedByCategory(self.target,'indication'):
            self.indication = True
    def set_pseudoanatomy(self):
        if self.markup.isModifiedByCategory(self.target,'pseudoanatomy'):
            self.pseudoanatomy = True
            
def markup_classifier(markup):
    """Takes a markup object and classifies according to logic defined below.
    Should be customized for implementation.
    Note the lower capitalization of fluid collection-indication; this is only to match
    the annotations made in the gold standard for this project."""
    conditions = markup_conditions(markup)
    
    markup_class = None
    if not conditions.target:
        pass
    #positive
    elif (conditions.anatomy and not conditions.negated and not conditions.indication)\
        or (conditions.anatomy and conditions.definitive):
        markup_class = "Fluid collection-positive"
        
    #negated
    elif conditions.negated and not conditions.definitive:
        markup_class = "Fluid collection-negated"
    
    #indication
    elif conditions.indication and not (conditions.negated or conditions.definitive
                                or conditions.historical or conditions.probable):
        markup_class = "fluid collection-indication"
        
    #check for pseudoanatomy
    if conditions.pseudoanatomy and not conditions.anatomy:
        markup_class = None
    return markup_class



def my_pipeline(report, preprocess=lambda x:x.lower(), 
                splitter=helpers.my_sentence_splitter):
    report = preprocess(report)
    sentences = splitter(report)
    markups = create_list_of_markups(sentences,spans=True)
    markups = [m for m in markups if m.markupClass]
    #classified_markups = 
    #document = create_context_doc(markups)
    #markups = 
    return markups






    
