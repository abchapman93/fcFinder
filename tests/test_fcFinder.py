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
import output
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText

class fcFinderTest(unittest.TestCase):
    def setUp(self):
        self.txt = 'There is fluid collection in the abdomen. There is no hematoma near the liver. Evaluate for abscess.'
        self.sentences = self.txt.split('.')[:-1]
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
    def test_sentences_are_split_txt(self):
        self.assertEqual(self.sentences,self.txt.split('.')[:-1])
    def test_markup_sentence_returns_markup(self):
        self.assertIsInstance(fc.markup_sentence(self.sentences[0],(0,0)),pyConText.ConTextMarkup)