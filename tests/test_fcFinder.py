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
#from fcFinder import markup_conditions, markup_classifier
import helpers
#import rules
import io
import pyConTextNLP.itemData as itemData
import pyConTextNLP.pyConTextGraph as pyConText
from collections import namedtuple

class fcFinderTest(unittest.TestCase):
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
        self.document = fc.create_context_doc(self.markups)
        
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
        self.assertEqual(self.sentences,[x.text for x in helpers.my_sentence_splitter(self.txt)])
    def test_sentence_spans_are_consecutive(self):
        raveled_spans = np.ravel(self.spans)
        for i in range(1,len(raveled_spans),2):
            try:
                self.assertEqual(raveled_spans[i+1] - raveled_spans[i], 1)
            except IndexError:
                pass
        
        
    def test_pipeline_default_preprocessor_returns_lower_case(self):
        preprocessor  = lambda x: x.lower()
        self.assertEqual(self.txt.lower(), preprocessor(self.txt))
    def test_pipeline_default_splitter_returns_split_sentences(self):
        splitter = helpers.my_sentence_splitter
        self.assertEqual(self.sentences,[x.text for x in splitter(self.txt)])
    
    def test_context_doc_get_markups_same_length_as_spans(self):
        self.assertEqual(len(self.document.getSectionMarkups()),len(self.spans))
    def test_context_doc_get_markups_equals_enumerate_self_markups(self):
        self.assertEqual(list(enumerate(self.markups)),self.document.getSectionMarkups())

        
        
