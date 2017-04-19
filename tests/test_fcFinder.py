#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:26:32 2017

@author: alec
"""

import os
import sys
import unittest
import numpy as np
sys.path.append(os.path.join(os.getcwd(),'..'))
import fcFinder as fc
import helpers
import output
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText
from collections import namedtuple

class fcFinderTest(unittest.TestCase):
    def setUp(self):
        self.txt = 'There is fluid collection in the abdomen.\n There is no hematoma near the liver.\n Evaluate for abscess.'
        self.sentenceSpanPairs = helpers.my_sentence_splitter(self.txt)
        self.sentences = [x.text for x in self.sentenceSpanPairs]
        self.spans = [x.span for x in self.sentenceSpanPairs]
        #self.sentences = self.sentences.remove('')
        self.modifiers = itemData.instantiateFromCSVtoitemData(
                        "/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/modifiers.tsv")
        self.targets = itemData.instantiateFromCSVtoitemData(
                        "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/targets.tsv")
    
        
    def test_modifiers_exist(self):
        self.assertIsNotNone(self.modifiers)
    def test_targets_exist(self):
        self.assertIsNotNone(self.targets)
        
        
    def test_sentences_length_equals_three(self):
        self.assertEqual(3,len(self.sentences))
    def test_sentence_splitter_returns_list(self):
        self.assertIsInstance(self.sentenceSpanPairs,list)
    def test_sentence_splitter_returns_list_of_namedtuples(self):
        for _ in self.sentenceSpanPairs:
            self.assertIsInstance(_,tuple)
    def test_sentences_are_split_txt(self):
        self.assertEqual(self.sentences,self.txt.split('\n'))
    def test_sentence_spans_are_consecutive(self):
        raveled_spans = np.ravel(self.spans)
        for i in range(1,len(raveled_spans),2):
            try:
                self.assertEqual(raveled_spans[i+1] - raveled_spans[i], 1)
            except IndexError:
                pass
        
        
    def test_markup_sentence_returns_markup(self):
        self.assertIsInstance(fc.markup_sentence(self.sentences[0],(0,0)),pyConText.ConTextMarkup)
    
        