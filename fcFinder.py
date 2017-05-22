"""
@author: Alec Chapman
Last Updated: 5-10-17
"""

import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData

try:
    modifiers = itemData.instantiateFromCSVtoitemData(
            'https://raw.githubusercontent.com/abchapman93/fcFinder/master/modifiers.tsv')
    targets = itemData.instantiateFromCSVtoitemData(
    'https://raw.githubusercontent.com/abchapman93/fcFinder/master/targets.tsv')
except:
    modifiers = None
    targets = None
class markup_conditions(object):
    """This class creates the conditions of interest for a markup.
    A rule-based classifier can then assign a class to a markup based on rules
    pertaining to these conditions.
    """
    def __init__(self,markup=None, target_values=[['fluid_collection']], target=None,
                 modifiers=[], definitive=False, historical=False,probable=False, negated=False,
                 indication=False, anatomy=False, pseudoanatomy=False):
        self.markup=markup
        self.modifiers=modifiers
        self.target_values=target_values
        self.target=target
        self.definitive=definitive
        self.historical=historical
        self.probable=probable
        self.negated=negated
        self.indication=indication
        self.anatomy=anatomy
        self.pseudoanatomy=pseudoanatomy
        
        self.set_target_and_modifiers()
        if self.target:
            self.set_anatomy()
            self.set_definitive()
            self.set_negated()
            self.set_indication()
            self.set_pseudoanatomy()

    def set_target_and_modifiers(self): #These rules should be customized
        for tag_object in self.markup.nodes():
            if tag_object.getCategory() in self.target_values: #could be changed for multiple target values
                self.target = tag_object
            else:
                self.modifiers.append(tag_object)
    def set_anatomy(self):
        if self.markup.isModifiedByCategory(self.target,'anatomy'):
            self.anatomy = True
    def set_definitive(self):
        if self.markup.isModifiedByCategory(self.target,'definitive_existence'):
            self.definitive = True
    def set_negated(self):
        if self.markup.isModifiedByCategory(self.target,'definite_negated_existence'):
            self.negated = True
    def set_indication(self):
        if self.markup.isModifiedByCategory(self.target,'indication'):
            self.indication = True
    def set_pseudoanatomy(self):
        if self.markup.isModifiedByCategory(self.target,'pseudoanatomy'):
            self.pseudoanatomy = True
            
    def add_target(self,new_target):
        """Appends a new target  to target_values"""
        self.target_values.append(new_target)
        self.set_target_and_modifiers()
            
    def __repr__(self): #view the category of the target and all modifiers
        modifier_categories = ['anatomy','definitive','negated','indication','pseudoanatomy']
        try:
            return '{target} modified by: {modifiers}'.format(target=self.target.getCategory(),
                    modifiers=[x for x in modifier_categories
                               if self.__dict__[x]])
        except AttributeError:
            return "Empty Conditions"
    
def markup_classifier(m):
    """Takes a markup conditions object and classifies according to logic defined below.
    Should be customized for implementation."""
    
    conditions = m.conditions
    markup_class = None
    if not conditions.target:
        pass
    
    #positive
    elif (conditions.anatomy and not conditions.negated and not conditions.indication)\
        or (conditions.anatomy and conditions.definitive):
        markup_class = "Fluid collection-positive"
        
    #negated
    elif conditions.negated and not conditions.definitive:
        markup_class = "Fluid collection-negated" #work on making this more generalizable
    
    #indication
    elif conditions.indication and not (conditions.negated or conditions.definitive
                                or conditions.historical or conditions.probable):
        markup_class = "fluid collection-indication"
        
    #check for pseudoanatomy
    if conditions.pseudoanatomy and not conditions.anatomy:
        markup_class = None
    return markup_class

def conditions_decorator(func,markup_conditions=markup_conditions,
                         markup_classifier=markup_classifier):
    """Decorates a create_markup function to add conditions using a markup_conditions object"""
    def wrapper_function(*args,**kwargs):
        markup = func(*args,**kwargs)
        markup.conditions = markup_conditions(markup) #check conditions of interest
        markup.target = markup.conditions.target #save the target for this markup
        markup.modifiers = markup.conditions.modifiers #save the modifiers for this markup
        markup.markupClass = markup_classifier(markup) #classify markup according to target and modifiers,
                                                                   #save class
        return markup
    return wrapper_function

def create_markup(s,span=None,modifiers=modifiers, targets=targets, prune_inactive=True):
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

markup_sentence = conditions_decorator(create_markup)


def create_list_of_markups(sentences,spans=False,modifiers=modifiers,targets=targets):
    """Takes a list of sentences and returns a list of markups.
    If you are passing in document spans for each sentence, set spans = True and
    pass sentences as a list of two-tuples with the sentence in index 0. 
    Example:
        [ ..., ('There is a fluid collection near the abdomen.', (56, 72)), 
           (No rim enhancement can be seen.', (73, 86)),... ] 
    """

    if spans:
        markups = [markup_sentence(s=x[0],span=x[1],modifiers=modifiers,targets=targets)
                    for x in sentences]
    else:
        markups = [markup_sentence(x,modifiers=modifiers,targets=targets)
        for x in sentences] #adds a default span of (0, len(x)))
    return markups

def create_context_doc(list_of_markups,modifiers=modifiers,targets=targets):
    """Creates a ConText document out of a list of markups."""
    context_doc = pyConText.ConTextDocument()
    for m in list_of_markups:
        context_doc.addMarkup(m)
    return context_doc


def fc_pipeline(report, preprocess=lambda x:x.lower(), 
                splitter=lambda x:x.split('.'),spans=False,
                modifiers=modifiers,targets=targets):
    report = preprocess(report)
    sentences = splitter(report)
    markups = create_list_of_markups(sentences,spans=spans,modifiers=modifiers,targets=targets)
    markups = [m for m in markups if m.markupClass]
    return markups






    
