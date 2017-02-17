#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:16:35 2017

@author: alec
"""

#test how to retain the span

import re
import pyConTextNLP.helpers as helpers
import os
input_report = '/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/Radiology_Annotation/Adjudication/Batch_3/corpus/Yes_28226_116465_05-29-93.txt'
report = ''
with open(input_report,'r') as f0:
    report += f0.read()
len(report)
report_name = os.path.basename(input_report)

from collections import OrderedDict

def retain_span(text):
    """2/6: Have to integrate this into the pyConText process"""
    #sentenceSplitter = helpers.sentenceSplitter()
    #sentences = sentenceSplitter.splitSentences(text)
    txt = text
    i = 0 #variable that will just keep track of where we are in the report
    #characterLoc = 0
    start_span = 0
    end_span = 0
    iteration = 0
    currentSentence = ''
    currentCharacter = text[end_span]
    spans = OrderedDict()
    #while i < len(text):
    while end_span < len(text):
        if currentCharacter in '.?!':
            
            end_span += 2 #one for the current character, one for a whitespace
            currentSentence = txt[start_span:end_span] #append each new character to the string
            
            spans[currentSentence] = (start_span, end_span) #save the sentence in a dictionary with the start and end spans
            
            start_span = end_span + 1 #set the start of the next sentence
            
            i += 1
            
            iteration += 1
            
            currentCharacter = text[start_span]
        else:
            
            end_span += 1
            i += 1
            try:
                currentCharacter = text[end_span]
            except IndexError:
                pass
    #  if any texts remains (due to failure to identify a final sentence termination,
    # then take all remaining text and put into a sentence
    
    ###COME BACK TO THIS, THIS COULD BE A PROBLEM IF A REPORT ENDS WITHOUT A PERIOD
    #if start_span != len(txt):
        #spans[txt[start_span:]] = (start_span,len(txt))

    
    print('current sentence:',currentSentence)
    print('end span:',end_span)
    print('i:',i)
    #print(txt[:end_span])
    return spans
    sentences = []
    wordLoc = 0
    i = 0 #this variable will keep track of the location in the original text
    start_span = 0
    end_span = 0
    spans = {}
    return text[text.find('\s')+1]

print(retain_span(report))



def failed_retain_span(text,regex):
    #sentenceSplitter = helpers.sentenceSplitter()
    #sentences = sentenceSplitter.splitSentences(text)
    txt = text.split()
    sentences = []
    wordLoc = 0
    i = 0 #this variable will keep track of the location in the original text
    start_span = 0
    end_span = 0
    spans = {}
    return text[text.find('\s')]

    
    while len(sentences) < 2:
        start_span = i
        currentWord = txt[wordLoc]
        if currentWord[-1] in '.?!':
            sentence = ' '.join(txt[:wordLoc+1]) #+1 is for the space?
            sentences.append(sentence) 
            txt = txt[wordLoc+1:]
            wordLoc = 0
            i += len(currentWord) +1 #for the new line
            end_span = i
            
            
        else:
            wordLoc += 1
            i += len(currentWord)
            
    for sentence in sentences:
        old_i = i
        sent_index = sentences.index(sentence)
        sent_start = old_i
        i += len(sentence) + 1 #1 is for the space
        sent_end = i
        spans[sent_index] = (sent_start,sent_end)
    print('len:',len(sentences[0]))
    print(sentences[0])
    print('len:',len(report[spans[0][0]:spans[0][1]]))
    return report[spans[0][0]:spans[0][1]]

