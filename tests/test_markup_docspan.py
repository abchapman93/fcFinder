#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 17:24:35 2017

@author: alec
"""

import os
import sys
import unittest
import numpy as np
sys.path.append(os.path.join(os.getcwd(),'..'))
import fcFinder as fc
import helpers
#import rules
import input_output as io
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText
from collections import namedtuple

class MarkupObjectTest(unittest.TestCase):
    def setUp(self):
        self.txt = 'There is fluid collection in the abdomen. There is no hematoma near the liver. Evaluate for abscess.'
        self.sentenceSpanPairs = helpers.my_sentence_splitter(self.txt)
        self.sentences = [x.text for x in self.sentenceSpanPairs]
        self.spans = [x.span for x in self.sentenceSpanPairs]
        #self.sentences = self.sentences.remove('')
        self.modifiers = itemData.instantiateFromCSVtoitemData(
                        "/Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/modifiers.tsv")
        self.targets = itemData.instantiateFromCSVtoitemData(
                        "file:///Users/alec/Box Sync/Bucher_Surgical_MIMICIII/pyConText_implement/fcFinder/targets.tsv")
        self.markups = [fc.markup_sentence(x) for x in self.sentences]
        self.first_markup = self.markups[0]
        self.document = fc.create_context_doc(self.markups)
        
    def test_markup_is_a_markup_object(self):
        self.assertIsInstance(self.first_markup,pyConText.ConTextMarkup)
    def test_markup_doc_span_is_tuple(self):
        self.assertIsInstance(self.first_markup.docSpan,tuple)
    def test_default_markup_sentence_span_starts_with_zero(self):
        self.assertEqual(fc.markup_sentence(self.sentences[0]).docSpan,self.spans[0])
    def test_length_of_create_list_of_markups_equals_length_of_self_markups(self):
        self.assertEqual(len(self.markups), len(fc.create_list_of_markups(self.sentences)))
        
    def test_markup_has_markupclass(self):
        self.assertIsNotNone(self.first_markup.markupClass)
    def test_first_markup_has_markupclass_positive(self):
        self.assertEqual(self.first_markup.markupClass,"Fluid collection-positive")