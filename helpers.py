#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:16:35 2017

@author: alec
"""

#test how to retain the span

import re
#import pyConTextNLP.helpers as helpers
import os
from collections import OrderedDict
#DATADIR = '/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/Radiology_Annotation/Adjudication/Batch_3/corpus/Yes_68832_100619_06-01-58.txt'
#DATADIR = '/Users/alec/Box Sync/Radiology_Annotation_Backup/Original Documents/Batch_14/No_62980_181394_08-30-92.txt'
#report = ''
#with open(DATADIR,'r') as f0:
    #report += f0.read()
#len(report)
#report_name = os.path.basename(DATADIR)

#from collections import OrderedDict

def preprocess(report):
    """Preprocesses a report for annotation
    Features:
        - Insert termination points before Headers
        - remove new page headers
        - replace exception words
        - delete ------- ???
        - delete [**3432]
        - delete excess whitespaces
        """
    
    #1) delete new page header
    
    txt = report
    header_exists = re.search("\(Over\)",report)
    while header_exists:
        #find the start of the word 'over'
        re_over = re.compile(r"""\(Over\)""")
        header_over = re_over.search(report)
        header_start = header_over.start()
        #find end of the word 'cont'
        re_cont = re.compile(r"""\(Cont\)""")
        header_cont = re_cont.search(report)
        header_end = header_cont.end()
        #return report[header_end+1]
        #return header_start, header_end
        report = report[:header_start] + report[header_end:]
        header_exists = re.search("\(Over\)",report)
    #0) add a ~ before a heading
    #header_pattern = re.compile(r"""[A-Z])
    headers = ["UNDERLYING MEDICAL CONDITION:", "REASON FOR THIS EXAMINATION:","Reason:","REASON:", "INDICATION:",
               "TECHNIQUE:","WITH IV CONTRAST:","CT OF","IMPRESSION:","WET READ:", "Admitting Diagnosis",
               "COMPARISON:", "FINDINGS:","ADDENDUM:","PFI:","ADDENDUM","PROVISIONAL FINDINGS IMPRESSION","FINAL REPORT"]

    for h in headers:
        report = re.sub(h, "~ "+h,report)
    
    #Replace exception words
    report = re.sub('d\.r\.|dr\.|Dr\.|DR\.','DR',report)
    report = re.sub('EG\.|e\.g\.|eg\.','eg,',report)
    report = re.sub('Mr\.|MR\.|mr\.','MR',report)
    report = re.sub('Mrs\.|MRS\.|mrs\.','MRS',report)
    report = re.sub('Ms\.|MS\.|ms\.','MS',report)
    report = re.sub('M\.D\.|MD\.|M\.d\.|m\.d\.','MD',report)
    report = re.sub('\d{1,}\.','-',report)
    #4) delete deidentified data fields[** **]
    #report = re.sub('\[\*\*[\w\-\(\)]{1,}\*\*\ ]','',report)
    report = re.sub('\[\*\*[^\*]{1,}\*\*\]','',report)
    report = re.sub('Clip #','',report)
    
    # delete times
    report = re.sub('(\d{1,2}:\d{2} )((AM)|(am)|(A.M.)|(a.m.)|(PM)|(pm)|(P.M.)|(p.m.))','',report)
    
    #2) delete excess whitespaces
    report = re.sub('[\n]{2,}','\n',report)
    report = re.sub('[\t]{2,}','\t',report)
    report = re.sub('[ ]{3,}',' ',report)
    
    #3) delete ----
    report = re.sub('[_]{5,}', '\n', report)
    
    
    return report

def my_sentence_splitter(text):
    """Concatenates a text character by character. Sentences end at a termination point
        Returns an OrderedDictionary: Keys are the sentence strings, values are their span in the document
        This can then be passed to pyConText to keep track of the original span of the TagObjects."""
    txt = text
    i = 0 #variable that will just keep track of where we are in the report
    #characterLoc = 0
    termination_points = '.?!~'
    start_span = 0
    end_span = 0
    iteration = 0
    currentSentence = ''
    
    currentCharacter = text[end_span]
    
    spans = OrderedDict()
    while end_span < len(text):
        if currentCharacter in termination_points:
            
            end_span += 1 #one for the current character, one for a whitespace
            currentSentence = txt[start_span:end_span] #append each new character to the string
            
            spans[currentSentence] = (start_span, end_span) #save the sentence in a dictionary with the start and end spans
            
            start_span = end_span + 1 #set the start of the next sentence
            
            i += 1
            
            iteration += 1
            
            try:
            
                currentCharacter = text[start_span]
            except IndexError:
                pass
        else:
            
            end_span += 1
            i += 1
            try:
                currentCharacter = text[end_span]
            except IndexError:
                pass
    return spans

