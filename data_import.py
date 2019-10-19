import os
import re
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

caselookup = {'numeric':0,'alllower':1,'allupper':2,'initupper':3,'others':4}
labels_lookup = {'B-ORG':0,'O':1,'B-MISC':2,'B-PER':3,'I-PER':4,'B-LOC':5,'I-ORG':6,'I-MISC':7,'I-LOC':8}

def get_data(filename,dir_path,caselookup,labels_lookup):
 
    f = open(dir_path+"\\Data\\"+filename)
    sentences_labels = []
    sentence = []  
    casing_info = []
    sentences_casing = []
    for line in f:
        if len(line)==0 or line.startswith('-DOCSTART') or line[0]=="\n":
            if len(sentence) > 0:
                sentences_labels.append(sentence)
                sentence = []
                sentences_casing.append(casing_info)
                casing_info = []
            continue
        delimiters = " ","\n"
        regexPattern = '|'.join(map(re.escape, delimiters))
        splits = re.split(regexPattern, line)
        #splits = pattern.split(line)
        label_id = labels_lookup[splits[-2]]
        sentence.append([splits[0],label_id])
        casing = casingmap(splits[0],caselookup)
        casing_info.append([splits[0],casing])     

    if len(sentence) >0:
        sentences_labels.append(sentence)
        sentences_casing.append(casing_info)
        sentence = []
        casing_info= []
        
    return sentences_labels,sentences_casing

def casingmap(word,caselookup):
   
    casing = 'others'
    
    if word.isdigit():
        casing = 'numeric'
    elif word.islower():
        casing = 'alllower'
    elif word.isupper():
        casing = 'allupper'
    elif word[0].isupper():
        casing = 'initupper'

    return caselookup[casing]

#sentences_labels,sentences_casing = get_data("train.txt",dir_path,caselookup,labels_lookup)