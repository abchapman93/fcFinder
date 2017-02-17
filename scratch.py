#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 11:06:19 2017

@author: alec
"""

class definitiveEvidence(mentionAnnotation):
    def __init__(self,tagObject,mentionid=None,annotatorid='FC_FINDER',
                 span=None,spannedText=None,creationDate=None, 
                 mentionClass='Fluid collection-definitive'):
        super(definitiveEvidence,self).__init__(tagObject=tagObject, mentionClass=mentionClass,
        mentionid=mentionid, annotatorid=annotatorid,span=span,
        spannedText=spannedText,creationDate=creationDate)
        """Creates an annotation of definitive evidence."""
        self.mentionid = mentionid
        self.annotatorid = annotatorid
        self.span = span
        self.spannedText = spannedText
        self.creationDate = creationDate
        self.mentionClass = mentionClass
        self.setCreationDate()
    
    def setText(self,text):
        """Sets the text for spannedText"""
        self.__spannedText = text
    def setSpan(self,markupScope): #this should be the entire scope for evidence, but not for modifier
        self.__span = markupScope
    def setMentionID(self,ID):
        self.__mentionid = ID
    def setCreationDate(self):
        self.__creationDate = time.strftime("%c") #add time zone
    
    def getMentionClass():
        return self.__mentionClass
    def getMentionID(self):
        return self.__mentionid    
    def getText(self):
        return self.__spannedText
    def getSpan(self):
        return self.__span
    def getCreationDate(self):
        return self.__creationDate