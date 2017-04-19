#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:24:52 2017

@author: alec
"""

import os, sys
import numpy as np
sys.path.append(os.getcwd())
import fcFinder as fc

def fc_vectorizer(annotations,classes):
    arr = np.zeros((len(classes),1))
    arr = np.ravel(arr)
    for i in range(len(classes)):
        for a in annotations:
            if a == classes[i]:
                arr[i] += 1
    return arr
    """Takes a list of annotations from fcFinder and arbitrary arguments representing the classes.
    Outputs a vector of annotation counts for each class argument."""
    
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