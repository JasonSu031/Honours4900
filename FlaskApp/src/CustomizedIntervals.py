#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import pandas as pd
import numpy as np
from datetime import datetime
import datetime


# In[2]:


# dataFile = "cupheadkb.tsv"


# In[3]:


def concatAnnotation(cPath, dataFile):
    df = pd.read_csv(os.path.join(cPath,dataFile), sep='\t', header = None, names = ["TS", "elapsed","Annotation"])
    df = df.fillna(method = "ffill")                              #fill the annotations for the data based off of prev value
    return df.iloc[:,2]


# In[9]:


def binaryVectorize(iPath, cPath, dataFile, resample):
    df = pd.read_csv(os.path.join(iPath,dataFile), sep='\t', header = None, names = ["TS", "Key","Event", "Action"])
    # print(df.Event)
    df.Event = df.Event.map(lambda x:x.lower())                                                 #make the values in the event column lowercase
    df = df.assign(Event= df.Event.map({"pressed":1, "released":0}))                            #replace the event values from pressed and released to 0 and 1
    pivot = df.pivot(columns=["Action"], values = ["Event"]).fillna(0).astype(int)              #pivot the table based off of Actions and make empty values 0
    pivot.columns = pivot.columns.droplevel()                                                   #drop the multilevel index called Event
    pivot.columns.name = None                                                                   #drop the multilevel index called Action
    pivot = pivot.set_index(pd.to_datetime(df.TS,format='%Y-%m-%d %H:%M:%S.%f')).reset_index()  #convert the timestamp string to datetime and then set it as index, then reset the index
    
#     print(pivot)
    annotations = concatAnnotation(cPath,dataFile)                                                    #get the annotations as series column
    states = pd.concat([pivot, annotations], axis = 1)                                          #concat the pivot table with annotations
    states= states.resample(resample, on='TS').max().fillna(method="ffill")                     #split the data into even intervals 
    states = states.reset_index()                                                               #reset the index
    
    for columns in states:                                                                      #if the values in the pivot table are decimal values, change them to int
        if(type(states[columns][0])==type(np.float64(2))):                                  
            states[columns] = states[columns].astype(int)
    # print(states)
    # states.to_csv("../Data/ActionState/states"+dataFile,sep = '\t', header=None, index = False)
    return states


# In[10]:


# output = binaryVectorize(dataFile, "500ms")


# In[ ]:




