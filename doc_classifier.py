#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 11:41:48 2017

@author: alec
"""
import os
import glob
import random
import time
import re
from xml.etree import ElementTree
from xml.etree.cElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

#create document-level annotation
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def create_document_annotation(doc_class,src):
    """Creates a document-level 'Fluid collection-status' annotation."""
    root = Element('annotations')
    root.set('textSource',src)
    annotation_body = SubElement(root,'annotation')
    mentionid = random.randint(1,200000)
    mention = SubElement(annotation_body,'mention')
    mention.set('id',str(mentionid))
    annotatorID = SubElement(annotation_body,'annotator')
    annotatorID.set('id','eHOST_2010')
    annotatorID.text = 'FC_FINDER'
    token_span = (0,15)
    span = SubElement(annotation_body,"span",{"start":str(token_span[0]),"end":str(token_span[1])})
    spannedText = SubElement(annotation_body,'spannedText')
    spannedText.text = 'first word'
    creationDate = SubElement(annotation_body,"creationDate")
    creationDate.text = time.strftime("%c")
    
    stringSlotMention = SubElement(root,'stringSlotMention')
    stringSlotMention.set('id',str(mentionid+1))
    mentionSlot = SubElement(stringSlotMention,'mentionSlot')
    mentionSlot.set('id','existence')
    stringSlotValue = SubElement(stringSlotMention,'stringSlotMentionValue')
    stringSlotValue.set('value',doc_class)
    
    classMention = SubElement(root,'classMention')
    classMention.set('id',str(mentionid))
    hasSlotMention = SubElement(classMention,'hasSlotMention')
    hasSlotMention.set('id',str(mentionid+1))
    mentionClass = SubElement(classMention,'mentionClass')
    mentionClass.set('id','Fluid collection-status')
    mentionClass.text = 'first word'
    
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

def docClassifier(src, dst):
    """Creates a document-level annotation from a given XML file"""
    pos_count = 0
    neg_count = 0
    ind_count = 0
    fname = os.path.basename(src)
    tree = ElementTree.parse(src)
    for node in tree.iter():
        if node.tag == 'mentionClass':
            value = node.attrib
            if value['id'] == 'Fluid collection-positive':
                pos_count += 1
            if value['id'] == 'fluid collection-indication':
                ind_count += 1
            if value['id'] == 'Fluid collection-negated':
                neg_count += 1
    if pos_count >= 1:
        doc_class = 'present'
    else:
        doc_class = 'not present'
    XMLstring = create_document_annotation(doc_class,fname)
    with open(os.path.join(dst,fname),'w') as f0:
        f0.write(XMLstring)
    return
    
def classify_batch(saved_dir, outdir):
    files = glob.glob(os.path.join(saved_dir,'*.xml'))
    counter = 0
    for file in files:
        docClassifier(file,outdir)
        counter += 1
    print('You annotated %d files in %s'%(counter,outdir))
    return

def annotations2Binary(src,dest):
    """Replaces all 'Fluid collection-status: uncertain' mentions with 'present'
    Also replaces annotator names with ABC.
    Additionally, it will replace 'Fluid collection-definitive/probable/historical' with 'Fluid collection-positive' """
    ds = re.compile('>D5</annotator>')
    btb = re.compile('>B4</annotator>')
    annotators = [ds, btb]
    historical = re.compile('Fluid collection-historical')
    probable = re.compile('Fluid collection-probable')
    definitive = re.compile('Fluid collection-definitive')
    regexes = [historical, probable, definitive]
    attribute = re.compile('value="uncertain" />')
    with open(src,'r') as f0:
        xml = f0.read()
    new_xml = xml
    for reg in annotators:
        new_xml = reg.sub('>ABC</annotator>',new_xml)
    for reg in regexes:
        new_xml = reg.sub('Fluid collection-positive',new_xml)
    new_xml = attribute.sub('value="present" />',new_xml)
    with open(dest,'w') as f1:
        f1.write(new_xml)
    return

    
    