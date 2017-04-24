#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:24:52 2017

@author: alec

This module contains functions for input and output.
"""

import os, sys
import glob
import sqlite3 as sqlite
import numpy as np
sys.path.append(os.getcwd())
import fcFinder as fc


def read_file(inpath):
    with open(inpath,'r') as f:
        text = f.read()
    return text
    
def read_batch_of_files(DIR):
    """Reads in an entire batch of text files as a list of strings"""
    files = glob.glob(os.path.join(DIR,'*.txt'))
    texts = []
    for f in files:
        with open(f,'r') as f:
            texts.append(f.read())
    return texts
    
def read_sqlite(db, view=None,query=None):
    """Allows the user to select notes from a sqlite database using either 
    prewritten views or a custom query.
    Parameters:
        conn - database connection
        view - integer specifying which prewritten query to use. Default None.
        query - Custom string query"""
    conn = sqlite.connect(db)
    cursor = conn.cursor()
    if view and query:
        raise ValueError("View and query cannot both be defined.")
    if query:
        cursor.execute(query)
    if view == 1:
        cursor.execute("""SELECT text FROM training_notes""")
    if view == 2:
        cursor.execute("""SELECT text FROM testing_notes""")
    texts = [x[0] for x in cursor.fetchall()]
    return texts

def fc_vectorizer(annotations,classes):
    """Takes a list of annotations from fcFinder and arbitrary arguments representing the classes.
    Outputs a vector of annotation counts for each class argument."""
    arr = np.zeros((len(classes),1))
    arr = np.ravel(arr)
    for i in range(len(classes)):
        for a in annotations:
            if a == classes[i]:
                arr[i] += 1
    return arr

#need to get the target tag object from the markup
    
def createAnnotation(markup,file_name): #eventually mention_class will be defined by the logic
    """Takes a ConTextMarkup object and returns a single annotation object.
    This will have to be modified for classes other than definiiveEvidence
    2/24: cut down the unnecessary if statements"""
    #annotations = []

    annotation = mentionAnnotation(textSource=file_name,mentionClass=markup.markupClass,
                                    mentionid=tO.getTagID(), spannedText=markup.getText(),
                                    span=markup.markupClass())
   
#eHOST KNOWTATOR XML
#def createAnnotation(markup,tO,file_name): #eventually mention_class will be defined by the logic
#    """Takes a ConTextMarkup object and returns a single annotation object.
#    This will have to be modified for classes other than definiiveEvidence
#    2/24: cut down the unnecessary if statements"""
#    #annotations = []
#
#    annotation = mentionAnnotation(tagObject=tO,textSource=file_name,mentionClass=mention_class,
#                                    mentionid=tO.getTagID(), spannedText=markup.getText(),
#                                    span=markup.getDocSpan())
    return annotation
    
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

def write_knowtator(annotations,text_source): #test_source should be read automatically from the XML string
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
    
def getXML(annotation): #text source should be at the document level
        return annotationXMLSkel.format(annotation.getTextSource(),annotation.getMentionID(),
                annotation.getAnnotatorID(),annotation.getSpan()[0],annotation.getSpan()[1],
                annotation.getText(),annotation.getCreationDate(),annotation.getMentionClass())