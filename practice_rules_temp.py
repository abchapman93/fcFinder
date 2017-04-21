#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 13:23:44 2017

@author: alec
"""

class sentence_classifier(object):
    def __init__(self,sentence,period=None,question_mark=None,classification=None):
        self.sentence=sentence
        self.period=period
        self.question_mark=question_mark
        self.classification=classification
        
        self.is_question_mark()
        self.is_period()
        
    def change_sentence(self,s):
        self.sentence = s
        self.is_question_mark()
        self.is_period()
    def is_question_mark(self):
        if self.sentence[-1] == '?':
            self.question_mark = True
    def is_period(self):
        if self.sentence[-1] == '.':
            self.period = True
    def classify_sentence(self):
        if self.period:
            self.classification = 'statement'
        elif self.question_mark:
            self.classification = 'question'
        else:
            self.classification = 'incomplete'
    def get_classification(self):
        self.classify_sentence()
        return self.classification