#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:18:50 2017

@author: alec

This module contains classes that define the rules for classifying sentences
based on fcFinder findings. An implementation can include its own custom classifiers.

The function below should eventually be replaced by more generic rules.
"""

import os


#
#class markup_conditions(object):
#    """This class creates the conditions of interest for a markup.
#    A rule-based classifier can then assign a class to a markup based on rules
#    pertaining to these conditions.
#    """
#    def __init__(self,markup=None, target_values=[['fluid_collection']], target=None,
#                 tag_objects=[], definitive=False, historical=False,probable=False, negated=False,
#                 indication=False, anatomy=False, pseudoanatomy=False):
#        self.markup=markup
#        self.tag_objects=tag_objects
#        self.target_values=target_values
#        self.target=target
#        self.definitive=definitive
#        self.historical=historical
#        self.probable=probable
#        self.negated=negated
#        self.indication=indication
#        self.anatomy=anatomy
#        self.pseudoanatomy=pseudoanatomy
#        
#        self.set_target()
#        if self.target:
#            self.set_anatomy()
#            self.set_definitive()
#            self.set_negated()
#            self.set_indication()
#            self.set_pseudoanatomy()
#
#    def set_target(self): #These rules should be customized
#        for tag_object in self.markup.nodes():
#            if tag_object.getCategory() in self.target_values: #could be changed for multiple target values
#                self.target = tag_object
#    def set_anatomy(self):
#        if self.markup.isModifiedByCategory(self.target,'anatomy'):
#            self.anatomy = True
#    def set_definitive(self):
#        if self.markup.isModifiedByCategory(self.target,'definitive_existence'):
#            self.definitive = True
#    def set_negated(self):
#        if self.markup.isModifiedByCategory(self.target,'definite_negated_existence'):
#            self.negated = True
#    def set_indication(self):
#        if self.markup.isModifiedByCategory(self.target,'indication'):
#            self.indication = True
#    def set_pseudoanatomy(self):
#        if self.markup.isModifiedByCategory(self.target,'pseudoanatomy'):
#            self.pseudoanatomy = True
#            
#def markup_classifier(conditions):
#    """Takes a markup_conditions object and classifies according to logic defined below.
#    Should be customized for implementation.
#    Note the lower capitalization of fluid collection-indication; this is only to match
#    the annotations made in the gold standard for this project."""
#    markup_class = None
#    if not conditions.target:
#        pass
#    #positive
#    elif (conditions.anatomy and not conditions.negated and not conditions.indication)\
#        or (conditions.anatomy and conditions.definitive):
#        markup_class = "Fluid collection-positive"
#        
#    #negated
#    elif conditions.negated and not conditions.definitive:
#        markup_class = "Fluid collection-negated"
#    
#    #indication
#    elif conditions.indication and not (conditions.negated or conditions.definitive
#                                or conditions.historical or conditions.probable):
#        markup_class = "fluid collection-indication"
#        
#    #check for pseudoanatomy
#    if conditions.pseudoanatomy and not conditions.anatomy:
#        markup_class = None
#    return markup_class


