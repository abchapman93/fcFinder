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

DATADIR = os.path.join(os.path.expanduser('~'),'Box Sync','Bucher_Surgical_MIMICIII','pyConText_implement','fcFinder')
modifiers = itemData.instantiateFromCSVtoitemData(\
"/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/modifiers.tsv")
targets = itemData.instantiateFromCSVtoitemData(\
    "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/targets.tsv")

def markup_sentence(s,i,modifiers=modifiers, targets=targets, prune_inactive=True):
    """s is the text from a split sentence
    r is the tuple of the span of the sentence
    """
    
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.setDocSpan(i) #this is an added feature that is not in the original pyConTextNLP code
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

def create_context_doc(report,modifiers=modifiers,targets=targets):
    """Creates a ConText document out of a text string using pyConTextNLP itemdata."""
    context_doc = pyConText.ConTextDocument()
    sentences = list(helpers.my_sentence_splitter(report).keys())
    spans = list(helpers.my_sentence_splitter(report).values()) #FEB 10: changed to my_sentence_splitter
    markups = []
    for n in range(len(sentences)):
        s = sentences[n]
        
        i = spans[n]
        m = markup_sentence(s.lower(), i, modifiers=modifiers, targets=targets)
        
        markups.append(m)
    for m in markups:
        context_doc.addMarkup(m)
    return context_doc
    
    
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")
    
    
class mentionAnnotation(object):
    def __init__(self,tagObject,textSource=None,mentionClass=None,mentionid=None,annotatorid='FC_FINDER',span=None,
                 spannedText=None,creationDate=None,XML=None,MentionXML=None):
        """Creates an annotation of Object"""
        self.textSource = textSource
        self.mentionid = str(mentionid)
        self.mentionClass = mentionClass
        self.annotatorid = annotatorid
        self.span = span
        self.spannedText = spannedText
        self.creationDate = creationDate
        self.XML = XML
        self.MentionXML = MentionXML
        self.setCreationDate()
        self.setXML()
        self.setMentionXML()
    def setText(self,text):
        """Sets the text for spannedText"""
        self.spannedText = text
    def setSpan(self,markupSpan): #this should be the entire scope for evidence, but not for modifier
        self.span = markupSpan
    def setMentionID(self,ID):
        self.mentionid = str(ID)
    def setCreationDate(self):
        self.creationDate = time.strftime("%c") #add time zone
    def setXML(self):
        """Creates an element tree that can later be appended to a parent tree"""
        annotation_body = Element("annotation")
        mentionID = SubElement(annotation_body, 'mention')
        mentionID.set('id',self.getMentionID()) #perhaps this needs to follow eHOST's schema
        annotatorID = SubElement(annotation_body,"annotator")
        annotatorID.set('id','eHOST_2010') 
        annotatorID.text = self.getAnnotatorID()
        span = SubElement(annotation_body, "span",{"start":str(self.getSpan()[0]),"end":str(self.getSpan()[1])}) #Why is this backwards?
        spannedText=SubElement(annotation_body,'spannedText')
        spannedText.text = self.getText()
        creationDate = SubElement(annotation_body, "creationDate")
        creationDate.text = self.getCreationDate()
        self.XML = annotation_body
        #print(prettify(parent))
    def setMentionXML(self):
        classMention = Element("classMention")
        classMention.set("id",self.getMentionID())
        mentionClass = SubElement(classMention,"mentionClass")
        mentionClass.set("id",self.getMentionClass())
        mentionClass.text = self.getText()
        self.MentionXML = classMention
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
    def getXML(self):
        return self.XML
    def getMentionXML(self):
        return self.MentionXML
    
    def stringXML(self):
        def prettify(elem):
            """Return a pretty-printed XML string for the Element.
            """
            rough_string = ElementTree.tostring(elem, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        XML_string = prettify(self.getXML())
        MentionXML_string = prettify(self.getMentionXML())
        return XML_string+MentionXML_string
    #add this magic method
    #def __str__(self):
        #return ElementTree.tostring(self.getXML(), 'utf-8')
        #rough_string = ElementTree.tostring(self.getXML(), 'utf-8')
        #reparsed = minidom.parseString(rough_string)
        #return reparsed.toprettyxml(indent="  ")

def fluid_collection_classifier(document,source_file):
    """Takes a ConTextDocument and returns the following unique sets of mentionAnnotation objects:
    definitive_evidence: markups that are classified as definitive evidence of fluid collection.
    negated_evidence: markups that are classified as negated evidence of fluid collection.
    indication: markups that are classified as indication of fluid collection.
    MARCH 1: CHANGED DEFINITIVE, PROBABLE AND HISTORICAL TO POSITIVE
    ignored: markups that contain target words but are unmodified by any modifiers"""
    definite_evidence = 0
    negated_evidence = 0
    indication = 0
    historical = 0
    probable = 0
    ignored = 0

    annotations = []
    completed_spans = []
    markups = [m[1] for m in document.getSectionMarkups()]
    
    for m in markups:
        for tO in m.nodes():
            if tO.getCategory() == ['fluid_collection']:
                annotation = None
                if '?' in m.getRawText():
                    annotation = createAnnotation(m,tO,"fluid collection-indication",source_file)
                    indication += 1
                elif m.isModifiedByCategory(tO,"definite_existence"):
                    if m.isModifiedByCategory(tO,'anatomy'):
                        annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                        definite_evidence += 1
                else:
                    if m.isModifiedByCategory(tO,"definite_negated_existence"):
                        annotation = createAnnotation(m,tO,"Fluid collection-negated",source_file)
                        negated_evidence += 1
                    elif m.isModifiedByCategory(tO, "indication"):
                        annotation = createAnnotation(m,tO,"fluid collection-indication",source_file)
                        indication += 1
                    elif m.isModifiedByCategory(tO,"probable_existence"):
                        if m.isModifiedByCategory(tO,"anatomy"):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            probable += 1
                        else:
                            ignored += 1
                            annotation = None
                    elif m.isModifiedByCategory(tO,"historical"):
                        if m.isModifiedByCategory(tO,"anatomy"):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            historical += 1
                        else:
                            annotation = None
                            ignored += 1
                    else:
                        if m.isModifiedByCategory(tO,'anatomy'):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            definite_evidence += 1
                        else:
                            annotation = None
                            ignored += 1
                    if m.isModifiedByCategory(tO,'pseudoanatomy'):
                        if not m.isModifiedByCategory(tO,'anatomy'):
                            annotation = None
                        else:
                            annotation = annotation
                if annotation:
                    if m.getDocSpan() in completed_spans:
                        pass
                    else:
                        completed_spans.append(m.getDocSpan())
                        annotations.append(annotation)
    for _ in annotations:
        if _ == 'false':
            annotations.remove(_)
    return annotations

    
def createAnnotation(markup,tO,mention_class,file_name): #eventually mention_class will be defined by the logic
    """Takes a ConTextMarkup object and returns a single annotation object.
    This will have to be modified for classes other than definiiveEvidence
    2/24: cut down the unnecessary if statements"""
    #annotations = []
    
    annotation = mentionAnnotation(tagObject=tO,textSource=file_name,mentionClass=mention_class,
                                    mentionid=tO.getTagID(), spannedText=markup.getText(),
                                    span=markup.getDocSpan())
    return annotation
    
def getXML(annotation): #text source should be at the document level
        return annotationXMLSkel.format(annotation.getTextSource(),annotation.getMentionID(),
                annotation.getAnnotatorID(),annotation.getSpan()[0],annotation.getSpan()[1],
                annotation.getText(),annotation.getCreationDate(),annotation.getMentionClass())

def writeKnowtator(annotations,text_source): #test_source should be read automatically from the XML string
    """Writes a .txt.knowtator.xml file for all annotations in a document
    Takes a list of mentionAnnotation objects, a source file name, and an outpath.
    2/3/17: returns a single ElementTree Element object.
    Need to be able to turn this into a string."""
    
    root = Element('annotations')
    root.set('textSource',text_source)
    for annotation in annotations:
        try: #Feb 10 debug this later!!!
            root.append(annotation.getXML())
            root.append(annotation.getMentionXML())   ####Bring this back later!!!
        except AttributeError:
            pass
    
        
    adjudication_status = SubElement(root,'eHOST_Adjudication_Status')
    adjudication_status.set('version','1.0')
    selected_annotators = SubElement(adjudication_status,'Adjudication_Selected_Annotators')
    selected_annotators.set('version','1.0')
    selected_classes = SubElement(adjudication_status,'Adjudication_Selected_Classes')
    selected_classes.set('version','1.0')
    adjudication_others = SubElement(adjudication_status,'Adjudication_Others')
    
    check_spans = SubElement(adjudication_others,'CHECK_OVERLAPPED_SPANS')
    check_spans.text = 'false'
    check_attributes = SubElement(adjudication_others,'CHECK_ATTRIBUTES')
    check_attributes.text = 'false'
    check_relationship = SubElement(adjudication_others,'CHECK_RELATIONSHIP')
    check_relationship.text = 'false'
    check_class = SubElement(adjudication_others,'CHECK_CLASS')
    check_class.text = 'false'
    check_comment = SubElement(adjudication_others,'CHECK_COMMENT')
    check_comment.text = 'false'
    
    XMLstring = prettify(root)
    return XMLstring





