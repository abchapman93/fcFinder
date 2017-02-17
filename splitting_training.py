#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 19:21:08 2017

@author: alec
"""
import os
import glob
import pandas as pd
DATADIR = os.path.join(os.path.expanduser('~'),'Box Sync','Radiology Annotation')

#print(os.path.exists(DATADIR))
annotator_folders = ['BTB','DS']
#read file names and info into pandas dataframe

#id
#name
#path
#batch
#yes or no
#note length
#annotator
#train or test
index = 0
failed_names = []
df = pd.DataFrame(columns=['id','name','path','batch','yes','length','annotator','train'])
print(df)
for name in annotator_folders: #annotato
    folder_path = os.path.join(DATADIR,name)
    batches = glob.glob(os.path.join(folder_path,'Batch*'))
    for batch in batches:
        batch_name = os.path.basename(batch) #batch
        
        files = glob.glob(os.path.join(batch,"corpus","*.txt"))
    
        for file in files: #path
            index += 1 #id
            file_name = os.path.basename(file) #file name
            if file_name[:2] == 'No': #yes or no
                yes_or_no = 0
            elif file_name[:2] == 'Yes':
                yes_or_no = 1
            else:
                yes_or_no = None
                failed_names.append(file)
            f1 = open(file, 'r')
            note_length = len(f1.read()) #length
            f1.close()
            #df['id'] = index
            #row = pd.DataFrame(data=[index,file_name,file,batch_name,
                                #yes_or_no,note_length,name,None])
            row =[index,file_name,file,batch_name, yes_or_no,note_length,name,None]
            df.loc[index] = row
            #print(row)
            #row = pd.DataFrame({'id':index,'name':file_name,'path':file,'batch':batch_name,
                                #'yes':yes_or_no,'length':note_length,'annotator':name,'train':None})
            #df.join(row)
print(df)
df.to_csv(os.path.join(DATADIR,'table_of_contents.csv'))
                



#number of total notes
#average length of notes