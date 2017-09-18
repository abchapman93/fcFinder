import os, sys
import pandas as pd

import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import helpers

MODIFIERS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/modifiers.tsv'
TARGETS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/targets.tsv'
REPORTS_FILE = '/Users/alec/bucher/data/MIMIC_RAD/radiology_reports.sqlite'

def create_markup(s, modifiers=None, targets=None, span=None, prune_inactive=True):
    """Creates a markup object from a sentence.
    s is a sentence from a list of a split report.
    span is the tuple of the span of the sentence. Optional.
    Returns a named tuple where markup=markup, span=span
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    if not span: #Creates a default docSpan if you're just splitting a list
        span = (0,len(s))
    markup.docSpan = span
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
        
    return markup


def main():
    modifiers = itemData.instantiateFromCSVtoitemData(MODIFIERS_FILE)
    targets = targets = itemData.instantiateFromCSVtoitemData(TARGETS_FILE)

    df = pd.read_pickle(source_df)
    print(df.head())
    print(df.tail())

    reports = list(df[df.train_val == 'train']['text'])
    reports = [helpers.preprocess(report) for report in reports]
    sentences = [helpers.my_sentence_splitter(report) for report in reports]

    markups = []
    markups = [create_markup(s, modifiers=modifiers, targets=targets) for s in sentences]
    print(markups[:5])




if __name__ == '__main__':
    source_df = sys.argv[1]
    
    main()
