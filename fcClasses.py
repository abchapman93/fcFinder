#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:20:47 2017

@author: alec
"""
#create classes
import fcFinder
import pyConTextNLP.pyConTextGraph as pyConText
from pyConTextNLP.pyConTextGraph import ConTextMarkup
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
import networkx as nx
import os

import re
import copy
import networkx as nx
import platform
import copy
import uuid
import datetime
import time

"""A module defining itemData classes specific to fcFinder.

    1) definitiveEvidence
    2) negatedEvidence
    3) indication
    4) historicalEvidence
    5) probableEvidence"""

modifiers = itemData.instantiateFromCSVtoitemData("/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/modifiers.tsv")
targets = itemData.instantiateFromCSVtoitemData(
    "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/targets.tsv")
class mentionAnnotation(object):
    def __init__(self,tagObject,textSource=None,mentionClass=None,mentionid=None,annotatorid='FC_FINDER',span=None,
                 spannedText=None,creationDate=None):
        """Creates an annotation of Object"""
        self.textSource = textSource
        self.mentionid = mentionid
        self.mentionClass = mentionClass
        self.annotatorid = annotatorid
        self.span = span
        self.spannedText = spannedText
        self.creationDate = creationDate
        self.setCreationDate()
    
    def setText(self,text):
        """Sets the text for spannedText"""
        self.spannedText = text
    def setSpan(self,markupSpan): #this should be the entire scope for evidence, but not for modifier
        self.span = markupSpan
    def setMentionID(self,ID):
        self.mentionid = ID
    def setCreationDate(self):
        self.creationDate = time.strftime("%c") #add time zone

    def getTextSource(self):
        return self.textSource
    def getMentionClass(self):
        return self.mentionClass    
    def getMentionID(self):
        return self.mentionid    
    def getText(self):
        return self.spannedText
    def getSpan(self):
        return self.span
    def getAnnotatorID(self):
        return self.annotatorid
    def getCreationDate(self):
        return self.creationDate


    
    
def createAnnotations(markup,mention_class,file_name): #eventually mention_class will be defined by the logic
    """Takes a ConTextMarkup object and returns a list of annotation object
    This will have to be modified for classes other than definiiveEvidence"""
    annotations = []

    for tO in markup.nodes(): #apply logic here to apply to multiple different mention_classes
        if mention_class == 'fluid collection-definitive':
            annotation = mentionAnnotation(tagObject=tO,textSource=file_name,mentionClass=mention_class,
                    mentionid=tO.getTagID(), spannedText=markup.getText(),
                    span=markup.getScope()) #scope only for definitive
        #annotation = definitiveEvidence(markup)
        #annotation.setText(markup.getText())
        #annotation.setSpan(markup.getScope())
        #annotation.setMentionID(tO.getTagID())
        
            annotations.append(annotation)
    return annotations
    
def getXML(annotation): #text source should be at the document level
        return annotationXMLSkel.format(annotation.getTextSource(),annotation.getMentionID(),
                annotation.getAnnotatorID(),annotation.getSpan()[0],annotation.getSpan()[1],
                annotation.getText(),annotation.getCreationDate(),annotation.getMentionClass())

annotationXMLSkel = \
u"""<?xml version="1.0" encoding="UTF-8"?>
<annotations textSource="{0}">
    <annotation>
        <mention id = "{1}" /> 
        <annotator id="{2}"</annotator> 
        <span start="{3}" end="{4}" />
        <spannedText>{5}</spannedText>
        <creationDate>{6}</creationDate>
    </annotation>
    <classMention id="{1}">
        <mentionClass id="{7}">{5}</mentionClass>
    </classMention>
</annotations>

"""

def writeKnowtator(XMLstring,text_source,outpath): #test_source should be read automatically from the XML string
    """Writes a .txt.knowtator.xml file for all annotations"""
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    with open(os.path.join(outpath,text_source+'knowtator.xml'),'w') as f0:
        f0.write(XMLstring)
    return outpath
    
#markup1 = fcFinder.markup_sentence('There is a fluid collection in the abdomen.',modifiers,targets)
#tagObject1 = markup1.nodes()[0]
#annotation1 = createAnnotations(markup1,'fluid collection-definitive','file123.txt')[0]
#class definitiveEvidence(ConTextMarkup):
#    def __init__(self,txt='',scope=None,class_name="Fluid collection-definitive",\
#                 unicodeEncoding='utf-8'):
#        self.setRawText()
#        self.scope=scope
#        self.class_name= class_name
#        super(ConTextMarkup,self).__init__(__txt=None,__rawtxt=txt,__scope=None,__SCOPEUPDATED=False)
#        self.__document = nx.DiGraph()
#        self.__document.add_node("top",category="document")
#        self.__VERBOSE = False
#        self.__tagID = 0
#        self.__unicodeEncoding = unicodeEncoding
    #def setScope(self):
        #self.scope = 
#    def setRawText(self,txt=u''):
#        """
#        sets the current txt to txt and resets the current attributes to empty
#        values, but does not modify the object archive
#        """
#        if self.getVerbose():
#        self.graph["__rawTxt"] = txt
#        self.graph["__scope"] = None
#        self.graph["__SCOPEUPDATED"] = False
#    def get_class_name(self):
#        return self.class_name
    #self.setRawText()
    

        
#markup_test = fcFinder.markup_sentence("There is a fluid collection in the liver", modifiers, targets)

#example_definite = createAnnotation(markup_test)

