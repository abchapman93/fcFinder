#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:18:50 2017

@author: alec

This module contains classes that define the rules for classifying sentences
based on fcFinder findings.

The function below should eventually be replaced by more generic rules.
"""

import os

def fluid_collection_classifier(document,source_file):
    """Takes a ConTextDocument and returns the following unique sets of mentionAnnotation objects:
    definitive_evidence: markups that are classified as definitive evidence of fluid collection.
    negated_evidence: markups that are classified as negated evidence of fluid collection.
    indication: markups that are classified as indication of fluid collection.
    MARCH 1: CHANGED DEFINITIVE, PROBABLE AND HISTORICAL TO POSITIVE
    ignored: markups that contain target words but are unmodified by any modifiers"""
    definite_evidence = 0
    negated_evidence = 0
    indication = 0
    historical = 0
    probable = 0
    ignored = 0

    annotations = []
    completed_spans = []
    markups = [m[1] for m in document.getSectionMarkups()]

    for m in markups:
        for tO in m.nodes():
            if tO.getCategory() == ['fluid_collection']:
                annotation = None
                if '?' in m.getRawText():
                    annotation = createAnnotation(m,tO,"fluid collection-indication",source_file)
                    indication += 1
                elif m.isModifiedByCategory(tO,"definite_existence"):
                    if m.isModifiedByCategory(tO,'anatomy'):
                        annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                        definite_evidence += 1
                else:
                    if m.isModifiedByCategory(tO,"definite_negated_existence"):
                        annotation = createAnnotation(m,tO,"Fluid collection-negated",source_file)
                        negated_evidence += 1
                    elif m.isModifiedByCategory(tO, "indication"):
                        annotation = createAnnotation(m,tO,"fluid collection-indication",source_file)
                        indication += 1
                    elif m.isModifiedByCategory(tO,"probable_existence"):
                        if m.isModifiedByCategory(tO,"anatomy"):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            probable += 1
                        else:
                            ignored += 1
                            annotation = None
                    elif m.isModifiedByCategory(tO,"historical"):
                        if m.isModifiedByCategory(tO,"anatomy"):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            historical += 1
                        else:
                            annotation = None
                            ignored += 1
                    else:
                        if m.isModifiedByCategory(tO,'anatomy'):
                            annotation = createAnnotation(m,tO,"Fluid collection-positive",source_file)
                            definite_evidence += 1
                        else:
                            annotation = None
                            ignored += 1
                    if m.isModifiedByCategory(tO,'pseudoanatomy'):
                        if not m.isModifiedByCategory(tO,'anatomy'):
                            annotation = None
                        else:
                            annotation = annotation
                if annotation:
                    if m.getDocSpan() in completed_spans:
                        pass
                    else:
                        completed_spans.append(m.getDocSpan())
                        annotations.append(annotation)
    for _ in annotations:
        if _ == 'false':
            annotations.remove(_)
    return annotations