class MarkupConditionssTest(unittest.TestCase):
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
        self.document = fc.create_context_doc(self.markups)
        self.empty_markup = pyConText.ConTextMarkup()
        self.first_markup = self.markups[0]
        self.second_markup = self.markups[1]
        self.third_markup = self.markups[2]
        self.first_classifier = fc.markup_conditions(markup=self.first_markup)
        self.second_classifier = fc.markup_conditions(markup=self.second_markup)
        self.third_classifier = fc.markup_conditions(markup=self.third_markup)
        self.classifier = fc.markup_conditions(markup=self.empty_markup)
        
        

    def test_emtpy_markup_nodes_is_empty_list(self):
        self.assertEqual(self.empty_markup.nodes(),[])
    def test_rules_exist(self):
        self.assertIsNotNone(self.classifier)
    
        
    
    def test_default_target_values_is_fluid_collection(self):
        self.assertEqual([['fluid_collection']],self.classifier.target_values)
    def test_target_default_is_none(self):
        self.assertFalse(self.classifier.target)
    def test_default_attributes_not_markup_are_false(self):
        attributes = list(self.classifier.__dict__.keys())
        for a in attributes:
            if a not in ['markup','target_values','tag_objects','modifiers']:
                self.assertFalse(self.classifier.__dict__[a])
                

    def test_first_sentence_has_target(self):
        markup = self.markups[0]
        classifier = fc.markup_conditions(markup)
        self.assertTrue(classifier.target)
    def test_first_sentence_target_is_tag_object(self):
        markup = self.markups[0]
        classifier = fc.markup_conditions(markup)
        self.assertIsInstance(classifier.target,pyConText.tagObject)
    def test_first_sentence_target_has_category_fluid_collection(self):
        self.assertEqual(self.first_classifier.target.getCategory(),['fluid_collection'])
    def test_first_sentence_has_anatomy(self):
        self.assertTrue(self.first_classifier.anatomy)
    def test_first_sentence_is_not_other_categories(self):
        for _ in [self.first_classifier.definitive, self.first_classifier.negated,
                  self.first_classifier.historical, self.first_classifier.indication,
                  self.first_classifier.probable]:
            self.assertFalse(_)
    
    
    def test_second_sentence_has_target(self):
        self.assertTrue(self.second_classifier.target)
    def test_second_sentence_target_has_category_fluid_collection(self):
        self.assertEqual(self.second_classifier.target.getCategory(),['fluid_collection'])
    def test_second_sentence_has_anatomy(self):
        self.assertTrue(self.second_classifier.anatomy)
    def test_second_sentence_is_negated(self):
        self.assertTrue(self.second_classifier.negated)
    def test_second_sentence_is_not_other_categories(self):
        for _ in [self.second_classifier.definitive,
                  self.second_classifier.historical, self.second_classifier.indication,
                  self.second_classifier.probable]:
            self.assertFalse(_)
            
    def test_third_sentence_has_target(self):
        self.assertTrue(self.third_classifier.target)
    def test_third_sentence_target_has_category_fluid_collection(self):
        self.assertEqual(self.third_classifier.target.getCategory(),['fluid_collection'])
    def test_second_sentence_does_not_have_anatomy(self):
        self.assertFalse(self.third_classifier.anatomy)
    def test_third_sentence_is_indication(self):
        self.assertTrue(self.third_classifier.indication)
    def test_third_sentence_is_not_other_categories(self):
        for _ in [self.third_classifier.definitive, self.third_classifier.negated,
                  self.second_classifier.historical,
                  self.second_classifier.probable]:
            self.assertFalse(_)
            
    def test_all_attributes_in_irrelevant_markup_are_false(self):
        i_sentence = 'This could possibly be a sign of pneumonia in the lungs.'
        i_markup = fc.markup_sentence(i_sentence)
        i_classifier = fc.markup_conditions(markup=i_markup)
        attributes = list(i_classifier.__dict__.keys())
        for a in attributes:
            if a not in ['target_values','modifiers']:
                self.assertFalse(i_classifier.__dict__[a])
                
    def test_first_sentence_markup_class_is_positive(self):
        self.assertEqual(self.first_markup.markupClass,"Fluid collection-positive")
    def test_second_sentence_markup_class_is_negated(self):
        self.assertEqual(self.second_markup.markupClass,"Fluid collection-negated")
    def test_third_sentence_markup_class_is_indication(self):
        self.assertEqual(self.third_markup.markupClass,"fluid collection-indication")
    
    def test_indication_with_pseudoanatomy_has_pseudoanatomy(self):
        pseudo_sentence = "Evaluate for sternal fluid collection."
        pseudo_markup = fc.markup_sentence(pseudo_sentence)
        #self.assertIsInstance(pseudo_markup,pyConText.ConTextMarkup)
        pseudo_conditions = fc.markup_conditions(markup=pseudo_markup)
        self.assertTrue(pseudo_conditions.pseudoanatomy)
    def test_indication_with_pseudo_anatomy_is_none(self): #this pseudo rule is not working
        pseudo_sentence = "Evaluate for sternal fluid collection."
        pseudo_markup = fc.markup_sentence(pseudo_sentence)
        #pseudo_conditions = fc.markup_conditions(markup=pseudo_markup)
        self.assertIsNone(pseudo_markup.markupClass)
        
    def test_markup_has_target(self):
        self.assertIsNotNone(self.first_markup.target)
        
class firstPipelineTest(unittest.TestCase):
    def setUp(self):
        DATADIR = '/Users/alec/Desktop/fcfinder_apr21'
        file = os.path.join(DATADIR, 'corpus', 'Yes_74976_148937_02-28-66.txt')
        with open(file,'r') as f:
            report = f.read()
        pipeline = fc.fc_pipeline
        self.markups = pipeline(report)
    def test_markups_all_have_classes(self):
        for m in self.markups:
            self.assertIsNotNone(m.markupClass)
    def test_that_markup_list_is_twenty_three(self):
        self.assertEqual(23,len(self.markups))
    def test_positive_count_is_nineteen(self):
        positive_mentions = [x for x in self.markups if x.markupClass == 'Fluid collection-positive']
        self.assertEqual(19,len(positive_mentions))
 
class secondPipelineTest(unittest.TestCase):
    def setUp(self):
        DATADIR = '/Users/alec/Desktop/fcfinder_apr21'
        file = os.path.join(DATADIR, 'corpus','No_10792_131562_05-29-20.txt')
        with open(file,'r') as f:
            report = f.read()
        pipeline = fc.fc_pipeline
        self.markups = pipeline(report)
    def test_negated_count_is_two(self):
        negated_mentions = [x for x in self.markups if x.markupClass == 'Fluid collection-negated']
        self.assertEqual(2, len(negated_mentions))
   #def test_
#        for _ in self.classifier.__dict__.keys():
#            self.assertIsNone(_)
        
    