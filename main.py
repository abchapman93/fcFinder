import os, sys
import re
import pandas as pd

import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import helpers

MODIFIERS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/modifiers.tsv'
TARGETS_FILE = 'https://raw.githubusercontent.com/abchapman93/fcFinder/master/targets.tsv'
REPORTS_FILE = '/Users/alec/bucher/data/MIMIC_RAD/radiology_reports.sqlite'
REFERENCE_STANDARD = '/Users/alec/Box Sync/Radiology Annotation/Reference Standard/Training/saved/Annotations.xlsx'


def update_reference_df(df):
    span_strings = list(df.Span)
    span_strings = [re.sub('[^0-9,]', '', span) for span in span_strings]
    spans = []
    for span in span_strings:
        try:
            start, end = span.split(',')
            spans.append((int(start), int(end)))
        except:
            spans.append((0, 0))
    df['Span'] = spans
    return df

def extract_markups_from_text(text, targets, modifiers):
    split_report = helpers.my_sentence_splitter(text)
    markups = [create_markup(s=text, span=span, modifiers=modifiers, targets=targets)
                 for (text, span) in split_report
              ]
    markups = [m for m in markups if len(m) != 0]
    return markups
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
        span = (0, len(s))
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


def evaluate_report(markups, annotations):
    """
    Evaluates a report by matching pyConText's findings with annotated reference standard
    `markups` is a list of pyConText markups
    `annotations` is a dataframe where `File Name with extension` == the report name
    """
    for m in markups:
        overlapping_annotations = find_overlapping_annotations(m, annotations)
        print(overlapping_annotations)
        print(m)    
        markup_classes = []
        for t in m.getMarkedTargets():
            markup_class = classify_markup(m, t)
            if markup_class:
                 markup_classes.append(markup_class)
        print("Markup classes:")
        print(markup_classes)
   
 
def find_overlapping_annotations(m, annotations):

    def overlaps(m_span, a_span):
        m_span = [int(n) for n in m_span]
        a_span = [int(n) for n in a_span]
        print(m_span, a_span)
        overlap = ((a_span[0] <= m_span[0] <= a_span[1])
                                |
                  (a_span[0] <= m_span[1] <= a_span[1]))
        print(overlap)
        return overlap

    overlapping_idx = []
    for i, row in annotations.iterrows():
        try:
            if overlaps(m.docSpan, row.Span):
                print("Match")
                print(i)
                overlapping_idx.append(i)
        except:
            continue
    try:
        overlapping_annotations = annotations.iloc[overlapping_idx]
        print("Success")
    except:
        overlapping_annotations = None
    return overlapping_annotations


def classify_markup(m, target):
    """This function will be unique to each project"""
    
    fluid_collection = False
    anatomy = False
    negated = False
    indication = False

    if target.getCategory() == ['fluid_collection']:
        fluid_collection = True
    if m.isModifiedByCategory(target, 'anatomy'):
        anatomy = True
    if m.isModifiedByCategory(target, 'definite_negated_existence'):
        negated = True


    if fluid_collection and negated:
        markup_class = 'Fluid collection-negated'
    elif fluid_collection and indication:
        markup_class = 'fluid collection-indication'
    elif fluid_collection and anatomy:
        markup_class = 'Fluid collection-positive'
    else:
        markup_class = None
    return markup_class
    

def main():
    modifiers = itemData.instantiateFromCSVtoitemData(MODIFIERS_FILE)
    targets = targets = itemData.instantiateFromCSVtoitemData(TARGETS_FILE)

    df = pd.read_pickle(source_df)
    df = df.iloc[:10]
    ref = pd.read_excel(REFERENCE_STANDARD)
    ref = update_reference_df(ref)
    extract_markups_from_text(df.iloc[0].text, targets, modifiers)

    df['markups'] = df.apply(lambda row: extract_markups_from_text(
                                                row.text, targets, modifiers
                                         ),
                             axis=1
                             )
    print(df.head())
    for idx, row in df.iterrows():
        # Get all annotations from reference standard with this report name
        annotations = ref[ref['File Name with extension'] == row.note_name]
        evaluate_report(row.markups, annotations)

    exit()
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
