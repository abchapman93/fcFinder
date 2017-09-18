import os, sys
import pandas as pd

import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import helpers

MODIFIERS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/modifiers.tsv'
TARGETS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/targets.tsv'
REPORTS_FILE = '/Users/alec/bucher/data/MIMIC_RAD/radiology_reports.sqlite'
REFERENCE_STANDARD = '/Users/alec/Box Sync/Radiology Annotation/Reference Standard/Training/saved/Annotations.xlsx'


def extract_markups_from_text(text, targets, modifiers):
    split_report = helpers.my_sentence_splitter(text)
    markups = [create_markup(s=text, span=span, modifiers=modifiers, targets=targets)
                 for (text, span) in split_report
              ]
    print(markups); exit()
# reports = list(df[df.train_val == 'train']['text'])
# reports = [helpers.preprocess(report) for report in reports]
# split_reports = [helpers.my_sentence_splitter(report) for report in reports]
# markups = []
# for report in split_reports[:10]:
#     # Each report is a list of sentence span pairs
#     for text, span in report:
#         m = create_markup(s=text, modifiers=modifiers, targets=targets, span=span)
#         markups.append(m)
# print(markups)
# exit()




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


def evaluate_report(df):
    """
    Evaluates a report by matching pyConText's findings with annotated reference standard
    """
    print(df.head())
    print(df.tail())
    exit()
    


def main():
    modifiers = itemData.instantiateFromCSVtoitemData(MODIFIERS_FILE)
    targets = targets = itemData.instantiateFromCSVtoitemData(TARGETS_FILE)

    df = pd.read_pickle(source_df)
    ref = pd.read_excel(REFERENCE_STANDARD)
    #extract_markups_from_text(df.iloc[0].text, targets, modifiers)

    df['markups'] = df.apply(lambda row: extract_markups_from_text(
                                                row.text, targets, modifiers
                                         ),
                             axis=1
                             )
    print(df.head())
    reports = list(df[df.train_val == 'train']['text'])
    reports = [helpers.preprocess(report) for report in reports]
    split_reports = [helpers.my_sentence_splitter(report) for report in reports]
    markups = []
    for report in split_reports[:10]:
        # Each report is a list of sentence span pairs
        for text, span in report:
            m = create_markup(s=text, modifiers=modifiers, targets=targets, span=span)
            markups.append(m)
    print(markups)
    exit()
           
          
    markups = [create_markup(s=sentence, modifiers=modifiers, targets=targets, span=span) for (sentence, span) in sentence_span_pairs]

    report_names = list(set(df.note_name))
    for report in report_names:
        report_df = df[df.note_name == report]
        evaluate_report(report_df)

if __name__ == '__main__':
    source_df = sys.argv[1]
    
    main()
