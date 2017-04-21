#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:39:09 2017

@author: alec
"""

import os
import sys
import unittest
import numpy as np

sys.path.append(os.path.join(os.getcwd(),'..'))
import fcFinder as fc
import input_output as io

class OutputTest(unittest.TestCase):
    def setUp(self):
        self.input = ('positive','negated','negated','indication')
        self.classes = ['positive','indication','negated']
    def test_vectorizer_returns_length_of_args(self):
        self.assertEqual(3,len(io.fc_vectorizer(self.input,self.classes)))
    def test_vectorizer_returns_array(self):
        self.assertIsInstance(io.fc_vectorizer(self.input,self.classes),np.ndarray)
    def test_vectorizer_array_describes_input(self):
        self.assertEqual(list(np.array([1,1,2])),list(io.fc_vectorizer(self.input,self.classes)))
