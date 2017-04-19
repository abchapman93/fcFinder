#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:21:10 2017

@author: alec
"""

"""This module contains functions for reading in files from either directories
or a sqlite database"""

import os
import glob
import sqlite3 as sqlite

def read_file(inpath):
    with open(inpath,'r') as f:
        text = f.read()
    return text
    
def read_batch_of_files(DIR):
    """Reads in an entire batch of text files as a list of strings"""
    files = glob.glob(os.path.join(DIR,'*.txt'))
    texts = []
    for f in files:
        with open(f,'r') as f:
            texts.append(f.read())
    return texts
    
def read_sqlite(db, view=None,query=None):
    """Allows the user to select notes from a sqlite database using either 
    prewritten views or a custom query.
    Parameters:
        conn - database connection
        view - integer specifying which prewritten query to use. Default None.
        query - Custom string query"""
    conn = sqlite.connect(db)
    cursor = conn.cursor()
    if view and query:
        raise ValueError("View and query cannot both be defined.")
    if query:
        cursor.execute(query)
    if view == 1:
        cursor.execute("""SELECT text FROM training_notes""")
    if view == 2:
        cursor.execute("""SELECT text FROM testing_notes""")
    texts = [x[0] for x in cursor.fetchall()]
    return texts