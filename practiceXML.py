#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 11:15:11 2017

@author: alec
"""

import fcClasses
import fcFinder
import os
import shutil

markup1 = fcFinder.markup_sentence('There is a fluid collection in the abdomen.',modifiers,targets)
tagObject1 = markup1.nodes()[0]
annotation1 = fcClasses.createAnnotations(markup1,'fluid collection-definitive','teststring.txt')[0]

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

test = getXML(annotation1)

writeKnowtator(test,"No_20117_107563_05-03-68.txt",
               os.path.join(os.path.expanduser('~'),'XML_test_files'))
"""No_20117_107563_05-03-68.txt.knowtator.xml"""
#annotationXMLSkel.format("file.txt",12345)

ehost_annotation = \
"""
<?xml version="1.0" encoding="UTF-8"?>
<annotations textSource="No_20117_107563_05-03-68.txt">
    <annotation>
        <mention id="EHOST_Instance_1" />
        <annotator id="eHOST_2010">ADJUDICATION</annotator>
        <span start="141" end="177" />
        <spannedText>assess fluid collections/infiltrates</spannedText>
        <creationDate>Thu Dec 22 12:28:53 MST 2016</creationDate>
    </annotation>
    <classMention id="EHOST_Instance_1">
        <mentionClass id="fluid collection-indication">assess fluid collections/infiltrates</mentionClass>
    </classMention>
    <annotation>
        <mention id="EHOST_Instance_2" />
        <annotator id="eHOST_2010">ADJUDICATION</annotator>
        <span start="438" end="474" />
        <spannedText>assess fluid collections/infiltrates</spannedText>
        <creationDate>Thu Dec 22 12:29:07 MST 2016</creationDate>
    </annotation>
    <classMention id="EHOST_Instance_2">
        <mentionClass id="fluid collection-indication">assess fluid collections/infiltrates</mentionClass>
    </classMention>
    <annotation>
        <mention id="EHOST_Instance_3" />
        <annotator id="eHOST_2010">ADJUDICATION</annotator>
        <span start="749" end="771" />
        <spannedText>Assess for loculation.</spannedText>
        <creationDate>Wed Dec 14 15:54:48 MST 2016</creationDate>
    </annotation>
    <classMention id="EHOST_Instance_3">
        <mentionClass id="fluid collection-indication">Assess for loculation.</mentionClass>
    </classMention>
    <annotation>
        <mention id="EHOST_Instance_4" />
        <annotator id="eHOST_2010">ADJUDICATION</annotator>
        <span start="3195" end="3231" />
        <spannedText>assess fluid collections/infiltrates</spannedText>
        <creationDate>Wed Dec 14 15:55:38 MST 2016</creationDate>
    </annotation>
    <classMention id="EHOST_Instance_4">
        <mentionClass id="fluid collection-indication">assess fluid collections/infiltrates</mentionClass>
    </classMention>
    <annotation>
        <mention id="EHOST_Instance_5" />
        <annotator id="eHOST_2010">ADJUDICATION</annotator>
        <span start="0" end="15" />
        <spannedText>[**2527-5-27**]</spannedText>
        <creationDate>Thu Dec 22 12:29:43 MST 2016</creationDate>
    </annotation>
    <stringSlotMention id="EHOST_Instance_6">
        <mentionSlot id="existence" />
        <stringSlotMentionValue value="not present" />
    </stringSlotMention>
    <classMention id="EHOST_Instance_5">
        <hasSlotMention id="EHOST_Instance_6" />
        <mentionClass id="Fluid collection-status">[**2527-5-27**]</mentionClass>
    </classMention>
    <eHOST_Adjudication_Status version="1.0">
        <Adjudication_Selected_Annotators version="1.0" />
        <Adjudication_Selected_Classes version="1.0" />
        <Adjudication_Others>
            <CHECK_OVERLAPPED_SPANS>false</CHECK_OVERLAPPED_SPANS>
            <CHECK_ATTRIBUTES>false</CHECK_ATTRIBUTES>
            <CHECK_RELATIONSHIP>false</CHECK_RELATIONSHIP>
            <CHECK_CLASS>false</CHECK_CLASS>
            <CHECK_COMMENT>false</CHECK_COMMENT>
        </Adjudication_Others>
    </eHOST_Adjudication_Status>
</annotations>
"""
